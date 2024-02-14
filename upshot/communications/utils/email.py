from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(to_emails, json_content):
    from_email = settings.PROJECT_EMAIL
    msg = EmailMultiAlternatives(
        json_content["title"], json_content["content"], from_email, to_emails
    )
    body = loader.render_to_string("email/default.html", json_content)
    msg.attach_alternative(body, "text/html")
    return msg.send()
