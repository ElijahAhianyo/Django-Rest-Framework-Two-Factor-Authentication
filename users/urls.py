from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from users import views as user_view

generate_totp = user_view.UserLoginGenerateOTP.as_view({
    'post': 'generate_totp',
})

verify_otp = user_view.UserLoginGenerateOTP.as_view({
    'post': 'verify_otp',
})

urlpatterns = [
    url(r'^users/login/otp/$',
        generate_totp,
        name='generate-totp'),
    url(r'^users/login/otp/verify$',
        verify_otp,
        name='verify-otp'),
   
]

urlpatterns = format_suffix_patterns(urlpatterns)
