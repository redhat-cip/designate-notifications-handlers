# Copyright (C) 2013 eNovance SAS <licensing@enovance.com>
#
# Author: Artom Lifshitz <artom.lifshitz@enovance.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from kombu import mixins
import kombu
import signal
import logging
from oslo.config import cfg
from stevedore import named

LOG = logging.getLogger(__name__)

cfg.CONF.register_opts([
    cfg.BoolOpt('debug', default=False, required=True),
])

CFG_GRP = 'consumer'
cfg.CONF.register_group(
    cfg.OptGroup(name=CFG_GRP,
                 title='Configuration for notifications consumer')
)
cfg.CONF.register_opts([
    cfg.StrOpt('host', default='localhost', required=True),
    cfg.IntOpt('port', default=5672, required=True),
    cfg.StrOpt('exchange', default='designate', required=True),
    cfg.StrOpt('queue', default='notifications.info', required=True),
    cfg.ListOpt('handlers', required=True),
], group=CFG_GRP)

SIGNALS = dict((k, v) for v, k in signal.__dict__.iteritems()
               if v.startswith('SIG'))


class Consumer(mixins.ConsumerMixin):

    def __init__(self):
        self.handlers = named.NamedExtensionManager(
            namespace='dnh.handler',
            names=cfg.CONF[CFG_GRP].handlers,
            invoke_on_load=True)
        # Some handlers may have required options. They're loaded by stevedore
        # after the initial config parsing, so we reparse the config file here
        # to make sure handlers get all their (required) options parsed.
        cfg.CONF()
        self.connection = kombu.Connection(
            'amqp://%s:%d' % (cfg.CONF[CFG_GRP].host,
                              cfg.CONF[CFG_GRP].port))
        signal.signal(signal.SIGTERM, self.on_signal_stop)
        signal.signal(signal.SIGINT, self.on_signal_stop)

    def on_signal_stop(self, signum, frame):
        LOG.info('Caught %s, stopping' % SIGNALS[signum])
        self.should_stop = True

    def on_connection_error(self, exc, interval):
        # self.should_stop only has an effect if the connection is already
        # established. If the kombu is retrying the connection,
        # self.should_stop # has no effect, so we need to override
        # ConsumerMixin's on_connection_error to raise an exception
        if self.should_stop:
            raise
        else:
            LOG.warn('Broker connection error: %r. '
                     'Trying again in %s seconds.', exc, interval)

    def get_consumers(self, Consumer, channel):
        exchange = kombu.Exchange(cfg.CONF[CFG_GRP].exchange, type='topic',
                                  durable=False)
        queue = kombu.Queue(cfg.CONF[CFG_GRP].queue, exchange=exchange,
                            channel=channel, durable=False)
        return [
            kombu.Consumer(channel, queue, callbacks=[self.on_message])
        ]

    def on_message(self, body, message):
        def handle(ext, body):
            return (ext.name, ext.obj.handle(body))

        self.handlers.map(handle, body)
        message.ack()
