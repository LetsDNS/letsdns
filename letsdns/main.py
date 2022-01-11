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
from configparser import ConfigParser

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
from letsdns.crypt import read_x509_cert


def show_mx():
    answers = resolve(domain, 'MX')
    a: MX
    for a in answers:
        print(f'{a.exchange} has preference {a.preference}')


def show_tlsa():
    answers = resolve(f'letsdns_tlsa._acme-challenge.{domain}', 'TLSA')
    a: TLSA
    for a in answers:
        t: str = a.to_text()
        print(t)


def show_txt():
    answers = resolve(domain, 'TXT')
    a: TXT
    for a in answers:
        t: str = a.to_text()
        print(t)


def update_dyn(conf: ConfigParser):
    keyfile = config.get(conf, 'keyfile')
    with open(keyfile, 'r') as f:
        obj = json.load(f)
        keyring = dns.tsigkeyring.from_text(obj)
        update = Update(f'_acme-challenge.{domain}', keyring=keyring)
        update.replace('letsdns_tlsa', 3, 'TLSA',
                       '3 0 1 07ce6be3d50e07c8f8a6a6562a4d0e85bb0e62ceda1501600e2d4df148ac9b68')
        nameserver = config.get(conf, 'nameserver')
        r: UpdateMessage = dns.query.tcp(update, nameserver, timeout=5)
        print(r)


if __name__ == '__main__':
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
        print(conf_global.write(sys.stdout))
    else:
        domain = conf_global.get('DEFAULT', 'domain')
        print(domain)
        read_x509_cert('local/cert.pem')
        # update_dyn(conf_global)
        # show_tlsa()
