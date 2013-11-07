from dnh.handler.nsd4 import NSD4Handler
from dnh.handler import nsd4
from dnh.test import DnhTestCase
from mock import MagicMock
from oslo.config import cfg


class TestNSD4(DnhTestCase):

    def test_create(self):
        n = self.get_create_notification()
        nsd4_handler = NSD4Handler()
        nsd4_handler.dns_domain_create = MagicMock()
        nsd4_handler.handle(n)
        nsd4_handler.dns_domain_create.assert_called_with(n)

    def test_delete(self):
        n = self.get_delete_notification()
        nsd4_handler = NSD4Handler()
        nsd4_handler.dns_domain_delete = MagicMock()
        nsd4_handler.handle(n)
        nsd4_handler.dns_domain_delete.assert_called_with(n)

    def test_create_command(self):
        n = self.get_create_notification()
        domain = n['payload']['name']
        pattern = cfg.CONF[nsd4.CFG_GRP].pattern
        nsd4_handler = NSD4Handler()
        nsd4_handler._command = MagicMock()
        nsd4_handler.handle(n)
        nsd4_handler._command.assert_any_call('addzone %s %s' %
                                              (domain, pattern),
                                              'host1', 4242)
        nsd4_handler._command.assert_any_call('addzone %s %s' %
                                              (domain, pattern),
                                              'host2', 8952)

    def test_delete_command(self):
        n = self.get_delete_notification()
        domain = n['payload']['name']
        nsd4_handler = NSD4Handler()
        nsd4_handler._command = MagicMock()
        nsd4_handler.handle(n)
        nsd4_handler._command.assert_any_call('delzone %s' % domain,
                                              'host1', 4242)
        nsd4_handler._command.assert_any_call('delzone %s' % domain,
                                              'host2', 8952)
