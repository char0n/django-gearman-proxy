import logging

from django.core.mail.backends.base import BaseEmailBackend
from django.core.management import load_command_class

from django_gearman_commands import submit_job

import django_gearman_proxy.settings
from django_gearman_proxy import load_object


log = logging.getLogger(__name__)


PROXY_TASK_NAME = load_command_class('django_gearman_proxy', 'send_mail').task_name
SERIALIZER = load_object(django_gearman_proxy.settings.GEARMAN_EMAIL_SERIALIZER)


class EmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        """
        :param email_messages: list of django.core.mail.message.EmailMessage objects.
        :type email_messages: list
        :return: number of successfully submitted send_mail jobs
        :rtype: int

        """
        sent = 0
        for msg in email_messages:
            try:
                submit_job(PROXY_TASK_NAME, data=SERIALIZER(msg))
                sent += 1
            except Exception:
                log.exception('Error while submitting mail job from gearman email backend')
        return sent
    send_messages.__doc__ = BaseEmailBackend.send_messages.__doc__ + send_messages.__doc__