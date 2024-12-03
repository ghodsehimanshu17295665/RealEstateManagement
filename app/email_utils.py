# email_utils.py
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_verification_email(user, request):
    user.generate_verification_token()
    current_site = get_current_site(request)
    mail_subject = "Activate your account"
    message = render_to_string(
        "registration/acc_active_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": str(user.id),
            "token": user.verification_token,
        },
    )
    email = EmailMultiAlternatives(
        subject=mail_subject,
        body=message,
        to=[user.email],
    )
    email.attach_alternative(message, "text/html")
    email.send()
