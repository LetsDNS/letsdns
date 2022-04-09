Example configuration
=====================

The following example assumes a mail exchanger host *mx.example.com* with a certificate issued by `Let's Encrypt`_.
There is an active TLS certificate which is currently being used by Postfix, and a queued/incoming certificate which has
been acquired using `dehydrated`_.

.. _dehydrated: https://dehydrated.io
.. _Let's Encrypt: https://letsencrypt.org

.. literalinclude:: _static/example.conf
