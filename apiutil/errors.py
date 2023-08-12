from rest_framework.response import Response
from rest_framework import status

def badActionUser(request, reason):
    request.user.is_active = False
    request.user.msg = reason
    request.user.save()
    return {
        'error' : {
            'code' : 'badActionUser',
            'message' : 'You\'ve been blocked to access the platform due to security violations!'
        }
    }

def bodyEmptyFields():
    return {
        'error' : {
            'code' : 'bodyEmptyFields',
            'message' : 'Please fill the required information!'
        }
    }

error_bad_action_anon = {
    'code' : 'badActionAnon',
    'message' : 'Bad Action performed!'
}
