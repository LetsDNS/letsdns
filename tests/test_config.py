# Copyright © 2022-2025 Ralph Seichter
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
import filecmp
import logging
import os
from configparser import NoOptionError
from tempfile import NamedTemporaryFile

import tests
from letsdns.configuration import Config
from letsdns.configuration import log_level


class ConfigurationTest(tests.TestCase):
    def test_loglevel_bad(self):
        os.environ['LOG_LEVEL'] = 'BAD'
        with self.assertRaises(AttributeError):
            log_level()

    def test_loglevel_good(self):
        os.environ['LOG_LEVEL'] = 'FATAL'
        self.assertEqual(logging.FATAL, log_level())

    def test_dump(self):
        c = Config()
        c.init()
        f = NamedTemporaryFile(mode='wt', delete=False)
        c.dump(f)
        f.close()
        p = os.path.join(os.path.dirname(__file__), 'dump-expected')
        x = filecmp.cmp(p, f.name, shallow=False)
        os.unlink(f.name)
        self.assertTrue(x, msg='Dumped content differs')

    def test_get_domain(self):
        self.c.active_section = 'DEFAULT'
        with self.assertRaises(NoOptionError):
            self.c.get_domain()

    def test_options(self):
        self.c.active_section = 'tlsa'
        self.assertGreater(len(self.c.options()), 5)
