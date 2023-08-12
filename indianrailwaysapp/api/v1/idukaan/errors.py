from indianrailwaysapp import models as IrModel

def irShopLicFound():
    return {
        'error' : {
            'code' : 'irShopLicFound_iDUkaan',
            'message' : 'The registration number you entered already exists in our iDukaan app. Please double-check the registration number and try again. If you need further information or assistance, we recommend raising a request for more information.'
        }
    }

def irOrgShopListEmptyMng():
    return {
        'error' : {
            'code' : 'irOrgShopListEmptyMng_iDukaan',
            'message' : 'Shops/Stalls are not registered on iDukaan.'
        } 
    }

def irOrgShopListEmptyNotMng():
    return {
        'error' : {
            'code' : 'irOrgShopListEmptyNotMng_iDukaan',
            'message' : 'You are not associated with shop/stall on railway station. Please raise a request to your manager to add you in shop.'
        }
    }

def irOrgShopEmpNotMng(shopName):
    return  {
        'error' : {
            'code' : 'irOrgShopEmpNotMng_iDukaan',
            'message' : f'You are not authorized to add/update/view specific resources in {shopName}.'
        }
    }

def irOrgShopListEmpty():
    return {
        'error' : {
            'code' : 'irOrgShopsNotFound_iDukaan',
            'message' : 'You are not associated with shop/stall on railway station. Note: This window shows the list of shops you are connected as an employee.'
        }
    }

def irOrgShopEmpSelfNotFound():
    return {
        'error' : {
            'code' : 'irOrgShopEmpSelfNotFound_iDukaan',
            'message' : 'You are no longer associated with shop/stall.'
        }
    }

def irOrgShopNotFound():
    return {
        'error' : {
            'code' : 'irOrgShopNotFound_iDukaan',
            'message' : 'This shop/stall had been deleted from iDukaan.'
        }
    }

def irOrgShopInActive(shopName):
    return {
        'error' : {
            'code' : 'irOrgShopInActive_iDukaan',
            'message' : f'{shopName} is not active due Shop/FSSAI license expiry.'
        }
    }

def irOrgShopInActiveNotVerified(shopName):
    return {
        'error' : {
            'code' : 'irOrgShopInActiveNotVerified_iDukaan',
            'message' : f'Verficiation stopped as {shopName} is not active due Shop/FSSAI license expiry.'
        }
    }

def irOrgShopNotVerified(shopName):
    return {
        'error' : {
            'code' : 'irOrgShopNotVerified_iDukaan',
            'message' : f'Verficiation in-progess for {shopName}. We will verify the details provided within 24HRS.'
        }
    }
    
def irOrgShopAddEmpFound(orgShopEmp):
    return {
        'error' : {
            'code' : 'irOrgShopAddEmpFound_iDukaan',
            'message' : f'{orgShopEmp.user.first_name} {orgShopEmp.user.last_name} is already associated with {orgShopEmp.shop.name}'
        }
    }


def irOrgShopEmpNotFound(empName, shopName):
    return {
        'error' : {
            'code' : 'irOrgShopEmpNotFound_iDukaan',
            'message' : f'{empName} is no longer associated with {shopName}.'
        }
    }

def irOrgShopEmpSelfUd(shopName):
    return {
        'error' : {
            'code' : 'irOrgShopEmpSelfUd_iDukaan',
            'message' : f'You are not allowed to update or delete yourself from {shopName}'
        }
    }

def irShopLicNotFound():
    return {
        'error' : {
            'code' : 'irShopLicNotFound_iDukaan',
            'message' : 'Shop/Stall license or notice is not available.'
        }
    }

def irShopFssaiLicFound():
    return {
        'error' : {
            'code' : 'irShopFssaiLicFound_iDukaan',
            'message' : 'The registration number you entered already exists in our iDukaan app. Please double-check the registration number and try again. If you need further information or assistance, we recommend raising a request for more information.'
        }
    }

def irShopFssaiLicNotFoundEmpMng():
    return {
        'error' : {
            'code' : 'irShopFssaiLicNotFound_iDukaan',
            'message' : 'Shop/Stall FSSAI license is not available. Please add the license for verification process in case of catering business.'
        }
    }

def irShopFssaiLicNotFoundEmpNonMng(shopName):
    return {
        'error' : {
            'code' : 'irShopFssaiLicNotFound_iDukaan',
            'message' : f'Shop/Stall FSSAI license is not available. You are not authorized to add/update/view specific resources in {shopName}.'
        }
    }

def irShopInvIsNotFound():
    return {
        'error' : {
            'code' : 'irShopInvIsNotFound_iDukaan',
            'message' : 'Products are not yet added or out of stock!'
        }
    }

def irShopInvOsNotFound():
    return {
        'error' : {
            'code' : 'irShopInvOsNotFound_iDukaan',
            'message' : 'Products are not yet added or in stock!'
        }
    }

def irShopInvProdIsFound():
    return{
        'error' : {
            'code' : 'irShopInvIsFound_iDukaan',
            'message' : 'Product is listed under in-stock page!'
        }
    }

def irShopInvProdOsFound():
    return {
        'error' : {
            'code' : 'irShopInvOsFound_iDukaan',
            'message' : 'Product is listed under out-stock page!'
        }
    }

def irShopInvNotFound(shopName):
    return {
        'error' : {
            'code' : 'irShopInvNotFound_iDukaan',
            'message' : f'Product is no longer available at {shopName}!'
        }
    }

def irShopGstFound(shopName, gstin):
    return {
        'error' : {
            'code' : 'irShopGstFound_iDukaan',
            'message' : f'{shopName} is already associated with GSTIN {gstin}!'
        }
    }

def irShopGstNotFound(shopName):
    return {
        'error' : {
            'code' : 'irShopGstNotFound_iDukaan',
            'message' : f'{shopName} is not associated with GSTIN!'
        }
    }
