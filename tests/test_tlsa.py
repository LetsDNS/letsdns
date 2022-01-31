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
import os
import socket
import struct
from unittest import skipUnless

from dns.rdata import from_text
from dns.rdataclass import RdataClass
from dns.rdataset import Rdataset
from dns.rdatatype import RdataType

import tests
from letsdns.configuration import is_truthy
from letsdns.tlsa import update_dns

ENABLE_ONLINE_TESTS = is_truthy(os.environ.get('ENABLE_ONLINE_TESTS'))


class Test(tests.TestCase):
    @skipUnless(ENABLE_ONLINE_TESTS, 'online tests disabled')
    def test_update_dns(self):
        self.c.active_section = 'tlsa'
        rd = from_text(RdataClass.IN, RdataType.TLSA, tok='3 1 1 1234')
        ds = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=3)
        ds.add(rd)
        id_ = update_dns(self.c, name='test', dataset=ds)
        self.assertGreater(id_, 0)

    def test_bad_ttl(self):
        self.c.active_section = 'bad_ttl'
        rd = from_text(RdataClass.IN, RdataType.TLSA, tok='2 0 1 abcd')
        ds = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=-3)
        ds.add(rd)
        with self.assertRaises(struct.error):
            update_dns(self.c, name='test', dataset=ds)

    def test_bad_nameserver(self):
        self.c.active_section = 'bad_ns'
        with self.assertRaises(socket.gaierror):
            update_dns(self.c, name='test', dataset=Rdataset(RdataClass.IN, RdataType.TLSA, ttl=3))
