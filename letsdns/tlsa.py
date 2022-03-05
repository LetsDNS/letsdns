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
import re
from typing import List

from dns.rdata import from_text
from dns.rdataclass import RdataClass
from dns.rdataset import Rdataset
from dns.rdatatype import RdataType

from letsdns.action import Action
from letsdns.configuration import Config
from letsdns.crypto import dane_tlsa_records
from letsdns.crypto import read_x509_cert


def action_dane_tlsa(conf: Config, action: Action) -> None:
    """Update TLSA record."""
    path_re = re.compile(r'^(cert_\S+)_path$')
    ttl = int(conf.get_mandatory('ttl'))
    hostname = ''
    tlsa_records: List[str] = list()
    for option in conf.options():
        if path_re.match(option):
            filename = conf.get_mandatory(option)
            hostname = conf.get_mandatory('hostname')
            cert = read_x509_cert(filename)
            for record in dane_tlsa_records(cert):
                if record not in tlsa_records:
                    tlsa_records.append(record)
    if hostname and len(tlsa_records) > 0:
        rdata_set = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=ttl)
        for tlsa in tlsa_records:
            rdata = from_text(RdataClass.IN, RdataType.TLSA, tlsa)
            rdata_set.add(rdata)
        action.execute(conf, dataset=rdata_set, name=f'_25._tcp.{hostname}')
