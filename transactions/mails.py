from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



def send_deposit_verified(user, deposit):
    subject = f'Depoist Verified - {settings.SITE_NAME}'
    html_message = render_to_string('transactions/verified_deposit.html', {'name': user.first_name, 'deposit': deposit})
    plain_message = strip_tags(html_message)
    from_email = settings.SITE_DEFAULT_MAIL_SENDER
    to = [user.email]

    message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to, body=plain_message)
    message.attach_alternative(html_message, "text/html")
    message.send()
    


def send_Withdrawal_verified(user, withdrawal):
    subject = f'Withdrawal Verified - {settings.SITE_NAME}'
    html_message = render_to_string('transactions/verified_withdrawal.html', {'name': user.first_name, 'withdrawal': withdrawal})
    plain_message = strip_tags(html_message)
    from_email = settings.SITE_DEFAULT_MAIL_SENDER
    to = [user.email]

    message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to, body=plain_message)
    message.attach_alternative(html_message, "text/html")
    message.send()



# for admin only


def send_deposit_request(user, deposit):
    subject = f'New Depoist Request - {settings.SITE_NAME}'
    html_message = render_to_string('transactions/admin/new_deposit.html', {'user': user, 'deposit': deposit})
    plain_message = strip_tags(html_message)
    from_email = settings.SITE_DEFAULT_MAIL_SENDER
    to = [settings.SITE_DEFAULT_MAIL_SENDER]

    message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to, body=plain_message)
    message.attach_alternative(html_message, "text/html")
    message.send()

def send_withdrawal_request(user, withdrawal):
    subject = f'New Withdrawal Request - {settings.SITE_NAME}'
    html_message = render_to_string('transactions/admin/new_withdrawal.html', {'user': user, 'withdrawal': withdrawal})
    plain_message = strip_tags(html_message)
    from_email = settings.SITE_DEFAULT_MAIL_SENDER
    to = [settings.SITE_DEFAULT_MAIL_SENDER]

    message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to, body=plain_message)
    message.attach_alternative(html_message, "text/html")
    message.send()

    
