import unittest
from oslo.config import cfg
from dnh import consumer as dnh_consumer
from dnh.handler import nsd4


class DnhTestCase(unittest.TestCase):

    def setUp(self):
        cfg.CONF.set_override('handlers', ['nsd4'],
                              group=dnh_consumer.CFG_GRP)
        cfg.CONF.set_override('nsd_host', 'localhost',
                              group=nsd4.CFG_GRP)
        cfg.CONF.set_override('pattern', 'slave',
                              group=nsd4.CFG_GRP)

    def get_create_notification(self):
        return {
            '_context_roles': [],
            '_context_request_id': 'req-1328a110-c878-437b-8455-1b94eefc66b6',
            '_context_original_tenant_id': None,
            'event_type': 'dns.domain.create',
            'timestamp': u'2013-10-25 19:27:51.420937',
            '_context_auth_token': None,
            '_context_show_deleted': False,
            '_context_tenant': None,
            'message_id': u'2c60ea8c-60c7-40d2-8413-be7c12080477',
            '_unique_id': u'3e0bf71968624a96831e17def3c6d6a4',
            '_context_is_admin': True,
            '_context_read_only': False,
            '_context_tenant_id': None,
            '_context_user': None,
            '_context_user_id': None,
            'publisher_id': u'central.wr0k',
            'payload': {
                'status': u'ACTIVE',
                'retry': 600,
                'name': 'example.com.',
                'deleted': '0',
                'tenant_id': None,
                'created_at': u'2013-10-25T19:27:51.373368',
                'version': 1,
                'updated_at': None,
                'refresh': 3600,
                'id': '56248a86-ba74-4a53-aab4-abc6a472d32a',
                'minimum': 3600,
                'parent_domain_id': None,
                'expire': 86400,
                'ttl': 3600,
                'serial': 1382729271,
                'deleted_at': None,
                'email':
                'admin@example.com',
                'description': None,
            },
            'priority': 'INFO'
        }

    def get_delete_notification(self):
        return {
            '_context_roles': [],
            '_context_request_id': 'req-eab56feb-0354-4ef7-900a-0b7cf8a21967',
            '_context_original_tenant_id': None,
            'event_type': 'dns.domain.delete',
            'timestamp': '2013-10-25 19:40:13.310722',
            '_context_auth_token': None,
            '_context_show_deleted': False,
            '_context_tenant': None,
            'message_id': 'b7ab44c5-4444-405e-a2f6-16d192c66c8e',
            '_unique_id': '15c791dd5c0e4538a8b26dd2a519bfa3',
            '_context_is_admin': True,
            '_context_read_only': False,
            '_context_tenant_id': None,
            '_context_user': None,
            '_context_user_id': None,
            'publisher_id': 'central.wr0k',
            'payload': {
                'status': 'ACTIVE',
                'retry': 600,
                'name': 'example.com.',
                'deleted': '0',
                'tenant_id': None,
                'created_at': '2013-10-25T19:27:51.000000',
                'version': 1,
                'updated_at': None,
                'refresh': 3600,
                'id': '56248a86-ba74-4a53-aab4-abc6a472d32a',
                'minimum': 3600,
                'parent_domain_id': None,
                'expire': 86400,
                'ttl': 3600,
                'serial': 1382729271,
                'deleted_at': None,
                'email': 'admin@example.com',
                'description': None,
            },
            'priority': 'INFO',
        }
