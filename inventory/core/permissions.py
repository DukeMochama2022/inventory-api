from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to allow owners of the object to edit it."""
    def has_object_permission(self, request, view, obj):
        # Read permission allowed to any request
        
        if request.method in permissions.SAFE_METHODS:
            return True

        #Write permissions are only allowed to the owners.
        return obj.owner==request.user