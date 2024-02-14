from celery import shared_task
from .utils.sms import kavenegar_send_sms
from .utils.email import send_email


@shared_task
def kavenegar_celery_send_sms(
    receptor,
    template,
    token_data,
):
    try:
        response = kavenegar_send_sms(receptor, template, token_data)
        if response[0]["status"] in [4, 5]:
            return True
        else:
            return False
    except Exception:
        return False


@shared_task
def celery_send_email(
    json_content,
    to_emails,
):
    try:
        response = send_email(
            to_emails,
            json_content,
        )
        if response == 1:
            return True
        else:
            return False
    except Exception:
        return False
