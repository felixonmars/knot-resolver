.. SPDX-License-Identifier: GPL-3.0-or-later

********************************
Logging, monitoring, diagnostics
********************************

To read service logs use commands usual for your distribution.
E.g. on distributions using systemd-journald use command ``journalctl -eu knot-resolver``.

.. option:: logging:

   .. option:: level: crit|err|warning|notice|info|debug

      :default: notice

      Logging level ``notice`` is set after start by default,
      so logs from Knot Resolver should contain only couple lines a day.
      For debugging purposes it is possible to use the very verbose ``debug`` level,
      but that is generally not usable unless restricted in some way (see below).

      Toggle between ``debug`` and ``notice`` log level. Use only for debugging purposes.
      On busy systems verbose logging can produce several MB of logs per
      second and will slow down operation.

      In addition to levels, logging is also divided into the groups.

   .. option:: groups: <list of logging groups>

      Use to turn-on ``debug`` logging for the selected :ref:`groups <config_log_groups>` regardless of the global log level.
      Other groups are logged to the log based on the initial level.

      .. code-block:: yaml

         logging:
           level: notice  # other groups are logged based on this level
           groups: [manager, cache]  # enable debug logging level for manager and cache group

      .. It is also possible to enable ``debug`` logging level for particular requests,
      .. with :ref:`policies <mod-policy-logging>` or as :ref:`an HTTP service <mod-http-trace>`.

      Less verbose logging for DNSSEC validation errors can be enabled by using :ref:`config-logging-bogus` module.

   .. option:: target: syslog|stderr|stdout

      Knot Resolver logs to standard error stream by default, but typical systemd units change that to ``'syslog'``.
      That setting logs directly through systemd's facilities (if available) to preserve more meta-data.
      Do not edit if you do not know what you are doing.

Various statistics for monitoring purposes are available in :ref:`config-monitoring-stats`, including export to central systems like Graphite, Metronome, InfluxDB, or Prometheus format.

Additional monitoring and debugging methods are described below. If none of these options fits your deployment or if you have special needs you can configure your own checks and exports using :ref:`async-events`.

.. toctree::
   :maxdepth: 1

   config-logging-bogus
   config-monitoring-stats
   config-nsid
   config-logging-dnstap
   config-ta-sentinel
   config-ta-signal-query
   config-time-skew-detection
   config-time-jump-detection
   config-logging-debugging
