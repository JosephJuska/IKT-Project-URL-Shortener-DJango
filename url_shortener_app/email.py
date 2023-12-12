from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def verification_email(username, verification_token, email):
    content = {'username' : username, 'verification_token' : verification_token}
    subject = 'Account Verification'
    message = 'Please enable HTML to view this email.'
    html_message = render_to_string('html_message.html', content)
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, html_message=html_message, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)