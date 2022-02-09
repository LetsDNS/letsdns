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
from typing import List

import dns.query
import dns.tsigkeyring
from dns.rdata import from_text
from dns.rdataclass import RdataClass
from dns.rdataset import Rdataset
from dns.rdatatype import RdataType
from dns.update import Update

from letsdns.configuration import Config
from letsdns.crypto import dane_tlsa_records
from letsdns.crypto import read_x509_cert


def update_dns(conf: Config, name: str, dataset: Rdataset) -> int:
    """Update DNS record.

    Args:
        conf: Config object
        name: Record name
        dataset: Set of rdata objects
    """
    zone = conf.get_mandatory('domain')
    keyfile = conf.get('keyfile')
    if keyfile:
        with open(keyfile, 'r') as f:
            obj = json.load(f)
            keyring = dns.tsigkeyring.from_text(obj)
    else:  # pragma: no cover
        keyring = None
    message = Update(zone=zone, keyring=keyring)
    message.delete(name)
    if len(dataset) > 0:
        message.replace(name, dataset)
    nameserver = socket.gethostbyname(conf.get_mandatory('nameserver'))
    response = dns.query.tcp(message, nameserver, timeout=10)
    debug(response)
    return response.id


def action_dane_tlsa(conf: Config) -> None:
    """Update TLSA record."""
    path_re = re.compile(r'^(cert_\S+)_path$')
    ttl = int(conf.get_mandatory('ttl'))
    hostname = ''
    tlsa_records: List[str] = list()
    for option in conf.options():
        if path_re.match(option):
            debug(option)
            filename = conf.get_mandatory(option)
            debug(filename)
            hostname = conf.get_mandatory('hostname')
            debug(hostname)
            cert = read_x509_cert(filename)
            for record in dane_tlsa_records(cert):
                if record not in tlsa_records:
                    debug(f'Adding {record}')
                    tlsa_records.append(record)
                else:
                    debug(f'Ignoring duplicate {record}')
    if hostname and len(tlsa_records) > 0:
        rdata_set = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=ttl)
        for tlsa in tlsa_records:
            rdata = from_text(RdataClass.IN, RdataType.TLSA, tlsa)
            rdata_set.add(rdata)
        update_dns(conf, f'_25._tcp.{hostname}', rdata_set)
