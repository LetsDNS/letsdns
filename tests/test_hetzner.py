# Copyright © 2022-2023 Ralph Seichter
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
from unittest import skipUnless

from letsdns.hetznerapi import HetznerApiUpdate
from tests import ENABLE_HETZNER_API_TESTS
from tests import TestCase


class HetznerUpdateTest(TestCase):
    @skipUnless(ENABLE_HETZNER_API_TESTS, 'Hetzner API tests disabled')
    def test_lifecycle(self):
        self.c.active_section = 'hetzner'
        rc = HetznerApiUpdate.lifecycle(self.c, HetznerApiUpdate())
        self.assertEqual(0, rc)

    def test_empty_records(self):
        rc = HetznerApiUpdate().execute(self.c, records=[])
        self.assertEqual(0, rc)
