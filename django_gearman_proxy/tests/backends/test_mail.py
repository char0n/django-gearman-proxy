import unittest

from django.core.mail import get_connection
from django.core.mail.message import EmailMessage

import django_gearman_proxy.backends.mail


class TestEmailBackend(unittest.TestCase):

    def setUp(self):
        self.func = django_gearman_proxy.backends.mail.submit_job
        django_gearman_proxy.backends.mail.submit_job = lambda task_name, data: (task_name, data)
        self.connection = get_connection(backend='django_gearman_proxy.backends.mail.EmailBackend')
        self.message = EmailMessage(subject=u'subject', body=u'body', from_email='from@test.sk', to=['to@test.sk'])

    def tearDown(self):
        django_gearman_proxy.backends.mail.submit_job = self.func
        self.func = self.connection = self.message = None

    def test_submit_mail_job(self):
        result = self.connection.send_messages([self.message])
        self.assertEqual(result, 1)