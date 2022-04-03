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
from unittest import skipUnless

from letsdns.action import Action
from letsdns.action import import_action
from letsdns.action import import_class
from letsdns.configuration import Config
from letsdns.core import action_class
from letsdns.core import traverse_config
from letsdns.liveupdate import DnsLiveUpdate
from letsdns.nsupdate import NsupdateStdout
from tests import ENABLE_LIVEUPDATE_TESTS
from tests import TestCase
from tests import read_config


class FailPre(Action):
    def setup(self, conf: Config) -> int:
        return -10

    def execute(self, conf: Config, *args, **kwargs) -> int:
        return 0

    def teardown(self, conf: Config) -> int:
        return 0


class FailExec(Action):
    def setup(self, conf: Config) -> int:
        return 0

    def execute(self, conf: Config, *args, **kwargs) -> int:
        return -20

    def teardown(self, conf: Config) -> int:
        return 0


class FailPost(Action):
    def setup(self, conf: Config) -> int:
        return 0

    def execute(self, conf: Config, *args, **kwargs) -> int:
        return 0

    def teardown(self, conf: Config) -> int:
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
        self.assertTrue(action_class('dane-tlsa') == DnsLiveUpdate)

    def test_unknown_action(self):
        self.assertIsNone(action_class('BAD'))

    def test_callable(self):
        self.assertIsNotNone(action_class('dynamic:tests.actions.AnAction'))

    def test_fail_pre(self):
        a = FailPre()
        self.assertEqual(-10, a.lifecycle(self.c, a))

    def test_fail_exec(self):
        a = FailExec()
        self.assertEqual(-20, a.lifecycle(self.c, a))

    def test_fail_post(self):
        a = FailPost()
        self.assertEqual(-30, a.lifecycle(self.c, a))

    def test_traverse(self):
        self.assertEqual(1, traverse_config(self.c))


class LiveUpdateTest(TestCase):
    @skipUnless(ENABLE_LIVEUPDATE_TESTS, 'online tests disabled')
    def test_lifecycle(self):
        self.c.active_section = 'dane'
        rc = DnsLiveUpdate.lifecycle(self.c, DnsLiveUpdate())
        self.assertEqual(0, rc)


class NsupdateTest(TestCase):
    def test_lifecycle(self):
        self.c.active_section = 'dane'
        rc = NsupdateStdout.lifecycle(self.c, NsupdateStdout())
        self.assertEqual(0, rc)
