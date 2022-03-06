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
from letsdns.action import import_action
from letsdns.action import import_class
from tests import TestCase


class ImportTest(TestCase):
    def test_import_missing_class(self):
        with self.assertRaises(ModuleNotFoundError):
            import_class('BAD.CLASS')

    def test_import_not_an_action(self):
        with self.assertRaises(TypeError):
            import_action('tests.actions.NotAnAction')

    def test_import_action(self):
        self.assertIsNotNone(import_action('tests.actions.AnAction'))
