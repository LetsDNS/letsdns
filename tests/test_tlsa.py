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
from logging import WARN
from logging import basicConfig
from unittest import TestCase

from letsdns.conf import Config
from letsdns.tlsa import update_dns
from tests import read_config


class Test(TestCase):
    c: Config

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        basicConfig(
            datefmt='%Y-%m-%d %H:%M:%S',
            format='%(asctime)s %(levelname)s %(message)s',
            level=WARN
        )
        Test.c = read_config()

    def test_update_dns(self):
        self.c.active_section = 'tlsa'
        id_ = update_dns(self.c, name='test', record_type='TXT', record_data='test')
        self.assertGreater(id_, 0)

    def test_update_dns_bad_ttl(self):
        self.c.active_section = 'bad_ttl'
        with self.assertRaises(ValueError):
            update_dns(self.c, name='test', record_type='TXT', record_data='test')

    def test_update_dns_bad_ns(self):
        self.c.active_section = 'bad_ns'
        with self.assertRaises(socket.gaierror):
            update_dns(self.c, name='test', record_type='TXT', record_data='test')
