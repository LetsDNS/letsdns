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
from logging import debug

from _socket import gethostbyname
from dns import query
from dns import tsigkeyring
from dns.update import Update

from letsdns.action import Action
from letsdns.configuration import Config
from letsdns.tlsa import action_dane_tlsa
from letsdns.util import getenv


class DnsLiveUpdate(Action):
    @classmethod
    def lifecycle(cls, conf: Config, action) -> int:
        return action_dane_tlsa(conf, action)

    def execute(self, conf: Config, *args, **kwargs) -> int:
        """Update DNS record using the dnspython library."""
        dataset = kwargs['dataset']
        name = kwargs['name']
        keyfile = conf.get('keyfile')
        zone = conf.get_mandatory('domain')
        if keyfile:
            with open(keyfile, 'r') as f:
                obj = json.load(f)
                keyring = tsigkeyring.from_text(obj)
        else:  # pragma: no cover
            keyring = None
        update = Update(zone=zone, keyring=keyring)
        update.delete(name)
        if len(dataset) > 0:
            update.replace(name, dataset)
        nameserver = gethostbyname(conf.get_mandatory('nameserver'))
        debug(f'DNS update: {update}')
        timeout = int(getenv('DNS_TIMEOUT_SECONDS', '30'))
        response = query.tcp(update, nameserver, timeout=timeout)
        debug(f'DNS Response: {response}')
        return response.id
