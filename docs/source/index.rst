.. LetsDNS documentation master file

Welcome to LetsDNS
==================

Manage DANE TLSA records in DNS servers. Supports multiple domains with multiple TLS certificates each.  LetsDNS can be
invoked manually, from a periodic cron job, or called in the *deploy_cert()* hook function of `dehydrated`_, or from a
`certbot`_ hook.

.. _certbot: https://eff-certbot.readthedocs.io
.. _dehydrated: https://dehydrated.io
.. _GitHub: https://github.com/LetsDNS/letsdns

Copyright © 2022 Ralph Seichter. Hosted on `GitHub`_.

.. toctree::
    :maxdepth: 3

    example
    install
    config
    operation
    envvar
    dynaction

    contrib
    license

    letsdns


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
