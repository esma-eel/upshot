from django.conf import settings
from kavenegar import KavenegarAPI
from upshot.adminstration.models import APIKey


def kavenegar_send_sms(receptor, template, token_data):
    apikey_qs = APIKey.objects.filter(code="sms_provider_key")
    if not apikey_qs.exists():
        return "failed, there is no sms apikey"

    apikey_object = apikey_qs.last()
    api = KavenegarAPI(apikey_object.key)

    params = {"receptor": receptor, "template": template, **token_data}

    try:
        response = api.verify_lookup(params)
        return response
    except Exception as e:
        print(e)
