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
from argparse import ArgumentParser
from logging import info
from logging import warning

from letsdns import HOMEPAGE
from letsdns import IDENTIFIER
from letsdns import VERSION
from letsdns import init_logger
from letsdns.action import dynamic_action
from letsdns.action import import_action
from letsdns.configuration import Config
from letsdns.liveupdate import DnsLiveUpdate
from letsdns.nsupdate import NsupdateStdout
from letsdns.tlsa import action_dane_tlsa


def lookup_action(name: str):
    """Lookup a callable (method) and an action class.

    Returns None,None if no mapping was found.
    """
    action_map = {
        'dane-tlsa': [action_dane_tlsa, DnsLiveUpdate],
        'nsupdate-stdout': [action_dane_tlsa, NsupdateStdout],
    }
    if name in action_map:
        return action_map[name][0], action_map[name][1]
    elif name.startswith('dynamic:'):
        name = name.split(':')[1]
        action_class = import_action(name)
        return dynamic_action, action_class
    warning(f'Unknown action: {name}')
    return None, None


def traverse_sections(conf: Config) -> int:
    """Traverse the sections of a configuration object and return the number of actions found.

    If sections define an 'action' option, process accordingly.
    """
    action_count = 0
    for section in conf.parser.sections():
        conf.active_section = section
        info(f'Config section: {section}')
        action = conf.get('action')
        if action:
            action_count += 1
            _callable, _class = lookup_action(action)
            if _callable and _class:
                description = f' {action} {_callable} {_class}'
                info(f'Start{description}')
                _callable(conf, _class())
                info(f'End{description}')
    return action_count


if __name__ == '__main__':
    init_logger()
    parser = ArgumentParser(
        description=f'LetsDNS {VERSION} - Manage DANE TLSA records in DNS servers.',
        epilog=f'See {HOMEPAGE} for more information.',
        fromfile_prefix_chars='@',
        prog=IDENTIFIER,
    )
    parser.add_argument('--showconfig', action='store_true', help='print effective configuration to stdout')
    parser.add_argument('configfile', type=str, nargs='+')
    args = parser.parse_args()
    config = Config()
    config.init(args.configfile)
    if args.showconfig:
        config.dump()
    else:
        traverse_sections(config)
