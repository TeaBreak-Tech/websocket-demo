'''
http_response.py
    predefined HttpResponse
'''

from django.http import HttpResponse
from django.http.response import JsonResponse


# predefined HttpResponse
RESPONSE_INVALID_PARAM = HttpResponse(content="Invalid parameter", status=400, reason="I-PAR")
RESPONSE_BLANK_PARAM = HttpResponse(content="Blank or missing required parameter", status=400, reason="B-PAR")

RESPONSE_TOKEN_EXPIRE = HttpResponse(content="Token expire", status=403, reason="T-EXP")
RESPONSE_WRONG_EMAIL_CODE = HttpResponse(content="Wrong email code", status=403, reason="W-EMC")
RESPONSE_AUTH_FAIL = HttpResponse(content="Not Authorized", status=403, reason="N-AUTH")
RESPONSE_EXIST_DEPENDENCY = HttpResponse(content="Exist dependency", status=403, reason="E-DEP")
RESPONSE_UNIQUE_CONSTRAINT = HttpResponse(content="Not satisfy unique constraint", status=403, reason="N-UNI")
RESPONSE_FAIL_SEND_EMAIL = HttpResponse(content="Fail to send email", status=403, reason="E-FTS")
RESPONSE_WRONG_PASSWORD = HttpResponse(content="Wrong password", status=403, reason="W-PWD")
RESPONSE_TOKEN_NOT_MATCH = HttpResponse(content="Token does not match user", status=403, reason="T-DNM")
RESPONSE_INACTIVE_USER = HttpResponse(content="Inactive user, need to validate email", status=403, reason="U-INA")


def RESPONSE_INACTIVE_USER_JSON(body):
    return JsonResponse(body, status=403, reason="U-INA")


RESPONSE_WRONG_IDENTITY = HttpResponse(content="User wrong identity", status=403, reason="U-WID")

RESPONSE_USER_DO_NOT_EXIST = HttpResponse(content="User do not exist", status=404, reason="U-DNE")
RESPONSE_QUESTION_DO_NOT_EXIST = HttpResponse(content="Question do not exist", status=404, reason="Q-DNE")
RESPONSE_MESSAGE_DO_NOT_EXIST = HttpResponse(content="Message do not exist", status=404, reason="M-DNE")
RESPONSE_ANSWER_DO_NOT_EXIST = HttpResponse(content="Answer do not exist", status=404, reason="A-DNE")
RESPONSE_COMMENT_DO_NOT_EXIST = HttpResponse(content="Comment do not exist", status=404, reason="C-DNE")
RESPONSE_HANDBOOK_DO_NOT_EXIST = HttpResponse(content="Handbook do not exist", status=404, reason="H-DNE")
RESPONSE_DRAFT_DO_NOT_EXIST = HttpResponse(content="Draft do not exist", status=404, reason="D-DNE")
RESPONSE_APPLICANT_DO_NOT_EXIST = HttpResponse(content="Applicant do not exist", status=404, reason="AP-DNE")
RESPONSE_APPENDIX_DO_NOT_EXIST = HttpResponse(content="Applicant do not exist", status=404, reason="APD-DNE")

RESPONSE_UNKNOWN_ERROR = HttpResponse(content="Unknown error", status=500, reason="U-ERR")