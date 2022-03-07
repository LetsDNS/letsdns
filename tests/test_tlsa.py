# Copyright © 2022 Ralph Seichter
#
# This file is part of LetsDNS.
#
# LetsDNS is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# LetsDNS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with LetsDNS.
# If not, see <https://www.gnu.org/licenses/>.
import socket
import struct
from unittest import skipUnless

from cryptography.x509 import BasicConstraints
from cryptography.x509 import Certificate
from dns.rdata import from_text
from dns.rdataclass import RdataClass
from dns.rdataset import Rdataset
from dns.rdatatype import RdataType

import tests
from letsdns.crypto import dane_tlsa_records
from letsdns.crypto import read_x509_cert
from letsdns.liveupdate import DnsLiveUpdate
from letsdns.tlsa import dane_tlsa
from tests import ENABLE_DEVELOPER_TESTS
from tests import ENABLE_ONLINE_TESTS


class Test(tests.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.update = DnsLiveUpdate()

    @classmethod
    @skipUnless(ENABLE_ONLINE_TESTS, 'online tests disabled')
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        ds = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=3)
        u = DnsLiveUpdate()
        u.execute(cls.c, name='_25._tcp', dataset=ds)
        u.execute(cls.c, name='test', dataset=ds)

    @skipUnless(ENABLE_ONLINE_TESTS, 'online tests disabled')
    def test_update_dns(self):
        self.c.active_section = 'tlsa'
        rd = from_text(RdataClass.IN, RdataType.TLSA, tok='3 1 1 1234')
        ds = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=3)
        ds.add(rd)
        id_ = self.update.execute(self.c, name='test', dataset=ds)
        self.assertGreater(id_, 0)

    @skipUnless(ENABLE_ONLINE_TESTS, 'online tests disabled')
    def test_bad_ttl(self):
        self.c.active_section = 'bad_ttl'
        rd = from_text(RdataClass.IN, RdataType.TLSA, tok='2 0 1 abcd')
        ds = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=-3)
        ds.add(rd)
        with self.assertRaises(struct.error):
            self.update.execute(self.c, name='test', dataset=ds)

    def test_bad_nameserver(self):
        self.c.active_section = 'bad_ns'
        with self.assertRaises(socket.gaierror):
            self.update.execute(self.c, name='test', dataset=Rdataset(RdataClass.IN, RdataType.TLSA, ttl=3))


@skipUnless(ENABLE_DEVELOPER_TESTS, 'developer tests disabled')
class CertTest(tests.TestCase):
    def _cert(self, name: str) -> Certificate:
        self.c.active_section = 'dane'
        return read_x509_cert(self.c.get_mandatory(name))

    def test_ca_cert(self):
        c = self._cert('cert_ca_path')
        b: BasicConstraints = c.extensions.get_extension_for_class(BasicConstraints).value
        self.assertTrue(b.ca)

    def test_ca_dane(self):
        c = self._cert('cert_ca_path')
        d = dane_tlsa_records(c)
        self.assertEqual('2 1 1 ', d[0][:6])

    def test_leaf_cert(self):
        c = self._cert('cert_leaf_path')
        b: BasicConstraints = c.extensions.get_extension_for_class(BasicConstraints).value
        self.assertFalse(b.ca)

    def test_leaf_dane(self):
        c = self._cert('cert_leaf_path')
        d = dane_tlsa_records(c)
        self.assertEqual('3 1 2 ', d[1][:6])


class ActionTest(tests.TestCase):
    @skipUnless(ENABLE_ONLINE_TESTS, 'online tests disabled')
    def test_tlsa(self):
        self.c.active_section = 'dane'
        dane_tlsa(self.c, DnsLiveUpdate())
