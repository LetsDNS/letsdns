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
import logging
import os
import sys
from logging import basicConfig

HOMEPAGE = 'https://www.letsdns.org/'
IDENTIFIER = 'letsdns'
VERSION = '0.1.dev651202'


def init_logger() -> None:
    name = 'LOG_LEVEL'
    try:
        if name in os.environ:
            value = os.environ[name]
            level = getattr(logging, value.upper())
        else:
            level = logging.ERROR
    except AttributeError as e:
        print(f'Unsupported {name} value: {e}', file=sys.stderr)
        sys.exit(1)
    basicConfig(datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s %(levelname)s %(message)s', level=level)
