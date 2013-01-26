import logging

from django_gearman_commands import GearmanWorkerBaseCommand

import django_gearman_proxy.settings
from django_gearman_proxy import load_object


log = logging.getLogger(__name__)


UNSERIALIZER = load_object(django_gearman_proxy.settings.GEARMAN_SMS_UNSERIALIZER)


class Command(GearmanWorkerBaseCommand):

    @property
    def task_name(self):
        return 'send_sms'

    def do_job(self, job_data):
        to_return = False
        try:
            sms_message = UNSERIALIZER(job_data)
            log.info('Sending sms message to "%s"', sms_message.to)
            to_return = sms_message.send()
        except Exception:
            log.exception('Error while sending sms message with data: %s', job_data)
        return to_return