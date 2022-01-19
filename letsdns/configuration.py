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
import sys
from configparser import ConfigParser
from configparser import ExtendedInterpolation
from typing import List


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

    def init(self, filenames) -> None:
        """Initialise object by loading configuration files from disk.
        Nonexisting or unreadable files are silently ignored.

        Args:
            filenames: Either a single string or a list of strings.
        """
        self.parser = ConfigParser(interpolation=ExtendedInterpolation())
        self.parser.read_dict({'DEFAULT': {'nameserver': '127.0.0.1'}})
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
        return self.parser.get(self.active_section, name)

    def get_domain(self) -> str:
        """Return the mandatory 'domain' configuration value.

        Raise an exception if 'domain' is undefined.
        """
        return self.get_mandatory('domain')

    def options(self) -> List[str]:
        """Return all options in the active section."""
        return self.parser.options(self.active_section)
