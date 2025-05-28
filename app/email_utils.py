# email_utils.py
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_custom_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
    """
    Customize email sending to handle plain-text and HTML emails.
    """
    # Render the subject, plain-text, and HTML templates
    subject = render_to_string(subject_template_name, context).strip()
    plain_message = render_to_string(email_template_name, context)
    html_message = render_to_string(html_email_template_name, context) if html_email_template_name else None

    # Create the email object
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,  # Fallback for non-HTML email clients
        from_email=from_email,
        to=[to_email],
    )

    # If HTML content is available, attach it
    if html_message:
        email.attach_alternative(html_message, "text/html")

    # Send the email
    email.send()


def send_verification_email(user, request):
    user.generate_verification_token()
    current_site = get_current_site(request)
    mail_subject = "Activate your account"
    context = {
        "user": user,
        "domain": current_site.domain,
        "uid": str(user.id),
        "token": user.verification_token,
    }
    send_custom_mail(
        subject_template_name="registration/acc_active_email_subject.txt",
        email_template_name="registration/acc_active_email.txt",
        context=context,
        from_email="himanshughodse@gmail.com",  # Update to your sender email
        to_email=user.email,
        html_email_template_name="registration/acc_active_email.html"
    )
