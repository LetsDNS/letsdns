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
from logging import debug
from logging import error
from typing import List
from typing import Optional

import requests
from requests import RequestException
from requests import Response

from letsdns.action import Action
from letsdns.configuration import Config
from letsdns.tlsa import record_name
from letsdns.tlsa import tlsa_records


def _content(response: Response) -> Optional[dict]:
    """Return API response content (i.e. JSON body data) in a dict. Debug the response data if necessary.
    May raise a RequestException in case of decoding errors.

    Args:
        response: Response object
    """
    debug(f'{response.status_code} {response.reason}')
    d: dict = response.json()
    if 'error' in d and isinstance(d['error'], list) and len(d['error']) > 0:
        # Non-empty error data found
        error(d['error'])
    return d


class HetznerApiUpdate(Action):
    @classmethod
    def lifecycle(cls, conf: Config, action: Action) -> int:
        """Process configuration data."""
        return action.execute(conf, records=tlsa_records(conf))

    def __init__(self) -> None:
        super().__init__()
        self.headers = {}
        self.api_token = ''
        self.api_url = 'https://dns.hetzner.com/api/v1'

    def zone_id(self, domain: str) -> Optional[str]:
        """Returns zone ID for the given domain name, or None in case of errors.

        Args:
            domain: Domain name, e.g. "example.com".
        """
        response = requests.get(f'{self.api_url}/zones', headers=self.headers, params={'name': domain})
        c = _content(response)
        if response.ok and 'zones' in c and len(c['zones']) > 0 and 'id' in c['zones'][0]:
            return c['zones'][0]['id']

    def find_records(self, zone_id: str, name: str) -> Optional[List[str]]:
        """Returns matching record ID list for the given zone ID and name, or None in case of errors.

        Args:
            zone_id: Parent zone ID.
            name: DNS record name.
        """
        response = requests.get(f'{self.api_url}/records', headers=self.headers, params={'zone_id': zone_id})
        c = _content(response)
        if response.ok and 'records' in c:
            id_list: List[str] = []
            name = name.lower()
            for record in c['records']:
                if 'name' in record and record['type'].lower() == 'tlsa' and record['name'].lower() == name:
                    id_list.append(record['id'])
            return id_list

    def cleanup_records(self, zone_id: str, name: str) -> bool:
        """Delete existing TLSA records. Returns True to indicate success.

        Args:
            zone_id: Parent zone ID.
            name: DNS record name.
        """
        id_list = self.find_records(zone_id, name)
        if id_list is None:  # pragma: no cover
            error('Error while attempting to find existing TLSA records')
            return False
        elif len(id_list) < 1:  # pragma: no cover
            debug('No existing TLSA records found')
            return True
        for record_id in id_list:
            response = requests.delete(f'{self.api_url}/records/{record_id}', headers=self.headers)
            # Debug response ignoring the actual content
            _content(response)
            if not response.ok:  # pragma: no cover
                return False
        return True

    def execute(self, conf: Config, *args, **kwargs) -> int:
        """Update DNS record using the Hetzner DNS API. Return 0 to indicate success."""
        records: List[str] = kwargs['records']
        if len(records) < 1:
            return 0
        self.api_token = conf.get_mandatory('api_token')
        self.headers = {'Auth-API-Token': self.api_token}
        self.api_url = conf.get('api_url', fallback=self.api_url)
        try:
            zone_id = self.zone_id(conf.get_mandatory('domain'))
            data = {
                'ttl': conf.get_ttl(),
                'type': 'TLSA',
                'zone_id': zone_id,
            }
            for port in conf.get_tcp_ports():
                name = record_name(conf, port)
                if zone_id is None or not self.cleanup_records(zone_id, name):  # pragma: no cover
                    error('Error while deleting existing TLSA records')
                    return 2
                for record in records:
                    data['name'] = name
                    data['value'] = record
                    response = requests.post(f'{self.api_url}/records', headers=self.headers, json=data)
                    # Debug response ignoring the actual content
                    _content(response)
                    if not response.ok:  # pragma: no cover
                        return 3
        except RequestException as e:  # pragma: no cover
            error(e)
            return 1
        return 0
