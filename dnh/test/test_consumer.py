from dnh import consumer as dnh_consumer
from dnh.test import DnhTestCase
import signal


class TestConsumer(DnhTestCase):

    def test_sigterm(self):
        consumer = dnh_consumer.Consumer()
        consumer.on_signal_stop(signal.SIGTERM, None)
        self.assertEqual(consumer.should_stop, True)

    def test_sigint(self):
        consumer = dnh_consumer.Consumer()
        consumer.on_signal_stop(signal.SIGINT, None)
        self.assertEqual(consumer.should_stop, True)
