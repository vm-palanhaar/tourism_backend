def geographyStatesListEmpty(countryId): 
    return {
        'error' : {
            {
            'code' : 'geoStatesNotFound',
            'message' : f'States data not available for {countryId}'
        }
        }
    }