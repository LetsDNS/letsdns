Configuration
=============

Configuration data is specified using ``name = value`` pairs in
INI-style text files. A detailed syntax_ description is available at
Python.org. Please note that LetsDNS uses `extended interpolation`_ of
values.

.. _syntax: https://docs.python.org/3/library/configparser.html#supported-ini-file-structure
.. _extended interpolation: https://docs.python.org/3/library/configparser.html#interpolation-of-values

The option names and values listed below have specific semantics. You
can define custom options, but do take care when choosing names. To
avoid clashes, please prefix your custom options with ``x_`` or ``x-``
(i.e., an upper- or lowercase letter *X* followed by an underscore or
horizontal dash).

- action = *identifier*

  One of the following identifiers must be specified:

  - dane-tlsa

    Create DANE TLSA records for the certificates defined in a
    configuration section.

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

- ttl = *seconds*

  DNS record time-to-live, in seconds.
