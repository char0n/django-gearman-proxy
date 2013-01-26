import logging

from sendsms.backends.base import BaseSmsBackend

from django_gearman_commands import submit_job

from django.core.management import load_command_class

import django_gearman_proxy.settings
from django_gearman_proxy import load_object


log = logging.getLogger(__name__)


PROXY_TASK_NAME = load_command_class('django_gearman_proxy', 'send_sms').task_name
SERIALIZER = load_object(django_gearman_proxy.settings.GEARMAN_SMS_SERIALIZER)


class SmsBackend(BaseSmsBackend):

    def send_messages(self, messages):
        """
        :param messages: list of sendsms.message.SmsMessage objects.
        :type messages: list
        :return: number of successfully submitted send_sms jobs
        :rtype: int

        """
        sent = 0
        for msg in messages:
            try:
                submit_job(PROXY_TASK_NAME, data=SERIALIZER(msg))
                sent += 1
            except Exception:
                log.exception('Error while submitting sms job from gearman sms backend.')
        return sent
    send_messages.__doc__ = BaseSmsBackend.__doc__ + send_messages.__doc__