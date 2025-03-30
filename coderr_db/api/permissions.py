from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return request.user and (request.user.is_superuser or request.user == obj.user or request.user == obj.user.user)


class IsBusinessUser(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user.userprofil.type == 'business')


class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user.userprofil.type == 'customer')


class IsOwnerOrAdminOfOrder(BasePermission):
    def has_permission(self, request, view, instance):
        if request.user.is_superuser:
            return True
        if request.user.userprofil.type == 'business':
            return bool(request.user.userprofil.id == instance.business_user.id)


class IsOwnerOrAdminOfReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        return request.user.is_superuser or request.user.userprofil == obj.reviewer
