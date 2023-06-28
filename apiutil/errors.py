from rest_framework.response import Response
from rest_framework import status

error_bad_action_user = {
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
    return Response({'error': error_bad_action_user}, status=status.HTTP_401_UNAUTHORIZED)
