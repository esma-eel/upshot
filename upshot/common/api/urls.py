from django.urls import path
from .otp import views as otp_views


app_name = "api-common"

otp_urlpatterns = [
    # otp
    path(
        "otp/phone/create/",
        otp_views.RequestOTPPhoneApiView.as_view(),
        name="otp-phone-create",
    ),
    path(
        "otp/phone/verify/",
        otp_views.VerifyOTPPhoneApiView.as_view(),
        name="otp-phone-verify",
    ),
    path(
        "otp/email/create/",
        otp_views.RequestOTPEmailApiView.as_view(),
        name="otp-email-create",
    ),
    path(
        "otp/email/verify/",
        otp_views.VerifyOTPEmailApiView.as_view(),
        name="otp-email-verify",
    ),
]

urlpatterns = [] + otp_urlpatterns
