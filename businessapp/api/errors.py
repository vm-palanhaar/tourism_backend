from businessapp import models as OrgModel

def businessOrgFound():
    return {
        'code' : 'bussinessOrgFound_iDukaan',
        'message' : 'The registration number you entered already exists in our iDukaan app. Please double-check the registration number and try again. If you need further information or assistance, we recommend raising a request for more information.'
    }

def businessOrgNotVerified(orgName):
    return {
        'error' : {
            'code' : 'bussinessOrgNotVerified_iDukaan',
            'message' : f'Verficiation in-progess for {orgName}. Please check your registered mail for verification process.'
        }
    }

def businessOrgListNotFound():
    return {
        'code' : 'bussinessOrgListNotFound_iDukaan',
        'message' : 'You are not associated with organization. You can follow any one of the following point:\n\n'\
                    '- Add organization.\n'\
                    '- Request your manager to add you in organization.'
    }

def businessOrgEmpNotMng(orgName):
    return {
        'error' : {
            'code' : 'bussinessOrgEmpNotManager_iDukaan',
            'message' : f'You are not authorized to add/update/view specific resources in {orgName}!'
        }
    }

def businessOrgEmpSelfNotFound(orgId):
    response_data = {
        'error' : {
            'code' : 'businessSelfOrgEmpNotFound_iDukaan',
            'message' : 'You are no longer associated with {0}.'
        }
    }
    try:
        org = OrgModel.Org.objects.get(id = orgId)
        response_data['error']['message'] = response_data['error']['message'].format(org.name)
        return response_data
    except OrgModel.Org.DoesNotExist:
        response_data['error']['message'] = response_data['error']['message'].format('organization')
        return response_data

def businessOrgEmpFound(emp): 
    return {
        'error' : {
            'code' : 'businessOrgEmpFound_iDukaan',
        'message' : f'{emp.user.first_name} {emp.user.last_name} is already associated with {emp.org.name}'
        }
    }

def businessOrgEmpNotFound(orgName):
    return {
        'error' : {
            'code' : 'businessOrgEmpNotFound_iDukaan',
            'message' : f'User is no longer associated with {orgName}!'
        }
    }

def businessOrgEmpSelfUd(orgName):
    return {
        'error' : {
            'code' : 'businessOrgEmpSelfUd_iDukaan',
            'message' : f'You are not allowed to update or delete yourself from {orgName}!'
        }
    }

def businessOrgOpsFound():
    return{
        'error' : {
            'code' : 'businessOrgOpsFound_iDukaan',
        'message' : 'The registration number you entered already exists in our iDukaan app. Please double-check the registration number and try again. If you need further information or assistance, we recommend raising a request for more information.'
        }
    }

def businessOrgOpsNotFound(orgName):
    return {
        'error' : {
            'code' : 'businessOrgOpsNotFound_iDukaan',
            'message' : f'{orgName} do not have inter-state operations. Please add GSTIN for connecting with shops.'
        }
    }
