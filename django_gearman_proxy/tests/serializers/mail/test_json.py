import json
import unittest

from django.core.mail.message import EmailMessage

import django_gearman_proxy.settings
django_gearman_proxy.settings.GEARMAN_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
django_gearman_proxy.settings.GEARMAN_EMAIL_SERIALIZER = 'django_gearman_proxy.serializers.mail.json.serialize'
django_gearman_proxy.settings.GEARMAN_EMAIL_UNSERIALIZER = 'django_gearman_proxy.serializers.mail.json.unserialize'

from django_gearman_proxy import load_object
EmailBackend = load_object(django_gearman_proxy.settings.GEARMAN_EMAIL_BACKEND)


class TestMailJsonSerializer(unittest.TestCase):

    def setUp(self):
        self.email_message = EmailMessage(subject=u'test subject', body=u'test body', from_email='from@test.sk',
                                          to=['to@test.sk'], bcc=['bcc@test.sk'], attachments=['/path/to/file'],
                                          headers={'Extra-Header': 'extra-value'}, cc=['cc@test.sk'])
        serializer = load_object(django_gearman_proxy.settings.GEARMAN_EMAIL_SERIALIZER)
        self.serialized = json.loads(serializer(self.email_message))

    def test_serialize(self):
        self.assertIsInstance(self.serialized, dict)
        self.assertEqual(self.serialized['subject'], u'test subject')
        self.assertEqual(self.serialized['body'], u'test body')
        self.assertEqual(self.serialized['from_email'], 'from@test.sk')
        self.assertEqual(self.serialized['to'], ['to@test.sk'])
        self.assertEqual(self.serialized['bcc'], ['bcc@test.sk'])
        self.assertEqual(self.serialized['attachments'], ['/path/to/file'])
        self.assertEqual(self.serialized['headers'], {'Extra-Header': 'extra-value'})
        self.assertEqual(self.serialized['cc'], ['cc@test.sk'])
        self.assertEqual(self.serialized['connection'], django_gearman_proxy.settings.GEARMAN_EMAIL_BACKEND)


class TestMailJsonUnserializer(unittest.TestCase):

    def setUp(self):
        self.serialized = '{"body": "test body", "to": ["to@test.sk"],' \
                          ' "connection": "django.core.mail.backends.smtp.EmailBackend",' \
                          ' "attachments": ["/path/to/file"], "bcc": ["bcc@test.sk"], "cc": ["cc@test.sk"],' \
                          ' "headers": {"Extra-Header": "extra-value"}, "from_email": "from@test.sk",' \
                          ' "subject": "test subject"}'
        unserializer = load_object(django_gearman_proxy.settings.GEARMAN_EMAIL_UNSERIALIZER)
        self.email_message = unserializer(self.serialized)

    def test_unserialize(self):
        self.assertIsInstance(self.email_message, EmailMessage)
        self.assertEqual(self.email_message.subject, u'test subject')
        self.assertEqual(self.email_message.body, u'test body')
        self.assertEqual(self.email_message.from_email, 'from@test.sk')
        self.assertEqual(self.email_message.to, ['to@test.sk'])
        self.assertEqual(self.email_message.bcc, ['bcc@test.sk'])
        self.assertEqual(self.email_message.attachments, ['/path/to/file'])
        self.assertEqual(self.email_message.extra_headers, {'Extra-Header': 'extra-value'})
        self.assertEqual(self.email_message.cc, ['cc@test.sk'])
        self.assertIsInstance(self.email_message.get_connection(), EmailBackend)