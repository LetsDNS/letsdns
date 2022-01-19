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
import json
import re
import socket
from logging import debug
from logging import error

import dns.query
import dns.tsigkeyring
from dns.update import Update

from letsdns.conf import Config
from letsdns.crypt import dane_tlsa_data
from letsdns.crypt import read_x509_cert


def update_dns(conf: Config, name: str, record_type: str, record_data: str) -> int:
    """Update DNS record.

    Args:
        conf: Config object
        name: Record name
        record_type: Record type (e.g. A, TLSA, etc.)
        record_data: Record data string
    """
    domain = conf.get_mandatory('domain')
    ttl = int(conf.get_mandatory('ttl'))
    keyfile = conf.get('keyfile')
    if keyfile:
        with open(keyfile, 'r') as f:
            obj = json.load(f)
            keyring = dns.tsigkeyring.from_text(obj)
    else:
        keyring = None
    update = Update(f'{domain}', keyring=keyring)
    update.replace(name, ttl, record_type, record_data)
    nameserver = socket.gethostbyname(conf.get_mandatory('nameserver'))
    r = dns.query.tcp(update, nameserver, timeout=10)
    debug(r)
    return r.id


def action_dane_tlsa(conf: Config) -> None:
    """Update TLSA record."""
    path_re = re.compile(r'^(cert_\S+)_path$')
    record_re = re.compile(r'^(\d)-(\d)-(\d)$')
    for option in conf.options():
        match = path_re.match(option)
        if match:
            debug(option)
            filename = conf.get_mandatory(option)
            debug(filename)
            record = conf.get_mandatory(f'{match.group(1)}_record')
            if record_re.match(record):
                certificate = read_x509_cert(filename)
                data = dane_tlsa_data(record, certificate)
                update_dns(conf, 'letsdns_tlsa', 'TLSA', data)
            else:
                error(f'Unsupported TLSA record "{record}" in section "{conf.active_section}"')
