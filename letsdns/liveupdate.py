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
import json
from _socket import gethostbyname
from logging import debug

from dns import query
from dns import rcode
from dns import tsig
from dns import tsigkeyring
from dns.message import Message
from dns.update import Update

from letsdns.action import Action
from letsdns.configuration import Config
from letsdns.tlsa import rdata_action_lifecycle
from letsdns.tlsa import record_name
from letsdns.util import getenv


class DnsLiveUpdate(Action):
    @classmethod
    def lifecycle(cls, conf: Config, action: Action) -> int:
        return rdata_action_lifecycle(conf, action)

    def execute(self, conf: Config, *args, **kwargs) -> int:
        """Update DNS record using the dnspython library. Return 0 to indicate success."""
        zone = conf.get_mandatory('domain')
        keyalgorithm = conf.get('key_algorithm', tsig.default_algorithm)
        path = conf.get('keyfile')
        if path:
            debug(f'Key file: {path} (TSIG algorithm: {keyalgorithm})')
            with open(path, 'r') as f:
                keyring = tsigkeyring.from_text(json.load(f))
        else:  # pragma: no cover
            keyring = None
        update = Update(zone=zone, keyalgorithm=keyalgorithm, keyring=keyring)
        for port in conf.get_tcp_ports():
            name = record_name(conf, port)
            update.delete(name)
            dataset = kwargs['dataset']
            if len(dataset) > 0:
                update.replace(name, dataset)
            nameserver = gethostbyname(conf.get_mandatory('nameserver'))
            debug(f'DNS update: {update}')
            t = int(getenv('DNS_TIMEOUT_SECONDS', '30'))
            response: Message = query.tcp(update, nameserver, timeout=t)
            debug(f'DNS Response: {response}')
            if rcode.from_flags(response.flags, 0) != rcode.NOERROR:  # pragma: no cover
                return 1
        return 0
