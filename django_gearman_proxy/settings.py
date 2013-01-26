from django.conf import settings


# Email backend to be used inside of mail sender worker.
GEARMAN_EMAIL_BACKEND = getattr(settings, 'GEARMAN_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

# Serializers for transporting EmailMessage object via gearman protocol.
GEARMAN_EMAIL_SERIALIZER = getattr(settings, 'GEARMAN_EMAIL_SERIALIZER', 'django_gearman_proxy.serializers.mail.json.serialize')
GEARMAN_EMAIL_UNSERIALIZER = getattr(settings, 'GEARMAN_EMAIL_UNSERIALIZER', 'django_gearman_proxy.serializers.mail.json.unserialize')

# SMS backend to be used inside of sms sender worker.
GEARMAN_SMS_BACKEND = getattr(settings, 'GEARMAN_SMS_BACKEND', 'sendsms.backends.smssluzbacz.SmsBackend')

# Serializers for transporting SmsMessage object via gearman protocol.
GEARMAN_SMS_SERIALIZER = getattr(settings, 'GEARMAN_SMS_SERIALIZER', 'django_gearman_proxy.serializers.sms.json.serialize')
GEARMAN_SMS_UNSERIALIZER = getattr(settings, 'GEARMAN_SMS_UNSERIALIZER', 'django_gearman_proxy.serializers.sms.json.unserialize')