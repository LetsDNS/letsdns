Configuration options
=====================

Configuration data is specified using ``name = value`` pairs in INI-style text files.
The following option names/values are supported:

- action = *single-value*

  One of the following values must be specified:

  - foo

    Do the foo.

  - tlsa

    Create a TLSA 3 1 1 record.

- domain = *example.com*

  Fully qualified name of the domain or subdomain to be operated on.

- keyfile = */path/to/key.json*

  JSON file containing the TSIG keys required for DNS access.

- nameserver = *ip-address*

  The nameserver's IP address, e.g. ``111.222.333.444``. Host names cannot be used here.

- ttl = *seconds*

  DNS record time-to-live, in seconds.
