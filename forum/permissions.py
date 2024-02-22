from rest_framework import permissions



# ! Custom Permission
class IsUserObjectOrAdminPermission(permissions.BasePermission):
    """
    Custom Permission Which let only authenticated users
    to perform POST method and only the user who created
    the object or admin user has to permissions to delete
    specific object
    """

    def has_permission(self, request, view):
        """
        Overriding the has permissions to allow all user 
        to perform safe method and to perform other method
        other than safe method user needs to authenticated
        """
        if request.method in permissions.SAFE_METHODS:
            return True 
        return bool(request.user.is_authenticated)
    
    
    def has_object_permission(self, request, view, obj):
        """
        Over Riding the permissions for a object 
        so that only the user who created the object
        and admin users can perform other methods on it
        """
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        return bool(
            obj.user==request.user or
            request.user.is_staff or
            request.user.is_superuser
        )
    
