import unittest

from sendsms.api import get_connection
from sendsms.message import SmsMessage

import django_gearman_proxy.backends.sms


class TestSmsBackend(unittest.TestCase):

    def setUp(self):
        self.func = django_gearman_proxy.backends.sms.submit_job
        django_gearman_proxy.backends.sms.submit_job = lambda task_name, data: (task_name, data)
        self.connection = get_connection(path='django_gearman_proxy.backends.sms.SmsBackend')
        self.message = SmsMessage(body='body', from_phone='0001', to=['0002'])

    def tearDown(self):
        django_gearman_proxy.backends.sms.submit_job = self.func
        self.func = self.connection = self.message = None

    def test_submit_mail_job(self):
        result = self.connection.send_messages([self.message])
        self.assertEqual(result, 1)