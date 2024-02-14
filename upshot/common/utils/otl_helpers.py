from datetime import timedelta
from upshot.common.utils.redis_helpers import (
    redis_set_kvt,
    redis_get_key,
    redis_remove_key,
)
from upshot.common.utils.generators import generate_urlsafe_token
from upshot.common.utils import email_templates

from upshot.communications.tasks import celery_send_email


def get_otl_key(receiver):
    key = f"{receiver}_otl"
    return key


def generate_otl_for_receiver(receiver):
    otl = generate_urlsafe_token(28)
    lifetime = timedelta(hours=6)  # timedelta 6 hours from now
    receiver_key = get_otl_key(otl)
    otl_is_created = redis_set_kvt(receiver_key, receiver, lifetime)
    if otl_is_created:
        return otl

    return None


def get_otl_of_receiver(receiver):
    receiver_key = get_otl_key(receiver)
    otl_value = redis_get_key(receiver_key)
    return otl_value


def expire_otl(receiver):
    receiver_key = get_otl_key(receiver)
    expire_result = redis_remove_key(receiver_key)
    return expire_result


def verify_input_otl_of_receiver(receiver, input_otl):
    receiver_otl = get_otl_of_receiver(receiver)
    if receiver_otl and receiver_otl == input_otl:
        is_expired = expire_otl(receiver)
        return is_expired

    return None


def send_otl_to_receiver_email(receiver, link):
    try:
        token_data = {"link": link}
        email_content = email_templates.OTL.get("content")
        email_content = email_content.format(**token_data)
        json_content = {
            "title": "OTL Link",
            "content": email_content,
        }
        to_emails = [receiver]
        celery_result_object = celery_send_email.delay(json_content, to_emails)
        celery_result_object.wait(timeout=15)
        return celery_result_object.result

    except Exception:
        return False
