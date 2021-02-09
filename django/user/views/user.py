from datetime import datetime, timedelta
from secrets import token_urlsafe
from django.http.response import HttpResponsePermanentRedirect, JsonResponse
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
import requests
from .core import *


# User
URL_PREFIX = 'https://qrcode.tea-break.cn/uauth/'
# URL_PREFIX = 'http://127.0.0.1:9000/uauth/'
TOKEN_LENGTH = 50
TOKEN_DURING_DAYS = 15
SESSION_AGE = 1e10


def private_render_request_response(requests_response: requests.Response) -> HttpResponse:
    return HttpResponse(
        content=requests_response.content,
        status=requests_response.status_code,
        content_type=requests_response.headers['Content-Type']
    )


@ require_http_methods(["POST"])
def register(request):
    body_dict = json.loads(request.body.decode('utf-8'))
    r = requests.post(url=URL_PREFIX+'register/', json=body_dict)
    response = private_render_request_response(r)
    if r.status_code == 200:
        user = User(uid=r.json().get("uid"))
        user.token = token_urlsafe(TOKEN_LENGTH)
        user.expired_date = datetime.now() + timedelta(days=TOKEN_DURING_DAYS)
        user.is_active = r.json().get("is_active")
        user.identity = r.json().get("identity")
        user.save()
        response.set_cookie("token", user.token, max_age=SESSION_AGE)
        response.set_cookie("is_login", "true", max_age=SESSION_AGE)
        response.set_cookie("uid", user.uid, max_age=SESSION_AGE)
    return response


@ require_http_methods(["POST"])
def login(request):
    body_dict = json.loads(request.body.decode('utf-8'))
    r = requests.post(url=URL_PREFIX+'login/', json=body_dict)
    response = private_render_request_response(r)
    if r.status_code == 200:
        try:
            user = User.objects.get(uid=r.json().get("uid"))
            if not user.is_active:
                return RESPONSE_INACTIVE_USER_JSON({"uid": user.uid})  # 403 U-INA
        except User.DoesNotExist:
            # 在本平台上没有注册，立刻注册
            user = User(uid=r.json().get("uid"))
        # refresh token
        user.token = token_urlsafe(TOKEN_LENGTH)
        user.expired_date = datetime.now() + timedelta(days=TOKEN_DURING_DAYS)
        user.save()
        response.set_cookie("token", user.token, max_age=SESSION_AGE)
        response.set_cookie("is_login", "true", max_age=SESSION_AGE)
        response.set_cookie("uid", user.uid, max_age=SESSION_AGE)
    return response


@ require_http_methods(["GET"])
def is_login(request):
    try:
        user = User.objects.get(uid=request.COOKIES.get("uid"))
        if request.COOKIES.get("token") != user.token:
            return RESPONSE_TOKEN_NOT_MATCH  # 403 T-DNM
        if user.expired_date < datetime.now():
            return RESPONSE_TOKEN_EXPIRE  # 403 T-EXP
        if not user.is_active:
            return RESPONSE_INACTIVE_USER_JSON({"uid": user.uid})
        response = JsonResponse({"uid": user.uid})  # 200
        # refresh token
        user.token = token_urlsafe(TOKEN_LENGTH)
        user.expired_date = datetime.now() + timedelta(days=TOKEN_DURING_DAYS)
        user.save()
        response.set_cookie("token", user.token, max_age=SESSION_AGE)
        response.set_cookie("is_login", "true", max_age=SESSION_AGE)
        response.set_cookie("uid", user.uid, max_age=SESSION_AGE)
        return response
    except User.DoesNotExist:
        return RESPONSE_USER_DO_NOT_EXIST  # 404 U-DNE
    except:
        raise


@ require_http_methods(["POST"])
def send_validate_email(request):
    try:
        body_dict = json.loads(request.body.decode('utf-8'))
        r = requests.post(url=URL_PREFIX+'email/send/', json=body_dict)
        response = private_render_request_response(r)
        if r.status_code == 200:
            user = User.objects.get(uid=r.json().get("uid"))
            user.is_active = r.json().get("is_active")
            user.identity = r.json().get("identity")
            user.save()
        return response
    except Exception as e:
        raise e


@ require_http_methods(["POST"])
def validate_email_code(request):
    try:
        body_dict = json.loads(request.body.decode('utf-8'))
        r = requests.post(url=URL_PREFIX+'email/code/', json=body_dict)
        response = private_render_request_response(r)
        if r.status_code == 200:
            user = User.objects.get(uid=r.json().get("uid"))
            user.is_active = r.json().get("is_active")
            user.identity = r.json().get("identity")
            user.save()
        return response
    except Exception as e:
        raise e


@ require_http_methods(["GET", "POST"])
def read(request):
    def post_is_read(request):
        try:
            user = User.objects.get(uid=request.COOKIES.get("uid"))
            user.is_read = True
            user.save()
            return HttpResponse("user has read")
        except User.DoesNotExist:
            return RESPONSE_USER_DO_NOT_EXIST
        except:
            raise

    def get_is_read(request):
        try:
            user = User.objects.get(uid=request.COOKIES.get("uid"))
            if user.is_read:
                return HttpResponse("user has read")
            else:
                return HttpResponse("user has not read!", status=403)
        except User.DoesNotExist:
            return RESPONSE_USER_DO_NOT_EXIST
        except:
            raise
    if request.method == "POST":
        return post_is_read(request)
    elif request.method == "GET":
        return get_is_read(request)
