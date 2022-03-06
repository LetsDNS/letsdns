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
import unittest
from os import environ

from letsdns.configuration import Config
from letsdns.main import init_logger

UNITTEST_CONF = 'UNITTEST_CONF'


def read_config(path: str = UNITTEST_CONF, active_section: str = 'DEFAULT') -> Config:
    if path == UNITTEST_CONF:
        path = environ.get(path)
        if path is None:  # pragma: no cover
            raise ValueError(f'Missing environment variable {UNITTEST_CONF}')
    conf = Config()
    conf.init(path)
    conf.active_section = active_section
    return conf


class TestCase(unittest.TestCase):
    c: Config

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        init_logger()
        TestCase.c = read_config()
