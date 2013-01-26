from sendsms.api import get_connection
from sendsms.message import SmsMessage

from django.utils.importlib import import_module
json = import_module('json')

import django_gearman_proxy.settings


def serialize(sms_message):
    """Util for serializing SmsMessage object.
    
    SmsMessage object is serialized into json string that is easily transferable via
    gearman protocol as job payload.

    :param email_message: email message to be serialized
    :type email_message: sendsms.message.SmsMessage
    :returns: json representation of SmsMessage object
    :rtype: string
    
    """
    return json.dumps({
        'to': sms_message.to, 'from_phone': sms_message.from_phone, 'body': sms_message.body,
        'flash': sms_message.flash, 'connection': django_gearman_proxy.settings.GEARMAN_SMS_BACKEND
    })


def unserialize(serialized):
    """Util for unserializing json data and  constructing new SmsMessage object.

    :param serialized: json serialized SmsMessage object
    :type serialized: string
    :returns: SmsMessage object constructed from json representation
    :rtype: sendsms.message.SmsMessage

    """
    sms_props = json.loads(serialized)
    return SmsMessage(sms_props.get('body'), from_phone=sms_props.get('from_phone'), to=sms_props.get('to'),
                      flash=sms_props.get('flash'), connection=get_connection(path=sms_props.get('connection')))