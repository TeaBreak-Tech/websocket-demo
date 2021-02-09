'''
core.py
    @post_token_auth_decorator
    to_dict()
'''

import logging
from user.models import *
from .http_response import *
import json
from itertools import chain
from datetime import datetime

# logger
logger = logging.getLogger('django')


def cookie_token_auth_decorator(func):
    def token_auth(request, *args,**kwargs):
        try:
            user = User.objects.get(uid=request.COOKIES.get("uid"))
        except User.DoesNotExist:
            return RESPONSE_USER_DO_NOT_EXIST
        if request.COOKIES.get("token") != user.token:
            return RESPONSE_TOKEN_NOT_MATCH
        if user.expired_date < datetime.now():
            return RESPONSE_TOKEN_EXPIRE
        if not user.is_active:
            return RESPONSE_INACTIVE_USER
        if user.identity not in ["student", "teacher", "admin"]:
            return RESPONSE_WRONG_IDENTITY
        return func(request, *args,**kwargs)
    return token_auth


def to_dict(instance, except_fields=[]):
    opts = instance._meta
    d = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        if f.name in except_fields:
            continue
        d[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        if f.name in except_fields:
            continue
        d[f.name] = [i.id for i in f.value_from_object(instance)]
    return d