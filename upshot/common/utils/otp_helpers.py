from upshot.common.utils.redis_helpers import (
    redis_set_kvt,
    redis_get_key,
    redis_remove_key,
)
from upshot.communications.tasks import (
    kavenegar_celery_send_sms,
    celery_send_email,
)
from . import email_templates, sms_templates
from .generators import generate_number


def get_otp_key(receiver):
    key = f"{receiver}_otp"
    return key


def generate_otp_for_receiver(receiver):
    otp = generate_number(5)
    lifetime = 300  # seconds
    receiver_key = get_otp_key(receiver)
    otp_is_created = redis_set_kvt(receiver_key, otp, lifetime)
    if otp_is_created:
        return get_otp_of_receiver(receiver)

    return None


def get_otp_of_receiver(receiver):
    receiver_key = get_otp_key(receiver)
    otp_value = redis_get_key(receiver_key)
    return otp_value


def expire_otp(receiver):
    receiver_key = get_otp_key(receiver)
    expire_result = redis_remove_key(receiver_key)
    return expire_result


def verify_input_otp_of_receiver(receiver, input_otp):
    receiver_otp = get_otp_of_receiver(receiver)
    if receiver_otp and receiver_otp == input_otp:
        is_expired = expire_otp(receiver)
        return is_expired

    return None


def send_otp_to_receiver_sms(receiver, otp):
    try:
        token_data = {"token": otp}
        celery_result_object = kavenegar_celery_send_sms.delay(
            receptor=receiver,
            template=sms_templates.OTP,
            token_data=token_data,
        )
        celery_result_object.wait(timeout=15)
        return celery_result_object.result

    except Exception:
        return False


def send_otp_to_receiver_email(receiver, otp):
    try:
        token_data = {"token": otp}
        email_content = email_templates.OTP.get("content")
        email_content = email_content.format(**token_data)
        json_content = {
            "title": "OTP Code",
            "content": email_content,
        }
        to_emails = [receiver]
        celery_result_object = celery_send_email.delay(json_content, to_emails)
        celery_result_object.wait(timeout=15)
        return celery_result_object.result

    except Exception:
        return False
