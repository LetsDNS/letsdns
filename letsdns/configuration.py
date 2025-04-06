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
import logging
import sys
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from logging import basicConfig
from logging import debug
from typing import List

from letsdns.util import getenv
from letsdns.util import is_sensitive
from letsdns.util import split

LOG_LEVEL = 'LOG_LEVEL'


def log_level(default: str = 'ERROR') -> int:
    """Return logging level, using the LOG_LEVEL environment variable if available.

    Args:
        default: The default log level.
    """
    return getattr(logging, getenv(LOG_LEVEL, default, debug_env=False).upper())


def init_logger() -> None:
    """Initialise logger."""
    try:
        level = log_level()
        basicConfig(datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)s %(message)s', level=level)
    except AttributeError as e:  # pragma: no cover
        print(e, file=sys.stderr)
        sys.exit(1)


class Config:
    """Provide access to configuration data."""
    parser: ConfigParser
    active_section: str  # The currently active configuration section

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
        if is_sensitive(name):
            debug(f'config: {name} = *****')
        else:
            debug(f'config: {name} = {v}')
        return v

    def get_domain(self) -> str:
        """Return the mandatory 'domain' configuration value.

        Raise an exception if 'domain' is undefined.
        """
        return self.get_mandatory('domain')

    def get_ttl(self) -> int:
        """Return the 'ttl' configuration value (seconds, integer)."""
        return int(self.get('ttl', fallback='1800'))

    def get_tcp_ports(self) -> List[str]:
        """Return the optional 'tcp_ports' configuration value."""
        return split(self.get('tcp_ports', fallback='25'))

    def options(self) -> List[str]:
        """Return all options in the active section."""
        return self.parser.options(self.active_section)
