django-gearman-proxy
====================

django-gearman-proxy is django app containing backends/workers for asynchronous email and sms sending
using gearman as message queue.


How it works
------------

**Emails**

This app enables you to send email asynchronously without blocking current threads, while
sending email messages via various backends.

This setting in your project settings file does the following: ::

 # E-mails are sent to proxy backend.
 EMAIL_BACKEND = 'django_gearman_proxy.backends.mail.EmailBackend'

 # Email backend to be used inside of mail sender worker.
 GEARMAN_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


All email messages are sent to proxy email backend defined in settings *EMAIL_BACKEND*, in this example
*'django_gearman_proxy.backends.mail.EmailBackend'*. This backend serializes email message to json format and
submit it as background job to gearman message queue. django-gearman-proxy contains asynchronous email worker
implemented as django command. You have to start this command to make the magic work. ::

 $ python manage.py send_email

Right after *send_email* command is up and running, it pulls email message job from gearman message queue,
unserialize it from json and send it via backend defined in *GEARMAN_EMAIL_BACKEND*, in this example
*'django.core.mail.backends.smtp.EmailBackend'*. This architecture allows to send email messages directly from
your django application, without blocking request/response cycles because email messages are sent in background.

**Sms messages**

This app enables you to send sms messages asynchronously without blocking current threads, while
sending sms messages via various backends.

This setting in your project settings file does the following: ::

 # Sms messages are sent to proxy backend.
 SMS_BACKEND = 'sendsms.backends.smssluzbacz.SmsBackend' = 'django_gearman_proxy.backends.sms.SmsBackend'

 # Sms backend to be used inside of sms sender worker.
 GEARMAN_SMSL_BACKEND = 'sendsms.backends.smssluzbacz.SmsBackend'


All sms messages are sent to proxy sms backend defined in settings *SMS_BACKEND*, in this example
*'django_gearman_proxy.backends.sms.SmsBackend'*. This backend serializes sms message to json format and
submit it as background job to gearman message queue. django-gearman-proxy contains asynchronous sms worker
implemented as django command. You have to start this command to make the magic work. ::

 $ python manage.py send_sms

Right after *send_sms* command is up and running, it pulls sms message job from gearman message queue,
unserialize it from json and send it via backend defined in *GEARMAN_SMS_BACKEND*, in this example
*'sendsms.backends.smssluzbacz.SmsBackend'*. This architecture allows to send sms messages directly from
your django application, without blocking request/response cycles because sms messages are sent in background.


For more information how to run command as asynchronous workers, please
refer to `django-gearman-commands <http://github.com/CodeScaleInc/django-gearman-commands>`_.


Requirements
------------

 - python 2.7+
 - django
 - django_gearman_commands
 - smssluzbacz-api
 - django-sendsms
 - python-gearman
 - running gearman daemon


Installation
------------

Install via pypi or copy this module into your project or into your PYTHONPATH.


**Put django_gearman_proxy into INSTALLED_APPS in your projects settings.py file**

::

 INSTALLED_APPS = (
     'localeurl',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.sites',
     'django.contrib.admin',
     'django.contrib.sitemaps',
     'web',
     'debug_toolbar',
     'rosetta',
     'south',
     'django_gearman_proxy'
 )


Configuration
-------------

**django settings.py constants**

::

 # E-mails are sent to proxy backend.
 EMAIL_BACKEND = 'django_gearman_proxy.backends.mail.EmailBackend'

 # Email backend to be used inside of mail sender worker.
 GEARMAN_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

 # Serializers for transporting EmailMessage object via gearman protocol.
 GEARMAN_EMAIL_SERIALIZER = 'django_gearman_proxy.serializers.mail.json.serialize'
 GEARMAN_EMAIL_UNSERIALIZER = 'django_gearman_proxy.serializers.mail.json.unserialize'


 # Sms messages are sent to proxy backend.
 SMS_BACKEND = 'django_gearman_proxy.backends.sms.SmsBackend'

 # SMS backend to be used inside of sms sender worker.
 GEARMAN_SMS_BACKEND = 'sendsms.backends.smssluzbacz.SmsBackend'

 # Serializers for transporting SmsMessage object via gearman protocol.
 GEARMAN_SMS_SERIALIZER = 'django_gearman_proxy.serializers.sms.json.serialize'
 GEARMAN_SMS_UNSERIALIZER = 'django_gearman_proxy.serializers.sms.json.unserialize'


Tests
-----

**Tested on evnironment**

 - Xubuntu Linux 12.04.1 LTS precise 64-bit
 - python 2.7.3+
 - python unittest
 - django 1.4.5
 - gearmand 1.1.1

**Running tests**

To run the tests from your django project, run command: ::

 $ python manage.py test django_gearman_proxy


Author
------

| char0n (Vladimír Gorej, CodeScale s.r.o.)
| email: gorej@codescale.net
| web: http://www.codescale.net/


References
----------

 - http://github.com/CodeScaleInc/django-gearman-proxy
 - http://pypi.python.org/pypi/django-gearman-proxy/
 - http://www.codescale.net/en/community#django-gearman-proxy