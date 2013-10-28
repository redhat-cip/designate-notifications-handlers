from dnh import consumer as dnh_consumer
from dnh.test import DnhTestCase
from mock import patch
from mock import MagicMock
from stevedore.tests.manager import TestExtensionManager


class TestHandler(DnhTestCase):

    def test_handle(self):
        n = self.get_create_notification()
        with patch('kombu.message.Message') as message_mock:
            nsd4_ext = MagicMock()
            nsd4_ext.obj = MagicMock()
            consumer = dnh_consumer.Consumer()
            consumer.handlers = TestExtensionManager([nsd4_ext])
            consumer.on_message(n, message_mock)
            nsd4_ext.obj.handle.assert_called_with(n)
            message_mock.ack.assert_called_with()
