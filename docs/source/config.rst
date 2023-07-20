Configuration
=============

Configuration data is specified using ``name = value`` pairs in INI-style text files. A detailed syntax_ description is
available at Python.org. Please note that LetsDNS uses `extended interpolation`_ of values, and that entries in the
[DEFAULT] configuration section are inherited by all other sections.

.. _BIND 9: https://bind9.readthedocs.io/en/latest/
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


  LetsDNS "acts" on all all configuration sections which define an action.
  This is the reason why I recommend **not** defining actions in the [DEFAULT]
  section, unless it is the only section in your configuration set.

  The following action identifiers are available:

  - dane-tlsa

    Create DANE TLSA records using the DNS Update protocol (see `RFC 2136`_).
    If your nameserver is running on the same machine as LetsDNS, or if it is
    accessible over a network connection, using this action is the recommend
    and most convenient way to publish DNS records.

  - dynamic:*module.containing.YourActionClass*

    Import and execute a `dynamic action`_ at runtime. Unless you are faced with
    an untypical or advanced use case, you probably won't need this.

  - hetzner-tlsa

    Create DANE TLSA records using the `Hetzner DNS API`_. This action requires
    an API token for write access.

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

  Note that LetsDNS automatically deduplicates TLSA records, which implies
  that the number of records created may be lower than the number of
  cert_ID_path entries in your configuration.

- domain = *example.com*

  Fully qualified name of the domain or subdomain to be operated on.

- hostname = *somehost | .*

  Either a hostname without domain, or a single dot character. The latter
  denotes the domain apex.

- keyfile = */path/to/key.json*

  JSON file containing the TSIG keys required for DNS access. The file must
  contain a {"textual-dns-name": "base64-encoded-secret"} pair. For example,
  if your `BIND 9`_ nameserver permits access via
  ``key "mykey" { algorithm hmac-sha256; secret "c2VjcmV0Cg=="; };``
  the matching JSON content is ``{"mykey": "c2VjcmV0Cg=="}``.

- keyalgorithm = *hmac-sha256*

  If keyfile is set define which key algorithm the TSIG key uses

- nameserver = *hostname | ip-address*

  Host name or IP address for your nameserver. Name resolution is
  delegated to your OS.

- tcp_ports = *port [port [...]]*

  List of TCP service port numbers in the range 1-65535, separated with spaces
  or commas, for which TLSA records should be generated. Default: 25. Different
  ports can be used for other services, i.e. port 443 for HTTPS.

- ttl = *seconds*

  DNS record time-to-live, in seconds. Default: 1800. Values of more than one
  hour may cause issues due to prolonged caching, depending on your roll-over
  strategy for certificates.
