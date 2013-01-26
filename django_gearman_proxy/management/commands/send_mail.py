import logging

from django_gearman_commands import GearmanWorkerBaseCommand

import django_gearman_proxy.settings
from django_gearman_proxy import load_object


log = logging.getLogger(__name__)


UNSERIALIZER = load_object(django_gearman_proxy.settings.GEARMAN_EMAIL_UNSERIALIZER)


class Command(GearmanWorkerBaseCommand):

    @property
    def task_name(self):
        return 'send_mail'

    def do_job(self, job_data):
        to_return = False
        try:
            email_message = UNSERIALIZER(job_data)
            log.info('Sending mail message to "%s"', email_message.to)
            to_return = email_message.send()
        except Exception:
            log.exception('Error while sending mail message with data: %s', job_data)
        return to_return