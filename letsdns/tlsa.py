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

import dns.query
import dns.tsigkeyring
from dns.rdata import from_text
from dns.rdataclass import RdataClass
from dns.rdataset import Rdataset
from dns.rdatatype import RdataType
from dns.update import UpdateMessage

from letsdns.configuration import Config
from letsdns.crypto import dane_tlsa_data
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
    message = UpdateMessage(zone=zone, keyring=keyring)
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
    dataset = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=ttl)
    for option in conf.options():
        match = path_re.match(option)
        if match:
            debug(option)
            filename = conf.get_mandatory(option)
            debug(filename)
            certificate = read_x509_cert(filename)
            for tlsa in dane_tlsa_data(certificate):
                rdata = from_text(RdataClass.IN, RdataType.TLSA, tlsa)
                dataset.add(rdata)
    if len(dataset) > 0:
        # TODO: Make name configurable
        update_dns(conf, '_25._tcp.mail', dataset)
