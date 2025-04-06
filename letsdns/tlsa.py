# Copyright © 2022-2025 Ralph Seichter
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


def record_name(conf: Config, tcp_port: str) -> str:
    """Return TLSA record name for the configured host name.
    A single dot '.' host name denotes the domain apex.

    Args:
        conf: Configuration object.
        tcp_port: Desired TCP service port, default 25.
    """
    h = conf.get_mandatory('hostname')
    if h == '.':
        suffix = ''
    else:
        suffix = f'.{h}'
    return f'_{tcp_port}._tcp{suffix}'


def tlsa_records(conf: Config) -> List[str]:
    """Generate list of TLSA record strings based on the given configuration options.

    Args:
        conf: Configuration object.
    """
    path_re = re.compile(r'^cert_\S+_path$')
    records: List[str] = []
    for option in conf.options():
        if path_re.match(option):
            path = conf.get_mandatory(option)
            cert = read_x509_cert(path)
            for record in dane_tlsa_records(cert):
                if record not in records:
                    records.append(record)
    return records


def rdata_action_lifecycle(conf: Config, action: Action) -> int:
    """Lifecycle method for Rdata-based actions."""
    records = tlsa_records(conf)
    if len(records) < 1:  # pragma: no cover
        return 0
    dataset = Rdataset(RdataClass.IN, RdataType.TLSA, ttl=conf.get_ttl())
    for record in records:
        dataset.add(from_text(RdataClass.IN, RdataType.TLSA, record))
    return action.execute(conf, dataset=dataset)
