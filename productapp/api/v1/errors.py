def pcBrandSearchListEmpty(brandName): 
    return {
        'error' : {
            'code' : 'pcBrandSearchListEmpty_iDukaan',
            'message' : f'Brands with {brandName} keyword not found in the community.\n\n'\
                '- Please try again with another keyword.'\
                '- Add the manufacturer\'s brand to the community.'
        }
    }

def pcBrandListEmpty(): 
    return {
        'error' : {
            'code' : 'pcBrandListEmpty_iDukaan',
            'message' : f'Brands not found in the community. Add the manufacturer\'s brand to the community.'
        }
    }

def pcBrandActiveListEmpty(): 
    return {
        'error' : {
            'code' : 'pcBrandActiveListEmpty_iDukaan',
            'message' : f'Verified brands not found in the community.\n\n'\
                '- Verifications are in-progress for brands.'\
                '- Add the manufacturer\'s brand to the community.'
        }
    }

def pcBrandInActiveListEmpty(): 
    return {
        'error' : {
            'code' : 'pcBrandInActiveListEmpty_iDukaan',
            'message' : f'Non verified brands not found in the community.\n\n'\
                '- Verifications had been completed for all the brands.'\
                '- Add the manufacturer\'s brand to the community.'
        }
    }

def pcBrandNotFound(): 
    return {
        'error' : {
            'code' : 'pcBrandNotFound_iDukaan',
            'message' : 'Brand no longer exist!'
        }
    }

def pcBrandProdListEmpty(brandName): 
    return {
        'error' : {
            'code' : 'pcBrandProdSearchListEmpty_iDukaan',
            'message' : f'{brandName}\'s products not found in the community.\n\n'\
                f'- Add the product for {brandName} to the community.'
        }
    }

def pcBrandProdSearchListEmpty(prodName, brandName): 
    return {
        'error' : {
            'code' : 'pcBrandProdSearchListEmpty_iDukaan',
            'message' : f'{brandName}\'s products with {prodName} keyword not found in the community.\n\n'\
                '- Please try again with another keyword.'\
                f'- Add the product for {brandName} to the community.'
        }
    }

def pcBrandProdActiveListEmpty(brandName):
    return {
        'error' : {
            'code' : 'pcBrandProdActiveListEmpty_iDukaan',
            'message' : f'Verified products for {brandName} not found in the community.\n\n'\
                f'- Verifications are in-progress for {brandName}\'s products.'\
                f'- Add the product for {brandName} to the community.'
        }
    }

def pcBrandProdInActiveListEmpty(brandName): 
    return {
        'error' : {
            'code' : 'pcBrandProdInActiveListEmpty_iDukaan',
            'message' : f'Non verified products for {brandName} not found in the community.\n\n'\
                f'- Verifications had been completed for all the {brandName}\'s products.'\
                f'- Add the product for {brandName} to the community.'
        }
    }

def pcBrandProdSubGroupListEmpty(brandName): 
    return {
        'error' : {
            'code' : 'pcBrandProdSubGroupListEmpty_iDukaan',
            'message' : f'{brandName}\'s products with this category not found in the community.\n\n'\
        }
    }