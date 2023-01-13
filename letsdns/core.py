# Copyright © 2022-2023 Ralph Seichter
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
from logging import info
from typing import Optional

from letsdns.action import Action
from letsdns.action import import_action
from letsdns.configuration import Config
from letsdns.hetznerapi import HetznerApiUpdate
from letsdns.liveupdate import DnsLiveUpdate
from letsdns.nsupdate import NsupdateStdout

_ACTION_CLASS_MAP = {
    # Read-only mapping from action name to action class
    'dane-tlsa': DnsLiveUpdate,
    'hetzner-tlsa': HetznerApiUpdate,
    'nsupdate-stdout': NsupdateStdout,
}


def action_class(name: str) -> Optional[Action]:
    """Return action class for the given name.

    Args:
        name: Action name.
    """
    if name in _ACTION_CLASS_MAP:
        _class = _ACTION_CLASS_MAP[name]
    elif name.startswith('dynamic:'):
        _class = import_action(name.split(':')[1])
    else:
        _class = None
    return _class


def traverse_config(conf: Config) -> int:
    """Traverse and process the configuration sections. Return the number of processed actions.

    Args:
        conf: Configuration object.
    """
    counter = 0
    for section in conf.parser.sections():
        conf.active_section = section
        info(f'Config section: {section}')
        name = conf.get('action')
        if name:
            _class = action_class(name)
            if _class:
                description = f' {_class}.lifecycle'
                info(f'Start{description}')
                # noinspection PyCallingNonCallable
                _class.lifecycle(conf, _class())
                info(f'End{description}')
                counter += 1
    return counter
