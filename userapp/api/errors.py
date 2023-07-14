error_user_fields_empty = {
    'code' : 'userFieldsEmpty',
    'message' : 'Please fill the required user information!'
}

error_user_username_found = {
    'code' : 'userUsernameFound',
    'message' : 'Username already exists'
}

error_user_email_found = {
    'code' : 'userEmailFound',
    'message' : 'Email already exists'
}

error_user_username_email_found = {
    'code' : 'userUsernameEmailFound',
    'message' : 'Username and email already exists'
}

error_user_password_common = {
    'code' : 'userPasswordCommon',
    'message' : 'This password is too common.'
}

def userInvalid(): 
    return {
        'code' : 'userInvalid',
        'message' : 'User does not exist!'
    }

error_user_invalid_cred = {
    'code' : 'user_invalid_cred',
    'message' : 'Username or password is incorrect.'
}

def userInActive(): 
    return {
        'code' : 'userInActive',
        'message' : 'This account is not yet active.'
    }

def userNotVerified(): 
    return {
        'code' : 'userNotVerified',
        'message' : 'This account is not yet verified the identity.'
    }

def userInActiveNotVerified():
    return {
        'code' : 'userInActiveNotVerified',
        'message' : 'This account is not yet active, and not yet verified the identity.'
    }