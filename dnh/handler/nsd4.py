# copyright (c) 2013 enovance sas <licensing@enovance.com>
#
# author: artom lifshitz <artom.lifshitz@enovance.com>
#
# licensed under the apache license, version 2.0 (the "license"); you may
# not use this file except in compliance with the license. you may obtain
# a copy of the license at
#
#      http://www.apache.org/licenses/license-2.0
#
# unless required by applicable law or agreed to in writing, software
# distributed under the license is distributed on an "as is" basis, without
# warranties or conditions of any kind, either express or implied. see the
# license for the specific language governing permissions and limitations
# under the license.

import socket
import ssl
import logging
from oslo.config import cfg
from dnh.handler.base import BaseHandler

LOG = logging.getLogger(__name__)

CFG_GRP = 'handler:nsd4'
cfg.CONF.register_group(
    cfg.OptGroup(name=CFG_GRP, title='Configuration for NSD 4 handler')
)
cfg.CONF.register_opts([
    cfg.StrOpt('keyfile', default='/etc/nsd/nsd_control.key', required=True),
    cfg.StrOpt('certfile', default='/etc/nsd/nsd_control.pem', required=True),
    cfg.ListOpt('servers', required=True),
    cfg.StrOpt('pattern', required=True),
], group=CFG_GRP)
DEFAULT_PORT = 8952


class NSD4Handler(BaseHandler):
    """
    Handle domain create and delete events by sending commands to a NSD 4
    server
    """

    NSDCT_VERSION = 'NSDCT1'

    def __init__(self):
        self._keyfile = cfg.CONF[CFG_GRP].keyfile
        self._certfile = cfg.CONF[CFG_GRP].certfile
        self._servers = self._parse_servers()
        self._pattern = cfg.CONF[CFG_GRP].pattern

    def _parse_servers(self):
        servers = []
        for server in cfg.CONF[CFG_GRP].servers:
            try:
                (host, port) = server.split(':')
                port = int(port)
            except ValueError:
                host = server
                port = DEFAULT_PORT
            servers.append({'host': host, 'port': port})
        return servers

    def _command(self, command, host, port):
        sock = socket.create_connection((host, port))
        ssl_sock = ssl.wrap_socket(sock, keyfile=self._keyfile,
                                   certfile=self._certfile)
        stream = ssl_sock.makefile()
        stream.write('%s %s\n' % (self.NSDCT_VERSION, command))
        stream.flush()
        result = stream.read()
        stream.close()
        ssl_sock.close()
        return result.rstrip()

    def _do_and_log(self, command, expect, host, port):
        try:
            result = self._command(command, host, port)
            if result == expect:
                LOG.info('`%s` on %s:%d' %
                         (command, host, port))
            else:
                LOG.error('Failed `%s` on %s:%d. Server said: %s' %
                          (command, host, port, result))
        except socket.error as e:
            LOG.info('Failed `%s` on %s:%d. Error was: %s' %
                     (command, host, port, e))

    def _on_all_servers(self, command, expect):
        for server in self._servers:
            self._do_and_log(command, expect, server['host'], server['port'])

    def dns_domain_create(self, notification):
        domain = notification['payload']['name']
        command = 'addzone %s %s' % (domain, self._pattern)
        self._on_all_servers(command, 'ok')

    def dns_domain_delete(self, notification):
        domain = notification['payload']['name']
        command = 'delzone %s' % domain
        self._on_all_servers(command, 'ok')
