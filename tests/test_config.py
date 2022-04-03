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
import logging
import os
import subprocess
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
        conf = Config()
        conf.init()
        f = NamedTemporaryFile(mode='wt', delete=False)
        conf.dump(f)
        f.close()
        diff = subprocess.run(['diff', 'dump-expected', f.name])
        os.unlink(f.name)
        self.assertEqual(0, diff.returncode)

    def test_get_domain(self):
        self.c.active_section = 'DEFAULT'
        with self.assertRaises(NoOptionError):
            self.c.get_domain()

    def test_options(self):
        self.c.active_section = 'tlsa'
        self.assertGreater(len(self.c.options()), 5)
