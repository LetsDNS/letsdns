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
import logging
import os
import sys
from argparse import ArgumentParser
from logging import basicConfig
from logging import debug
from logging import info
from logging import warning

from dns.rdatatype import MX
from dns.rdatatype import TLSA
from dns.rdatatype import TXT
from dns.resolver import resolve

from letsdns import HOMEPAGE
from letsdns import IDENTIFIER
from letsdns import VERSION
from letsdns.configuration import Config
from letsdns.tlsa import action_dane_tlsa


def show_mx(domain: str) -> None:
    answers = resolve(domain, 'MX')
    a: MX
    for a in answers:
        info(f'{a.exchange} has preference {a.preference}')


def show_tlsa(domain: str) -> None:
    answers = resolve(f'letsdns_tlsa._acme-challenge.{domain}', 'TLSA')
    a: TLSA
    for a in answers:
        t: str = a.to_text()
        info(t)


def show_txt(domain: str) -> None:
    answers = resolve(domain, 'TXT')
    a: TXT
    for a in answers:
        t: str = a.to_text()
        info(t)


def traverse_sections(conf: Config) -> None:
    """Traverse the sections of a configuration object.

    If sections define an 'action' option, process accordingly.
    """
    for section in conf.parser.sections():
        conf.active_section = section
        debug(f'section: {section}')
        action = conf.get('action')
        if 'dane-tlsa' == action:
            debug(f'action: {action}')
            action_dane_tlsa(conf)
        elif action:
            warning(f'Ignoring unknown action: {action}')


def init_logger():
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
