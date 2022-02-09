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


class DnsLiveUpdate(Action):
    def execute(self, conf: Config, *args, **kwargs):
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
        response = query.tcp(update, nameserver, timeout=10)
        debug(response)
        return response.id
