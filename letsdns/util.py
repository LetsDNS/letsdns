# Copyright © 2022-2026 Ralph Seichter
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
import os
import re
from logging import debug
from typing import List

_SENSITIVE_RE = re.compile(r'key|pass|token', re.IGNORECASE)


def is_sensitive(name: str) -> bool:
    """Return True if the specified name is considered sensitive."""
    return _SENSITIVE_RE.search(name) is not None


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


def getenv(name: str, default=None, debug_env=True):
    """Return environment variable value if available, otherwise return the default value.

    Args:
        name: Environment variable name.
        default: Default value.
        debug_env: Debug variable name/value.
    """
    if name in os.environ:
        value = os.environ[name]
    else:
        value = default
    if debug_env:
        if is_sensitive(name):
            debug(f'ENV {name}=*****')
        else:
            debug(f'ENV {name}={value}')
    return value


def split(source: str) -> List[str]:
    """Split a string where whitespace or comma occurs. Return empty list for invalid input.

    Args:
        source: The string to be split.
    """
    strings = []
    if source:
        for s in source.replace(',', ' ').split(' '):
            strings.append(s.strip())
    return list(filter(lambda x: x, strings))
