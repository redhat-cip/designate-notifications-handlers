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

import logging

LOG = logging.getLogger(__name__)


class BaseHandler:
    """ Abstract class that Consumer calls to handle events """

    def handle(self, body):
        """
        Handle the notification by getting the event_type from the body,
        replacing . with _ and calling the resulting method by reflection
        """
        event_type = body['event_type']
        method_name = event_type.replace('.', '_')
        try:
            method = getattr(self, method_name)
            method(body)
        except AttributeError:
            LOG.debug('%s needs a method called `%s` to handle %s' %
                      (self.__class__.__name__, method_name, event_type))
