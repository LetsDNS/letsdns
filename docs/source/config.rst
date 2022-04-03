Configuration
=============

Configuration data is specified using ``name = value`` pairs in
INI-style text files. A detailed syntax_ description is available at
Python.org. Please note that LetsDNS uses `extended interpolation`_ of
values.

.. _dynamic action: dynaction.html
.. _extended interpolation: https://docs.python.org/3/library/configparser.html#interpolation-of-values
.. _Hetzner DNS API: https://dns.hetzner.com/api-docs
.. _nsupdate: https://linux.die.net/man/1/nsupdate
.. _RFC 2136: https://datatracker.ietf.org/doc/html/rfc2136.html
.. _syntax: https://docs.python.org/3/library/configparser.html#supported-ini-file-structure

The option names and values listed below have specific semantics. You
can define custom options, but do take care when choosing names. To
avoid clashes, please prefix your custom options with ``x_`` or ``x-``
(i.e., an upper- or lowercase letter *X* followed by an underscore or
horizontal dash).

- action = *identifier*

  One of the following identifiers must be specified:

  - dane-tlsa

    Create DANE TLSA records using the DNS Update protocol (see `RFC 2136`_).

  - dynamic:*module.containing.YourActionClass*

    Import and execute a `dynamic action`_ at runtime.

  - hetzner-tlsa

    Create DANE TLSA records using the `Hetzner DNS API`_.

  - nsupdate-stdout

    Print `nsupdate`_ commands for generating DANE TLSA records to stdout.

- api_token = *string*

  API access token. Required when using the *hetzner-tlsa* action.

- api_url = *URL*

  Optional URL for the Hetzner DNS API (default: https://dns.hetzner.com/api/v1)

- cert_ID_path = */path/to/cert.pem*

  Path to a x509 certificate. Replace *ID* with any unique combination
  of numbers and letters. By varying *ID*, you can define as many
  certificates as you need, limited only by available disk space and
  memory.

- domain = *example.com*

  Fully qualified name of the domain or subdomain to be operated on.

- hostname = *somehost*

  Short hostname without domain. Required for the *dane-tlsa* action.

- keyfile = */path/to/key.json*

  JSON file containing the TSIG keys required for DNS access.

- nameserver = *hostname | ip-address*

  Host name or IP address for your nameserver. Name resolution is
  delegated to your OS.

- tcp_ports = *port [...]*

  List of TCP service port numbers in the range 1-65535, separated with spaces
  or commas, for which TLSA records should be generated. Default: 25.

- ttl = *seconds*

  DNS record time-to-live, in seconds.
