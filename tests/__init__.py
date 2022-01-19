"""
Copyright © 2022 Ralph Seichter

This file is part of LetsDNS.

LetsDNS is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

LetsDNS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License along with LetsDNS.
If not, see <https://www.gnu.org/licenses/>.
"""
from os import environ

from letsdns.configuration import Config


def read_config(active_section: str = 'DEFAULT') -> Config:
    name = 'UNITTEST_CONF'
    path = environ.get(name)
    if path is None:  # pragma: no cover
        raise ValueError(f'Missing environment variable {name}')
    conf = Config()
    conf.init(path)
    conf.active_section = active_section
    return conf
