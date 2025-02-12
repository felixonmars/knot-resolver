.. SPDX-License-Identifier: GPL-3.0-or-later

.. _config-monitoring-stats:

Statistics collector
====================

Module ``stats`` gathers various counters from the query resolution
and server internals, and offers them as a key-value storage.
These metrics can be either exported to :ref:`mod-graphite`,
exposed as :ref:`mod-http-prometheus`, or processed using user-provided script
as described in chapter :ref:`async-events`.

.. note:: Please remember that each Knot Resolver instance keeps its own
   statistics, and instances can be started and stopped dynamically. This might
   affect your data postprocessing procedures if you are using
   :ref:`systemd-multiple-instances`.

.. _mod-stats-list:

Built-in statistics
-------------------

Built-in counters keep track of number of queries and answers matching specific criteria.

+-----------------------------------------------------------------+
| **Global request counters**                                     |
+------------------+----------------------------------------------+
| request.total    | total number of DNS requests                 |
|                  | (including internal client requests)         |
+------------------+----------------------------------------------+
| request.internal | internal requests generated by Knot Resolver |
|                  | (e.g. DNSSEC trust anchor updates)           |
+------------------+----------------------------------------------+
| request.udp      | external requests received over plain UDP    |
|                  | (:rfc:`1035`)                                |
+------------------+----------------------------------------------+
| request.tcp      | external requests received over plain TCP    |
|                  | (:rfc:`1035`)                                |
+------------------+----------------------------------------------+
| request.dot      | external requests received over              |
|                  | DNS-over-TLS (:rfc:`7858`)                   |
+------------------+----------------------------------------------+
| request.doh      | external requests received over              |
|                  | DNS-over-HTTP (:rfc:`8484`)                  |
+------------------+----------------------------------------------+
| request.xdp      | external requests received over plain UDP    |
|                  | via an AF_XDP socket                         |
+------------------+----------------------------------------------+

+----------------------------------------------------+
| **Global answer counters**                         |
+-----------------+----------------------------------+
| answer.total    | total number of answered queries |
+-----------------+----------------------------------+
| answer.cached   | queries answered from cache      |
+-----------------+----------------------------------+

+-----------------+----------------------------------+
| **Answers categorized by RCODE**                   |
+-----------------+----------------------------------+
| answer.noerror  | NOERROR answers                  |
+-----------------+----------------------------------+
| answer.nodata   | NOERROR, but empty answers       |
+-----------------+----------------------------------+
| answer.nxdomain | NXDOMAIN answers                 |
+-----------------+----------------------------------+
| answer.servfail | SERVFAIL answers                 |
+-----------------+----------------------------------+

+-----------------+----------------------------------+
| **Answer latency**                                 |
+-----------------+----------------------------------+
| answer.1ms      | completed in 1ms                 |
+-----------------+----------------------------------+
| answer.10ms     | completed in 10ms                |
+-----------------+----------------------------------+
| answer.50ms     | completed in 50ms                |
+-----------------+----------------------------------+
| answer.100ms    | completed in 100ms               |
+-----------------+----------------------------------+
| answer.250ms    | completed in 250ms               |
+-----------------+----------------------------------+
| answer.500ms    | completed in 500ms               |
+-----------------+----------------------------------+
| answer.1000ms   | completed in 1000ms              |
+-----------------+----------------------------------+
| answer.1500ms   | completed in 1500ms              |
+-----------------+----------------------------------+
| answer.slow     | completed in more than 1500ms    |
+-----------------+----------------------------------+
| answer.sum_ms   | sum of all latencies in ms       |
+-----------------+----------------------------------+

+-----------------+----------------------------------+
| **Answer flags**                                   |
+-----------------+----------------------------------+
| answer.aa       | authoritative answer             |
+-----------------+----------------------------------+
| answer.tc       | truncated answer                 |
+-----------------+----------------------------------+
| answer.ra       | recursion available              |
+-----------------+----------------------------------+
| answer.rd       | recursion desired (in answer!)   |
+-----------------+----------------------------------+
| answer.ad       | authentic data (DNSSEC)          |
+-----------------+----------------------------------+
| answer.cd       | checking disabled (DNSSEC)       |
+-----------------+----------------------------------+
| answer.do       | DNSSEC answer OK                 |
+-----------------+----------------------------------+
| answer.edns0    | EDNS0 present                    |
+-----------------+----------------------------------+

+-----------------+----------------------------------+
| **Query flags**                                    |
+-----------------+----------------------------------+
| query.edns      | queries with EDNS present        |
+-----------------+----------------------------------+
| query.dnssec    | queries with DNSSEC DO=1         |
+-----------------+----------------------------------+

Example:

.. code-block:: none

        modules.load('stats')

	-- Enumerate metrics
	> stats.list()
	[answer.cached] => 486178
	[iterator.tcp] => 490
	[answer.noerror] => 507367
	[answer.total] => 618631
	[iterator.udp] => 102408
	[query.concurrent] => 149

	-- Query metrics by prefix
	> stats.list('iter')
	[iterator.udp] => 105104
	[iterator.tcp] => 490

	-- Fetch most common queries
	> stats.frequent()
	[1] => {
		[type] => 2
		[count] => 4
		[name] => cz.
	}

	-- Fetch most common queries (sorted by frequency)
	> table.sort(stats.frequent(), function (a, b) return a.count > b.count end)

	-- Show recently contacted authoritative servers
	> stats.upstreams()
	[2a01:618:404::1] => {
	    [1] => 26 -- RTT
	}
	[128.241.220.33] => {
	    [1] => 31 - RTT
	}

	-- Set custom metrics from modules
	> stats['filter.match'] = 5
	> stats['filter.match']
	5

Module reference
----------------

.. function:: stats.get(key)

  :param string key: i.e. ``"answer.total"``
  :return: ``number``

Return nominal value of given metric.

.. function:: stats.set('key val')

Set nominal value of given metric.

Example:

.. code-block:: lua

   stats.set('answer.total 5')
   -- or syntactic sugar
   stats['answer.total'] = 5


.. function:: stats.list([prefix])

  :param string prefix:  optional metric prefix, i.e. ``"answer"`` shows only metrics beginning with "answer"

Outputs collected metrics as a JSON dictionary.

.. function:: stats.upstreams()

Outputs a list of recent upstreams and their RTT. It is sorted by time and stored in a ring buffer of
a fixed size. This means it's not aggregated and readable by multiple consumers, but also that
you may lose entries if you don't read quickly enough. The default ring size is 512 entries, and may be overridden on compile time by ``-DUPSTREAMS_COUNT=X``.

.. function:: stats.frequent()

Outputs list of most frequent iterative queries as a JSON array. The queries are sampled probabilistically,
and include subrequests. The list maximum size is 5000 entries, make diffs if you want to track it over time.

.. function:: stats.clear_frequent()

Clear the list of most frequent iterative queries.

.. include:: ../modules/graphite/README.rst
.. include:: ../modules/http/prometheus.rst
