from rest_framework.response import Response
from rest_framework import status

def badActionUser(request, reason):
    request.user.is_active = False
    request.user.msg = reason
    request.user.save()
    return {
        'code' : 'badActionUser',
        'message' : 'Bad Action performed! Your account will be de-activated. Please check your mail for further information.'
    }

error_bad_action_anon = {
    'code' : 'badActionAnon',
    'message' : 'Bad Action performed!'
}


def response_401_block_user(request, reason):
    request.user.msg = reason
    request.user.is_active = False
    request.user.save()
    return Response({'error': badActionUser}, status=status.HTTP_401_UNAUTHORIZED)
