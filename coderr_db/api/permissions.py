from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return request.user and (request.user.is_superuser or request.user == obj.user.user)


class IsBusinessUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return bool(request.user.userprofil.type == 'business')


class IsCustomerUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return bool(request.user.userprofil.type == 'customer')
