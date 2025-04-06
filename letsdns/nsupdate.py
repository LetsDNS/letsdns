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
from letsdns.action import Action
from letsdns.configuration import Config
from letsdns.tlsa import rdata_action_lifecycle
from letsdns.tlsa import record_name


class NsupdateStdout(Action):
    @classmethod
    def lifecycle(cls, conf: Config, action) -> int:
        return rdata_action_lifecycle(conf, action)

    def execute(self, conf: Config, *args, **kwargs) -> int:
        """Generate 'nsupdate' command list and print to stdout."""
        dataset = kwargs['dataset']
        nameserver = conf.get_mandatory('nameserver')
        ttl = int(conf.get_mandatory('ttl'))
        zone = conf.get_mandatory('domain')
        print(f'server {nameserver}')
        for port in conf.get_tcp_ports():
            name = record_name(conf, port)
            print(f'update del {name}.{zone}.', 'IN TLSA')
            for data in dataset:
                print(f'update add {name}.{zone}.', ttl, 'IN TLSA', data)
        print('send')
        return 0
