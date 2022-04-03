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
import re
import sys
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from logging import basicConfig
from logging import debug
from typing import List

from letsdns.util import getenv

LOG_LEVEL = 'LOG_LEVEL'


def log_level(default: str = 'ERROR') -> int:
    """Return logging level, using the LOG_LEVEL environment variable if available.

    Args:
        default: The default log level.
    """
    return getattr(logging, getenv(LOG_LEVEL, default, debug=False).upper())


def init_logger() -> None:
    """Initialise logger."""
    try:
        level = log_level()
        basicConfig(datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)s %(message)s', level=level)
    except AttributeError as e:  # pragma: no cover
        print(e, file=sys.stderr)
        sys.exit(1)


def is_truthy(something) -> bool:
    """Test if 'something' represents boolean True.

    An object represents True if it is (or can be converted to) a string and said
    string's first character, converted to lowercase, is one of: 1, t, y.

    Args:
        something: The object to examine.
    """
    if not something:
        return False
    if isinstance(something, str):
        s = something
    else:
        s = str(something)
    f = s[:1].lower()
    t = '1ty'.find(f)
    return t >= 0


class Config:
    """Provide access to configuration data."""
    parser: ConfigParser
    active_section: str  # The currently active configuration section
    sensitive_name_re = re.compile(r'key|password|token', re.IGNORECASE)

    def dump(self, destination=sys.stdout) -> None:
        """Dump configuration state into a file.

        Args:
            destination: File pointer.
        """
        self.parser.write(destination)

    def init(self, filenames=None) -> None:
        """Initialise object by loading configuration files from disk.
        Nonexisting or unreadable files are silently ignored.

        Args:
            filenames: Either a single string or a list of strings.
        """
        self.parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.parser.read_dict({'DEFAULT': {'nameserver': '127.0.0.1'}})
        if filenames:
            self.parser.read(filenames, encoding='utf-8')

    def get(self, name: str, fallback=None) -> str:
        """Return an optional configuration value or the specified fallback value.

        Args:
            name: Option name.
            fallback: Returned if option is undefined.
        """
        return self.parser.get(self.active_section, name, fallback=fallback)

    def get_mandatory(self, name: str) -> str:
        """Return a mandatory configuration value.
        Raise an exception if option value is undefined.

        Args:
            name: Option name.
        """
        v = self.parser.get(self.active_section, name)
        if self.sensitive_name_re.search(name):
            debug(f'config: {name} = *****')
        else:
            debug(f'config: {name} = {v}')
        return v

    def get_domain(self) -> str:
        """Return the mandatory 'domain' configuration value.

        Raise an exception if 'domain' is undefined.
        """
        return self.get_mandatory('domain')

    def options(self) -> List[str]:
        """Return all options in the active section."""
        return self.parser.options(self.active_section)
