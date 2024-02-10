# Copyright © 2022-2024 Ralph Seichter
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
from logging import debug

from letsdns.action import Action
from letsdns.configuration import Config


class AnAction(Action):
    def setup(self, conf: Config) -> int:
        r = super().setup(conf)
        debug('AnAction.setup')
        return r

    def execute(self, conf: Config, *args, **kwargs) -> int:
        return 0


class NotAnAction:
    def foo(self):
        pass
