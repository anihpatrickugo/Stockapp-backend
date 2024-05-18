from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings



def send_user_verify_otp(user, code):
    subject = f'Verify OTP - {settings.SITE_NAME}'
    html_message = render_to_string('users/verify_otp.html', {'name': user.first_name, 'code': code})
    plain_message = strip_tags(html_message)
    from_email = settings.SITE_DEFAULT_MAIL_SENDER
    to = [user.email]

    message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to, body=plain_message)
    message.attach_alternative(html_message, "text/html")
    message.send()


def send_new_pin_mail(user, code):
    subject = f'New Transaction Pin- {settings.SITE_NAME}'
    html_message = render_to_string('users/new_pin.html', {'name': user.first_name, 'code': code})
    plain_message = strip_tags(html_message)
    from_email = settings.SITE_DEFAULT_MAIL_SENDER
    to = [user.email]

    message = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to, body=plain_message)
    message.attach_alternative(html_message, "text/html")
    message.send()
    



