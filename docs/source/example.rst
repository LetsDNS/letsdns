Example use cases
=================

Mail Exchanger
--------------

The following example assumes a mail exchanger host *mx.example.com* with a certificate issued by `Let's Encrypt`_.
There is an active TLS certificate which is currently being used by Postfix, and a queued/incoming certificate which has
been acquired using `dehydrated`_.

.. _dehydrated: https://dehydrated.io
.. _Let's Encrypt: https://letsencrypt.org

.. literalinclude:: _static/mx.ini

The sequence of events is as follows:

1. A daily cron job runs dehydrated. For this example, assume that the job runs at midnight.

2. If a new certificate is obtained, dehydrated stores ("queues") this certificates in the directory /var/lib/dehydrated/certs/example.com. Using dehydrated's deploy_cert() hook funktion, LetsDNS is then launched with the configuration file shown above.

3. LetsDNS connects to nameserver *ns1.example.com* using the provided keyfile for authentication, and generates TLSA records for both the queued and the currently active certificate, which is located in /etc/postfix/tls. It also generates records for the Let's Encrypt "R3" Certificate Authority.

4. Assuming that the TTL is no longer than an hour, it is safe to either copy or move the queued certificate over the active certificate a day later, and restart Postfix. This can be achieved using another cron job, running daily at 23:45.

With this procedure, obtaining an updated certificate and publishing matching TLSA records happens roughly 24 hours before activating said certificate. Combined with the proper TTL, this gap ensures non-breaking certificate roll-overs, which are further backed by the TLSA records generated for the CA certificate.

Web Server
----------

The second example demonstrates how LetsDNS can be configured to generate TLSA records for both
*https://www.example.com* and for the domain apex *https://example.com*.

.. literalinclude:: _static/www.ini

The procedure for obtaining and activating certificates with the help of cron jobs is identical to what is used in the
Mail Exchanger example, the only difference being that you need to restart your Web Server software instead of Postfix.

This particular configuration demonstrates the use of cross-section referencing for the *action* parameter, which is a
completely optional method but may come in handy.
