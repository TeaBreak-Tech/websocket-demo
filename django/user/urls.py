from logging import log
from django.urls import path


from user.views.user import *

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('is_login/', is_login),
    path('email/send/', send_validate_email),
    path('email/code/', validate_email_code),
    path('read/', read)
]
