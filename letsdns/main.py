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
import json
import sys
from argparse import ArgumentParser

import dns.query
import dns.tsigkeyring
from dns.rdatatype import MX
from dns.rdatatype import TLSA
from dns.rdatatype import TXT
from dns.resolver import resolve
from dns.update import Update
from dns.update import UpdateMessage

from letsdns import HOMEPAGE
from letsdns import IDENTIFIER
from letsdns import VERSION
from letsdns import config
from letsdns.config import Configuration
from letsdns.crypt import read_x509_cert
from letsdns.crypt import tlsa_data


def show_mx(domain: str) -> None:
    answers = resolve(domain, 'MX')
    a: MX
    for a in answers:
        print(f'{a.exchange} has preference {a.preference}')


def show_tlsa(domain: str) -> None:
    answers = resolve(f'letsdns_tlsa._acme-challenge.{domain}', 'TLSA')
    a: TLSA
    for a in answers:
        t: str = a.to_text()
        print(t)


def show_txt(domain: str) -> None:
    answers = resolve(domain, 'TXT')
    a: TXT
    for a in answers:
        t: str = a.to_text()
        print(t)


def update_dns(conf: Configuration, name: str, record_type: str, record_data: str) -> None:
    """Update DNS record.

    :param conf: Configuration object
    :param name: Record name
    :param record_type: Record type (e.g. A, TLSA, etc.)
    :param record_data: Record data string
    """
    domain = conf.get_mandatory('domain')
    keyfile = conf.get_mandatory('keyfile')
    ttl = int(conf.get_mandatory('ttl'))
    with open(keyfile, 'r') as f:
        obj = json.load(f)
        keyring = dns.tsigkeyring.from_text(obj)
        update = Update(f'_acme-challenge.{domain}', keyring=keyring)
        update.replace(name, ttl, record_type, record_data)
        nameserver = conf.get_mandatory('nameserver')
        r: UpdateMessage = dns.query.tcp(update, nameserver, timeout=5)
        print(r)


def update_tlsa(conf: Configuration) -> None:
    """Update TLSA record."""
    filename = conf.get_mandatory('certificate')
    certificate = read_x509_cert(filename)
    data = tlsa_data(certificate)
    update_dns(conf, 'letsdns_tlsa', 'TLSA', data)


def traverse_sections(conf: Configuration) -> None:
    """Traverse the sections of a configuration object.

    If sections define an 'action' option, process accordingly.
    """
    for section in conf.parser.sections():
        conf.active_section = section
        print(section)
        action = conf.get('action')
        if 'tlsa' == action:
            update_tlsa(conf)
        elif action:
            print(f'Ignoring unknown action: {action}')


if __name__ == '__main__':
    """Entry point."""
    parser = ArgumentParser(
        description=f'LetsDNS {VERSION} - Manage DANE TLSA records in DNS servers.',
        epilog=f'See {HOMEPAGE} for more information.',
        fromfile_prefix_chars='@',
        prog=IDENTIFIER,
    )
    parser.add_argument('--showconfig', action='store_true', help='print effective configuration to stdout')
    parser.add_argument('configfile', type=str, nargs='+')
    args = parser.parse_args()
    conf_global = config.from_files(args.configfile)
    if args.showconfig:
        print(conf_global.parser.write(sys.stdout))
    else:
        traverse_sections(conf_global)
