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

from dnh import consumer as dnh_consumer
from oslo.config import cfg
import logging
import string
import sys
import os

LOG = logging.getLogger(__name__)


def main():
    logging.basicConfig()
    try:
        cfg.CONF()
        consumer = dnh_consumer.Consumer()
    except cfg.RequiredOptError as e:
        config_files = cfg.CONF.config_file + cfg.CONF.default_config_files
        if config_files:
            LOG.error('%s. Config file(s) used: %s' %
                      (e, string.join(config_files, ', ')))
        else:
            prog = os.path.basename(sys.argv[0])
            oslo_cfg_locations = ['~/%s.conf' % prog, '/etc/%s.conf' % prog]
            LOG.error('No config files found. Tried %s',
                      string.join(oslo_cfg_locations, ', '))
        return 1
    except cfg.ConfigFileValueError as e:
        LOG.error('%s' % e)
        return 1
    except cfg.ConfigFilesNotFoundError as e:
        LOG.error('%s' % e)
        return 1
    if cfg.CONF.debug:
        logging.getLogger().setLevel(level=logging.DEBUG)
    else:
        logging.getLogger().setLevel(level=logging.INFO)
    consumer.run()
