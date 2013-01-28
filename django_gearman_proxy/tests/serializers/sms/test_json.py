import json
import unittest

from sendsms.message import SmsMessage

import django_gearman_proxy.settings
django_gearman_proxy.settings.GEARMAN_SMS_BACKEND = 'sendsms.backends.smssluzbacz.SmsBackend'
django_gearman_proxy.settings.GEARMAN_SMS_SERIALIZER = 'django_gearman_proxy.serializers.sms.json.serialize'
django_gearman_proxy.settings.GEARMAN_SMS_UNSERIALIZER = 'django_gearman_proxy.serializers.sms.json.unserialize'

from django_gearman_proxy import load_object
SmsBackend = load_object(django_gearman_proxy.settings.GEARMAN_SMS_BACKEND)


class TestSmsJsonSerializer(unittest.TestCase):

    def setUp(self):
        self.sms_message = SmsMessage('sms body', from_phone='0001', to=['0002', '0003'], flash=True)
        serializer = load_object(django_gearman_proxy.settings.GEARMAN_SMS_SERIALIZER)
        self.serialized = json.loads(serializer(self.sms_message))

    def test_serialize(self):
        self.assertIsInstance(self.serialized, dict)
        self.assertEqual(self.serialized['body'], 'sms body')
        self.assertEqual(self.serialized['from_phone'], '0001')
        self.assertEqual(self.serialized['to'], ['0002', '0003'])
        self.assertTrue(self.serialized['flash'])
        self.assertEqual(self.serialized['connection'], django_gearman_proxy.settings.GEARMAN_SMS_BACKEND)


class TestSmsJsonUnserializer(unittest.TestCase):

    def setUp(self):
        self.serialized = '{"body": "sms body", "to": ["0002", "0003"], ' \
                          '"connection": "sendsms.backends.smssluzbacz.SmsBackend", "flash": true, ' \
                          '"from_phone": "0001"}'
        unserializer = load_object(django_gearman_proxy.settings.GEARMAN_SMS_UNSERIALIZER)
        self.sms_message = unserializer(self.serialized)

    def test_unserialize(self):
        self.assertIsInstance(self.sms_message, SmsMessage)
        self.assertEqual(self.sms_message.body, 'sms body')
        self.assertEqual(self.sms_message.from_phone, '0001')
        self.assertEqual(self.sms_message.to, ['0002', '0003'])
        self.assertTrue(self.sms_message.flash)
        self.assertIsInstance(self.sms_message.get_connection(), SmsBackend)