Configuration options
=====================

Configuration data is specified using ``name = value`` pairs in
INI-style text files. The option names/values listed below have
special semantics.

You can define any additional options you wish, but take care when
choosing names. To avoid naming clashes with future LetsDNS versions,
I suggest you prefix your own options with ``x_`` or ``x-`` (the
upper- or lowercase letter X followed by underscore or dash). LetsDNS
will never assign special meaning to options named with these
prefixes.

- action = *identifier*

  One of the following identifiers must be specified:

  - tlsa

    Create a TLSA records for the certificates defined in a
    configuration section.

- cert_XYZ_path = */path/to/cert.pem*

  Path to certificate *XYZ*. You can replace *XYZ* with any
  combination of numbers and letters. By varying *XYZ*, you can
  define as many certificates as you need, limited only by available
  disk space and memory.

- cert_XYZ_record = *usage-selector-type*

  Certificate usage, TLSA selector and TLSA matching type. See `RFC
  7671`_. Dashes will be replaced with spaces, so an input of
  ``3-1-1`` will result in "... TLSA 3 1 1 ...". The *XYZ*
  placeholder ties certificate records and paths together.

.. _RFC 7671: https://datatracker.ietf.org/doc/html/rfc7671

- domain = *example.com*

  Fully qualified name of the domain or subdomain to be operated on.

- keyfile = */path/to/key.json*

  JSON file containing the TSIG keys required for DNS access.

- nameserver = *hostname | ip-address*

  Hostname or IP address for your nameserver. LetsDNS will perform a
  DNS lookup if necessary.

- ttl = *seconds*

  DNS record time-to-live, in seconds.
