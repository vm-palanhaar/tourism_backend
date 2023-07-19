train_not_found = {
    'code' : 'trainNotFound_Yatrigan',
    'message' : 'Train not found!'
}

def irShopListInActiveNotVerified(stationName, stationCode):
    return {
        'code' : 'irShopListInActiveNotVerifiedEmpty_Yatrigan',
        'message' : f'Verification in-progress for stalls/shops found at {stationName} - {stationCode}.'
    }

def irShopListEmpty(stationName, stationCode):
    return {
        'code' : 'irShopListEmpty_Yatrigan',
        'message' : f'Stalls/Shops not found at {stationName} - {stationCode}. Following may be the reasons as stalls/shops are:\n\n'
                    '- not present on this station.\n'
                    '- not registered on iDukaan.'
    }

def irShopInvListEmpty():
    return {
        'code' : 'irShopInvListEmpty_Yatrigan',
        'message' : 'Products are not listed/available on this stall/shop!'
    }