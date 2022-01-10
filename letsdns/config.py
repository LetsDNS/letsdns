"""
Copyright (c) 2022 Ralph Seichter.

This file is part of LetsDNS.

LetsDNS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

LetsDNS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with LetsDNS. If not, see
<https://www.gnu.org/licenses/>.
"""
from configparser import ConfigParser
from configparser import ExtendedInterpolation

_DEFAULT_CONFIG = {
    'DEFAULT': {
        'domain': 'example.com.',
        'keyfile': '/etc/letsdns/dnskeys.json',
        'nameserver': '127.0.0.1',
    }
}


def from_files(filenames) -> ConfigParser:
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    parser.read_dict(_DEFAULT_CONFIG)
    parser.read(filenames, encoding='utf-8')
    return parser


def get(parser: ConfigParser, option: str, section='DEFAULT'):
    return parser.get(section, option)
