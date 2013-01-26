import unittest

from django.core.management import load_command_class


class TestSendMailCommand(unittest.TestCase):

    def setUp(self):
        self.command = load_command_class('django_gearman_proxy', 'send_mail')
        self.serialized = '{"body": "test body", "to": ["to@test.sk"],'\
                          ' "connection": "django.core.mail.backends.filebased.EmailBackend",'\
                          ' "bcc": ["bcc@test.sk"], "cc": ["cc@test.sk"],'\
                          ' "from_email": "from@test.sk", "subject": "test subject"}'

    def test_do_job(self):
        result = self.command.do_job(self.serialized)
        self.assertTrue(result)