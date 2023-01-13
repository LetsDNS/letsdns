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
import uuid
from os import getenv

import tests
from letsdns.util import is_truthy


class UtilTest(tests.TestCase):
    def test_getenv(self):
        u = uuid.uuid4().hex
        self.assertIsNone(getenv(u))
        self.assertEqual(-12, getenv(u, default=-12))

    def test_sensitive(self):
        u = 'API_TOKEN_' + uuid.uuid4().hex
        self.assertIsNone(getenv(u))

    def test_is_truthy1(self):
        self.assertFalse(is_truthy('false'))

    def test_is_truthy2(self):
        self.assertFalse(is_truthy(None))

    def test_is_truthy3(self):
        self.assertTrue(is_truthy('YES'))

    def test_is_truthy4(self):
        self.assertTrue(is_truthy(1))
