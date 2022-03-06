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
import os.path

from letsdns.action import Action
from letsdns.action import import_action
from letsdns.action import import_class
from letsdns.configuration import Config
from letsdns.liveupdate import DnsLiveUpdate
from letsdns.main import dynamic_action
from letsdns.main import lookup_action
from letsdns.main import traverse_sections
from tests import TestCase
from tests import read_config


class FailPre(Action):
    def pre_execute(self, conf: Config) -> int:
        return -10

    def execute(self, conf: Config, *args, **kwargs) -> int:
        return 0

    def post_execute(self, conf: Config) -> int:
        return 0


class FailExec(Action):
    def pre_execute(self, conf: Config) -> int:
        return 0

    def execute(self, conf: Config, *args, **kwargs) -> int:
        return -20

    def post_execute(self, conf: Config) -> int:
        return 0


class FailPost(Action):
    def pre_execute(self, conf: Config) -> int:
        return 0

    def execute(self, conf: Config, *args, **kwargs) -> int:
        return 0

    def post_execute(self, conf: Config) -> int:
        return -30


class ImportTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        ImportTest.c = read_config(path=os.path.join(os.path.dirname(__file__), 'actiontest.conf'))

    def test_import_missing_class(self):
        with self.assertRaises(ModuleNotFoundError):
            import_class('BAD.CLASS')

    def test_import_not_an_action(self):
        with self.assertRaises(TypeError):
            import_action('tests.actions.NotAnAction')

    def test_lookup_action(self):
        _callable, _class = lookup_action('dane-tlsa')
        self.assertIsNotNone(_callable)
        self.assertTrue(_class == DnsLiveUpdate)

    def test_unknown_action(self):
        _callable, _class = lookup_action('BAD')
        self.assertIsNone(_callable)
        self.assertIsNone(_class)

    def test_callable(self):
        _callable, _class = lookup_action('dynamic:tests.actions.AnAction')
        self.assertIsNotNone(_callable)
        self.assertIsNotNone(_class)
        _callable(self.c, _class())

    def test_fail_pre(self):
        self.assertEqual(-10, dynamic_action(self.c, FailPre()))

    def test_fail_exec(self):
        self.assertEqual(-20, dynamic_action(self.c, FailExec()))

    def test_fail_post(self):
        self.assertEqual(-30, dynamic_action(self.c, FailPost()))

    def test_traverse(self):
        self.assertEqual(1, traverse_sections(self.c))
