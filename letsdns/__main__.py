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
from argparse import ArgumentParser
from logging import debug

from letsdns import HOMEPAGE
from letsdns import IDENTIFIER
from letsdns import VERSION
from letsdns.configuration import Config
from letsdns.configuration import init_logger
from letsdns.core import traverse_config


def main():
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
        n = traverse_config(config)
        debug(f'Processed {n} action(s)')


if __name__ == '__main__':
    main()
