from rest_framework import permissions

class IsViewerReadOnly(permissions.BasePermission):
    """Allow read-only access for viewers. Staff/Admins get full access"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        role=request.user.profile.role
        if role == 'viewer' and request.method in permissions.SAFE_METHODS:
            return True    
        return role in ['staff','admin']


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow owners of the object to edit it."""
    def has_object_permission(self, request, view, obj):
        # Read permission allowed to any request
        
        if request.method in permissions.SAFE_METHODS:
            return True

        #Write permissions are only allowed to the owners.
        return obj.owner==request.user

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role =='admin'

class IsStaffOrAdmin(permissions.BasePermission):
    def  has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role in ['admin','staff']    