from rest_framework.permissions import BasePermission

class IsVerified(BasePermission):
    message = 'DigiLocker'
    def has_permission(self, request, view):
       if request.user.is_verified == True:
           pass
       return request.user.is_verified
