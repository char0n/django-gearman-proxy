import unittest

from django.core.management import load_command_class


class TestSendSmsCommand(unittest.TestCase):

    def setUp(self):
        self.command = load_command_class('django_gearman_proxy', 'send_sms')
        self.serialized = '{"body": "sms body", "to": ["00420777222333"],'\
                          ' "connection": "sendsms.backends.filebased.SmsBackend", "flash": true,'\
                          ' "from_phone": "0001"}'

    def test_do_job(self):
        result = self.command.do_job(self.serialized)
        self.assertTrue(result)