from rest_framework.permissions import BasePermission

class IsVerified(BasePermission):
    message = 'DigiLocker'
    def has_permission(self, request, view):
       return request.user.is_verified
