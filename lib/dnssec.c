/*  Copyright (C) 2015-2017 CZ.NIC, z.s.p.o. <knot-dns@labs.nic.cz>
 *  SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <libdnssec/binary.h>
#include <libdnssec/crypto.h>
#include <libdnssec/error.h>
#include <libdnssec/key.h>
#include <libdnssec/sign.h>
#include <libknot/descriptor.h>
#include <libknot/packet/wire.h>
#include <libknot/rdataset.h>
#include <libknot/rrset.h>
#include <libknot/rrtype/dnskey.h>
#include <libknot/rrtype/nsec.h>
#include <libknot/rrtype/rrsig.h>

#include "contrib/cleanup.h"
#include "lib/defines.h"
#include "lib/dnssec/nsec.h"
#include "lib/dnssec/nsec3.h"
#include "lib/dnssec/signature.h"
#include "lib/dnssec.h"
#include "lib/resolve.h"

/* forward */
static int kr_rrset_validate_with_key(kr_rrset_validation_ctx_t *vctx,
	knot_rrset_t *covered, size_t key_pos, const struct dnssec_key *key);

void kr_crypto_init(void)
{
	dnssec_crypto_init();
}

void kr_crypto_cleanup(void)
{
	dnssec_crypto_cleanup();
}

void kr_crypto_reinit(void)
{
	dnssec_crypto_reinit();
}

#define FLG_WILDCARD_EXPANSION 0x01 /**< Possibly generated by using wildcard expansion. */

/**
 * Check the RRSIG RR validity according to RFC4035 5.3.1 .
 * @param flags     The flags are going to be set according to validation result.
 * @param cov_labels Covered RRSet owner label count.
 * @param rrsigs    rdata containing the signatures.
 * @param key_alg   DNSKEY's algorithm.
 * @param keytag    Used key tag.
 * @param vctx->zone_name The name of the zone cut (and the DNSKEY).
 * @param vctx->timestamp Validation time.
 */
static int validate_rrsig_rr(int *flags, int cov_labels,
                             const knot_rdata_t *rrsigs,
                             uint8_t key_alg,
			     uint16_t keytag,
                             kr_rrset_validation_ctx_t *vctx)
{
	if (kr_fails_assert(flags && rrsigs && vctx && vctx->zone_name)) {
		return kr_error(EINVAL);
	}
	/* bullet 5 */
	if (knot_rrsig_sig_expiration(rrsigs) < vctx->timestamp) {
		vctx->rrs_counters.expired++;
		return kr_error(EINVAL);
	}
	/* bullet 6 */
	if (knot_rrsig_sig_inception(rrsigs) > vctx->timestamp) {
		vctx->rrs_counters.notyet++;
		return kr_error(EINVAL);
	}
	/* bullet 2 */
	const knot_dname_t *signer_name = knot_rrsig_signer_name(rrsigs);
	if (!signer_name || !knot_dname_is_equal(signer_name, vctx->zone_name)) {
		vctx->rrs_counters.signer_invalid++;
		return kr_error(EAGAIN);
	}
	/* bullet 4 */
	{
		int rrsig_labels = knot_rrsig_labels(rrsigs);
		if (rrsig_labels > cov_labels) {
			vctx->rrs_counters.labels_invalid++;
			return kr_error(EINVAL);
		}
		if (rrsig_labels < cov_labels) {
			*flags |= FLG_WILDCARD_EXPANSION;
		}
	}

	/* bullet 7
	 * Part checked elsewhere: key owner matching the zone_name. */
	if (key_alg != knot_rrsig_alg(rrsigs) || keytag != knot_rrsig_key_tag(rrsigs)) {
		vctx->rrs_counters.key_invalid++;
		return kr_error(EINVAL);
	}
	/* bullet 8 */
	/* Checked somewhere else. */
	/* bullet 9 and 10 */
	/* One of the requirements should be always fulfilled. */

	return kr_ok();
}

/**
 * Returns the number of labels that have been added by wildcard expansion.
 * @param expanded Expanded wildcard.
 * @param rrsigs   RRSet containing the signatures.
 * @param sig_pos  Specifies the signature within the RRSIG RRSet.
 * @return         Number of added labels, -1 on error.
 */
static inline int wildcard_radix_len_diff(const knot_dname_t *expanded,
					  const knot_rdata_t *rrsig)
{
	if (!expanded || !rrsig) {
		return -1;
	}

	return knot_dname_labels(expanded, NULL) - knot_rrsig_labels(rrsig);
}

int kr_rrset_validate(kr_rrset_validation_ctx_t *vctx, knot_rrset_t *covered)
{
	if (!vctx) {
		return kr_error(EINVAL);
	}
	if (!vctx->pkt || !covered || !vctx->keys || !vctx->zone_name) {
		return kr_error(EINVAL);
	}

	memset(&vctx->rrs_counters, 0, sizeof(vctx->rrs_counters));
	for (unsigned i = 0; i < vctx->keys->rrs.count; ++i) {
		int ret = kr_rrset_validate_with_key(vctx, covered, i, NULL);
		if (ret == 0) {
			return ret;
		}
	}

	return kr_error(ENOENT);
}

/** Assuming `rrs` was validated with `sig`, trim its TTL in case it's over-extended. */
static bool trim_ttl(knot_rrset_t *rrs, const knot_rdata_t *sig,
			uint32_t timestamp, const struct kr_query *log_qry)
{
	const uint32_t ttl_max = MIN(knot_rrsig_original_ttl(sig),
			knot_rrsig_sig_expiration(sig) - timestamp);
	if (likely(rrs->ttl <= ttl_max))
		return false;
	if (kr_log_is_debug_qry(VALIDATOR, log_qry)) {
		auto_free char *name_str = kr_dname_text(rrs->owner),
				*type_str = kr_rrtype_text(rrs->type);
		QRVERBOSE(log_qry, VALIDATOR, "trimming TTL of %s %s: %d -> %d\n",
			name_str, type_str, (int)rrs->ttl, (int)ttl_max);
	}
	rrs->ttl = ttl_max;
	return true;
}


typedef struct {
	struct dnssec_key *key;
	uint8_t alg;
	uint16_t tag;
} kr_svldr_key_t;

static int svldr_key_new(const knot_rdata_t *rdata, const knot_dname_t *owner,
			 kr_svldr_key_t *result)
{
	result->alg = knot_dnskey_alg(rdata);
	result->key = NULL; // just silence analyzers
	int ret = kr_dnssec_key_from_rdata(&result->key, owner, rdata->data, rdata->len);
	if (likely(ret == 0))
		result->tag = dnssec_key_get_keytag(result->key);
	return ret;
}
static inline void svldr_key_del(kr_svldr_key_t *skey)
{
	kr_dnssec_key_free(&skey->key);
}

static int kr_svldr_rrset_with_key(knot_rrset_t *rrs, const knot_rdataset_t *rrsigs,
				kr_rrset_validation_ctx_t *vctx, const kr_svldr_key_t *key)
{
	const int covered_labels = knot_dname_labels(rrs->owner, NULL)
				- knot_dname_is_wildcard(rrs->owner);
	knot_rdata_t *rdata_j = rrsigs->rdata;
	for (uint16_t j = 0; j < rrsigs->count; ++j, rdata_j = knot_rdataset_next(rdata_j)) {
		if (kr_fails_assert(knot_rrsig_type_covered(rdata_j) == rrs->type))
			continue; //^^ not a problem but no reason to allow them in the API
		int val_flgs = 0;
		int retv = validate_rrsig_rr(&val_flgs, covered_labels, rdata_j,
						key->alg, key->tag, vctx);
		if (retv == kr_error(EAGAIN)) {
			vctx->result = retv;
			return vctx->result;
		} else if (retv != 0) {
			continue;
		}
		// We only expect non-expanded wildcard records in input;
		// that also means we don't need to perform non-existence proofs.
		const int trim_labels = (val_flgs & FLG_WILDCARD_EXPANSION) ? 1 : 0;
		if (kr_check_signature(rdata_j, key->key, rrs, trim_labels) == 0) {
			trim_ttl(rrs, rdata_j, vctx->timestamp, vctx->log_qry);
			vctx->result = kr_ok();
			return vctx->result;
		} else {
			vctx->rrs_counters.crypto_invalid++;
		}
	}
	vctx->result = kr_error(ENOENT);
	return vctx->result;
}
/* The implementation basically performs "parts of" kr_rrset_validate(). */


/**
 * Validate RRSet using a specific key.
 * @param vctx    Pointer to validation context.
 * @param covered RRSet covered by a signature.  It must be in canonical format.
 * 		  TTL may get lowered.
 * @param key_pos Position of the key to be validated with.
 * @param key     Key to be used to validate.
 *		  If NULL, then key from DNSKEY RRSet is used.
 * @return        0 or error code, same as vctx->result.
 */
static int kr_rrset_validate_with_key(kr_rrset_validation_ctx_t *vctx,
				knot_rrset_t *covered,
				size_t key_pos, const struct dnssec_key *key)
{
	const knot_pkt_t *pkt         = vctx->pkt;
	const knot_rrset_t *keys      = vctx->keys;
	const knot_dname_t *zone_name = vctx->zone_name;
	bool has_nsec3		      = vctx->has_nsec3;
	struct dnssec_key *created_key = NULL;

	if (!knot_dname_is_equal(keys->owner, zone_name)
	   /* It's just caller's approximation that the RR is in that particular zone,
	    * so we verify that in the following condition.
	    * We MUST guard against attempts of zones signing out-of-bailiwick records. */
	    || knot_dname_in_bailiwick(covered->owner, zone_name) < 0) {
		vctx->result = kr_error(ENOENT);
		return vctx->result;
	}

	const knot_rdata_t *key_rdata = knot_rdataset_at(&keys->rrs, key_pos);
	if (key == NULL) {
		int ret = kr_dnssec_key_from_rdata(&created_key, keys->owner,
						   key_rdata->data, key_rdata->len);
		if (ret != 0) {
			vctx->result = ret;
			return vctx->result;
		}
		key = created_key;
	}
	uint16_t keytag = dnssec_key_get_keytag(key);
	const uint8_t key_alg = knot_dnskey_alg(key_rdata);
	/* The asterisk does not count, RFC4034 3.1.3, paragraph 3. */
	const int covered_labels = knot_dname_labels(covered->owner, NULL)
				- knot_dname_is_wildcard(covered->owner);

	for (uint16_t i = 0; i < vctx->rrs->len; ++i) {
		/* Consider every RRSIG that matches and comes from the same query. */
		const knot_rrset_t *rrsig = vctx->rrs->at[i]->rr;
		const bool ok = vctx->rrs->at[i]->qry_uid == vctx->qry_uid
			&& rrsig->type == KNOT_RRTYPE_RRSIG
			&& rrsig->rclass == covered->rclass
			&& knot_dname_is_equal(rrsig->owner, covered->owner);
		if (!ok)
			continue;

		knot_rdata_t *rdata_j = rrsig->rrs.rdata;
		for (uint16_t j = 0; j < rrsig->rrs.count; ++j, rdata_j = knot_rdataset_next(rdata_j)) {
			int val_flgs = 0;
			int trim_labels = 0;
			if (knot_rrsig_type_covered(rdata_j) != covered->type) {
				continue;
			}
			kr_rank_set(&vctx->rrs->at[i]->rank, KR_RANK_BOGUS); /* defensive style */
			vctx->rrs_counters.matching_name_type++;
			int retv = validate_rrsig_rr(&val_flgs, covered_labels, rdata_j,
							key_alg, keytag, vctx);
			if (retv == kr_error(EAGAIN)) {
				kr_dnssec_key_free(&created_key);
				vctx->result = retv;
				return retv;
			} else if (retv != 0) {
				continue;
			}
			if (val_flgs & FLG_WILDCARD_EXPANSION) {
				trim_labels = wildcard_radix_len_diff(covered->owner, rdata_j);
				if (trim_labels < 0) {
					break;
				}
			}
			if (kr_check_signature(rdata_j, key, covered, trim_labels) != 0) {
				vctx->rrs_counters.crypto_invalid++;
				continue;
			}
			if (val_flgs & FLG_WILDCARD_EXPANSION) {
				int ret = 0;
				if (!has_nsec3) {
					ret = kr_nsec_wildcard_answer_response_check(pkt, KNOT_AUTHORITY, covered->owner);
				} else {
					ret = kr_nsec3_wildcard_answer_response_check(pkt, KNOT_AUTHORITY, covered->owner, trim_labels - 1);
					if (ret == kr_error(KNOT_ERANGE)) {
						ret = 0;
						vctx->flags |= KR_DNSSEC_VFLG_OPTOUT;
					}
				}
				if (ret != 0) {
					vctx->rrs_counters.nsec_invalid++;
					continue;
				}
				vctx->flags |= KR_DNSSEC_VFLG_WEXPAND;
			}

			trim_ttl(covered, rdata_j, vctx->timestamp, vctx->log_qry);

			kr_dnssec_key_free(&created_key);
			vctx->result = kr_ok();
			kr_rank_set(&vctx->rrs->at[i]->rank, KR_RANK_SECURE); /* upgrade from bogus */
			return vctx->result;
		}
	}
	/* No applicable key found, cannot be validated. */
	kr_dnssec_key_free(&created_key);
	vctx->result = kr_error(ENOENT);
	return vctx->result;
}

bool kr_ds_algo_support(const knot_rrset_t *ta)
{
	if (kr_fails_assert(ta && ta->type == KNOT_RRTYPE_DS && ta->rclass == KNOT_CLASS_IN))
		return false;
	/* Check if at least one DS has a usable algorithm pair. */
	knot_rdata_t *rdata_i = ta->rrs.rdata;
	for (uint16_t i = 0; i < ta->rrs.count;
			++i, rdata_i = knot_rdataset_next(rdata_i)) {
		if (dnssec_algorithm_digest_support(knot_ds_digest_type(rdata_i))
		    && dnssec_algorithm_key_support(knot_ds_alg(rdata_i))) {
			return true;
		}
	}
	return false;
}

int kr_dnskeys_trusted(kr_rrset_validation_ctx_t *vctx, const knot_rdataset_t *sigs,
			const knot_rrset_t *ta)
{
	knot_rrset_t *keys = vctx->keys;
	const bool ok = keys && ta && ta->rrs.count && ta->rrs.rdata
			&& ta->type == KNOT_RRTYPE_DS
			&& knot_dname_is_equal(ta->owner, keys->owner);
	if (kr_fails_assert(ok))
		return kr_error(EINVAL);

	/* RFC4035 5.2, bullet 1
	 * The supplied DS record has been authenticated.
	 * It has been validated or is part of a configured trust anchor.
	 */
	knot_rdata_t *krr = keys->rrs.rdata;
	for (int i = 0; i < keys->rrs.count; ++i, krr = knot_rdataset_next(krr)) {
		/* RFC4035 5.3.1, bullet 8 */ /* ZSK */
		if (!kr_dnssec_key_zsk(krr->data) || kr_dnssec_key_revoked(krr->data))
			continue;

		kr_svldr_key_t key;
		if (svldr_key_new(krr, keys->owner, &key) != 0)
			continue; // it might e.g. be malformed

		int ret = kr_authenticate_referral(ta, key.key);
		if (ret == 0)
			ret = kr_svldr_rrset_with_key(keys, sigs, vctx, &key);
		svldr_key_del(&key);
		if (ret == 0) {
			kr_assert(vctx->result == 0);
			return vctx->result;
		}
	}

	/* No useable key found */
	vctx->result = kr_error(ENOENT);
	return vctx->result;
}

bool kr_dnssec_key_zsk(const uint8_t *dnskey_rdata)
{
	return knot_wire_read_u16(dnskey_rdata) & 0x0100;
}

bool kr_dnssec_key_ksk(const uint8_t *dnskey_rdata)
{
	return knot_wire_read_u16(dnskey_rdata) & 0x0001;
}

/** Return true if the DNSKEY is revoked. */
bool kr_dnssec_key_revoked(const uint8_t *dnskey_rdata)
{
	return knot_wire_read_u16(dnskey_rdata) & 0x0080;
}

int kr_dnssec_key_tag(uint16_t rrtype, const uint8_t *rdata, size_t rdlen)
{
	if (!rdata || rdlen == 0 || (rrtype != KNOT_RRTYPE_DS && rrtype != KNOT_RRTYPE_DNSKEY)) {
		return kr_error(EINVAL);
	}
	if (rrtype == KNOT_RRTYPE_DS) {
		return knot_wire_read_u16(rdata);
	} else if (rrtype == KNOT_RRTYPE_DNSKEY) {
		struct dnssec_key *key = NULL;
		int ret = kr_dnssec_key_from_rdata(&key, NULL, rdata, rdlen);
		if (ret != 0) {
			return ret;
		}
		uint16_t keytag = dnssec_key_get_keytag(key);
		kr_dnssec_key_free(&key);
		return keytag;
	} else {
		return kr_error(EINVAL);
	}
}

int kr_dnssec_key_match(const uint8_t *key_a_rdata, size_t key_a_rdlen,
                        const uint8_t *key_b_rdata, size_t key_b_rdlen)
{
	dnssec_key_t *key_a = NULL, *key_b = NULL;
	int ret = kr_dnssec_key_from_rdata(&key_a, NULL, key_a_rdata, key_a_rdlen);
	if (ret != 0) {
		return ret;
	}
	ret = kr_dnssec_key_from_rdata(&key_b, NULL, key_b_rdata, key_b_rdlen);
	if (ret != 0) {
		dnssec_key_free(key_a);
		return ret;
	}
	/* If the algorithm and the public key match, we can be sure
	 * that they are the same key. */
	ret = kr_error(ENOENT);
	dnssec_binary_t pk_a, pk_b;
	if (dnssec_key_get_algorithm(key_a) == dnssec_key_get_algorithm(key_b) &&
	    dnssec_key_get_pubkey(key_a, &pk_a) == DNSSEC_EOK &&
	    dnssec_key_get_pubkey(key_b, &pk_b) == DNSSEC_EOK) {
		if (pk_a.size == pk_b.size && memcmp(pk_a.data, pk_b.data, pk_a.size) == 0) {
			ret = 0;
		}
	}
	dnssec_key_free(key_a);
	dnssec_key_free(key_b);
	return ret;
}

int kr_dnssec_key_from_rdata(struct dnssec_key **key, const knot_dname_t *kown, const uint8_t *rdata, size_t rdlen)
{
	if (!key || !rdata || rdlen == 0) {
		return kr_error(EINVAL);
	}

	dnssec_key_t *new_key = NULL;
	const dnssec_binary_t binary_key = {
		.size = rdlen,
		.data = (uint8_t *)rdata
	};

	int ret = dnssec_key_new(&new_key);
	if (ret != DNSSEC_EOK) {
		return kr_error(ENOMEM);
	}
	ret = dnssec_key_set_rdata(new_key, &binary_key);
	if (ret != DNSSEC_EOK) {
		dnssec_key_free(new_key);
		return kr_error(ret);
	}
	if (kown) {
		ret = dnssec_key_set_dname(new_key, kown);
		if (ret != DNSSEC_EOK) {
			dnssec_key_free(new_key);
			return kr_error(ENOMEM);
		}
	}

	*key = new_key;
	return kr_ok();
}

void kr_dnssec_key_free(struct dnssec_key **key)
{
	if (kr_fails_assert(key))
		return;

	dnssec_key_free(*key);
	*key = NULL;
}

int kr_dnssec_matches_name_and_type(const ranked_rr_array_t *rrs, uint32_t qry_uid,
				    const knot_dname_t *name, uint16_t type)
{
	int ret = kr_error(ENOENT);
	for (size_t i = 0; i < rrs->len; ++i) {
		const ranked_rr_array_entry_t *entry = rrs->at[i];
		if (kr_fails_assert(!entry->in_progress))
			return kr_error(EINVAL);
		const knot_rrset_t *nsec = entry->rr;
		if (entry->qry_uid != qry_uid || entry->yielded) {
			continue;
		}
		if (nsec->type != KNOT_RRTYPE_NSEC &&
		    nsec->type != KNOT_RRTYPE_NSEC3) {
			continue;
		}
		if (!kr_rank_test(entry->rank, KR_RANK_SECURE)) {
			continue;
		}
		if (nsec->type == KNOT_RRTYPE_NSEC) {
			ret = kr_nsec_matches_name_and_type(nsec, name, type);
		} else {
			ret = kr_nsec3_matches_name_and_type(nsec, name, type);
		}
		if (ret == kr_ok()) {
			return kr_ok();
		} else if (ret != kr_error(ENOENT)) {
			return ret;
		}
	}
	return ret;
}
