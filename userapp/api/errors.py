def userEmptyFields():
    return {
        'error' : {
            'code' : 'userFieldsEmpty',
            'message' : 'Please fill the required user information!'
        }
    }

def userUsernameFound():
    return {
        'error' : {
            'code' : 'userUsernameFound',
            'message' : 'Username already exists!'
        }
    }

def userEmailFound():
    return {
        'error' : {
            'code' : 'userEmailFound',
            'message' : 'Email already exists!'
        }
    }

def userUsernameEmailFound(): 
    return {
        'error' : {
            'code' : 'userUsernameEmailFound',
            'message' : 'Username and email already exists!'
        }
    }

def userPwdCommon():
    return {
        'error' : {
            'code' : 'userPwdCommonCommon',
            'message' : 'This password is too common!'
        }
    }

def userInvalid(): 
    return {
        'error' : {
            'code' : 'userInvalid',
            'message' : 'User does not exist!'
        }
    }

def userInvalidCred():
    return {
        'error' : {
            'code' : 'user_invalid_cred',
            'message' : 'Username or password is incorrect!'
        }
    }

def userInActive(): 
    return {
        'error' : {
            'code' : 'userInActive',
            'message' : 'You\'ve not verified registered email.'
        }
    }

def userNotVerified(): 
    return {
        'error' : {
            'code' : 'userNotVerified',
            'message' : 'You\'ve not verified your identity. Please verify your identity using the options shown on screen.'
        }
    }

def userInActiveNotVerified():
    return {
        'error' : {
            'code' : 'userInActiveNotVerified',
            'message' : 'This account is not yet active, and not yet verified the identity.'
        }
    }