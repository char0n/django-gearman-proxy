import base64
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage
from django.utils.importlib import import_module
json = import_module('json')

import django_gearman_proxy.settings


def serialize(email_message):
    """Util for serializing EmailMessage object.

    EmailMessage object is serialized into json string that is easily transferable via
    gearman protocol as job payload.

    :param email_message: email message to be serialized
    :type email_message: django.core.mail.message.EmailMessage
    :returns: json representation of EmailMessage object
    :rtype: string

    """
    attachments = []
    for attachment in email_message.attachments:
        if isinstance(attachment, tuple):
            attachments.append((attachment[0], 
                                 base64.b64encode(attachment[1]),
                                 attachment[2]))
        else:
            attachments.append(attachment)

    return json.dumps({
        'subject': email_message.subject, 'body': email_message.body, 'from_email': email_message.from_email,
        'to': email_message.to, 'bcc': email_message.bcc, 'attachments': attachments,
        'headers': email_message.extra_headers, 'cc': email_message.cc,
        'connection': django_gearman_proxy.settings.GEARMAN_EMAIL_BACKEND
    })


def unserialize(serialized):
    """Util for unserializing json data and  constructing new EmailMessage object.

    :param serialized: json serialized EmailMessage object
    :type serialized: string
    :returns: EmailMessage object constructed from json representation
    :rtype: django.core.mail.message.EmailMessage

    """
    mail_props = json.loads(serialized)
    attachments = []
    for attachment in mail_props['attachments']:
        if isinstance(attachment, list):
            attachments.append([attachment[0], base64.b64decode(attachment[1]), attachment[2]])
        else:
            attachments.append(attachment)
    return EmailMessage(subject=mail_props.get('subject', u''), body=mail_props.get('body', u''),
        from_email=mail_props.get('from_email'), to=mail_props.get('to'),
        bcc=mail_props.get('bcc'), attachments=attachments,
        headers=mail_props.get('headers'), cc=mail_props.get('cc'),
        connection=get_connection(backend=mail_props.get('connection')))

