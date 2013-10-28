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
    cfg.StrOpt('nsd_host', required=True),
    cfg.IntOpt('nsd_port', default=8952, required=True),
    cfg.StrOpt('pattern', required=True),
], group=CFG_GRP)


class NSD4Handler(BaseHandler):
    """
    Handle domain create and delete events by sending commands to a NSD 4
    server
    """

    NSDCT_VERSION = 'NSDCT1'

    def __init__(self):
        self._keyfile = cfg.CONF[CFG_GRP].keyfile
        self._certfile = cfg.CONF[CFG_GRP].certfile
        self._nsd_host = cfg.CONF[CFG_GRP].nsd_host
        self._nsd_port = cfg.CONF[CFG_GRP].nsd_port
        self._pattern = cfg.CONF[CFG_GRP].pattern

    def _command(self, command):
        sock = socket.create_connection((self._nsd_host, self._nsd_port))
        ssl_sock = ssl.wrap_socket(sock, keyfile=self._keyfile,
                                   certfile=self._certfile)
        stream = ssl_sock.makefile()
        stream.write('%s %s\n' % (self.NSDCT_VERSION, command))
        stream.flush()
        result = stream.read()
        stream.close()
        ssl_sock.close()
        return result.rstrip()

    def _do_and_log(self, command, expect):
        try:
            result = self._command(command)
            if result == expect:
                LOG.info('`%s` on %s:%d' %
                         (command, self._nsd_host, self._nsd_port))
            else:
                LOG.error('Failed `%s` on %s:%d. Server said: %s' %
                          (command, self._nsd_host, self._nsd_port, result))
        except socket.error as e:
            LOG.info('Failed `%s` on %s:%d. Error was: %s' %
                     (command, self._nsd_host, self._nsd_port, e))

    def dns_domain_create(self, notification):
        domain = notification['payload']['name']
        command = 'addzone %s %s' % (domain, self._pattern)
        self._do_and_log(command, 'ok')

    def dns_domain_delete(self, notification):
        domain = notification['payload']['name']
        command = 'delzone %s' % domain
        self._do_and_log(command, 'ok')
