#!/bin/bash

# fail fast
set -e

# check for root
if test "$(id -u)" -ne 0; then
	echo "Must be run as root"
	exit 1
fi

# We will be starting a systemd service, but another tests might do the same
# so this makes sure there is nothing left after we exit
trap "systemctl stop knot-resolver.service" EXIT


if ! systemctl start knot-resolver.service; then
	echo
	echo "Failed to start service, here is its status:"
	systemctl status knot-resolver.service || true
	echo
	echo "knot-resolver.service:"
	systemctl cat knot-resolver.service || true
	echo
	echo "Checking service user using \`id knot-resolver\`:"
	id knot-resolver
	exit 1
else
	# check that the resolvers are actually running
	kdig @127.0.0.1 nic.cz

	echo "Running interactive tests..."
	for test in "$(dirname $0)"/interactive/*; do
		echo "[test] $test"
		$test
	done
fi

