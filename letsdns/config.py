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


class Configuration:
    """Provide access to configuration data."""
    parser: ConfigParser
    active_section: str  # The currently active configuration section

    def __init__(self, parser: ConfigParser) -> None:
        """Create configuration object.

        :param parser: Configuration parser.
        """
        super().__init__()
        self.parser = parser

    def get(self, name: str, fallback=None) -> str:
        """Return an optional configuration value or the specified fallback value.

        :param name: Option name.
        :param fallback: Returned if option is undefined.
        """
        return self.parser.get(self.active_section, name, fallback=fallback)

    def get_mandatory(self, name: str) -> str:
        """Return a mandatory configuration value.

        Raise an exception if option value is undefined.

        :param name: Option name.
        """
        return self.parser.get(self.active_section, name)

    def get_domain(self) -> str:
        """Return the mandatory 'domain' configuration value.

        Raise an exception if 'domain' is undefined.
        """
        return self.get_mandatory('domain')

    def dump(self, destination=sys.stdout) -> None:
        """Dump configuration state into a file.

        :param destination: File pointer.
        """
        self.parser.write(destination)


def from_files(filenames) -> Configuration:
    """Read configuration files.

    :param filenames: String or list of strings.
    """
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read_dict({'DEFAULT': {'nameserver': '127.0.0.1'}})
    parser.read(filenames, encoding='utf-8')
    return Configuration(parser)
