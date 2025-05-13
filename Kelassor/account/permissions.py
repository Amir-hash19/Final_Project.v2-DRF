from rest_framework.permissions import BasePermission




def GroupPermission(*group_names):
    class _DynamicGroupPermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False

            return request.user.groups.filter(name__in=group_names).exists()
    return _DynamicGroupPermission





def is_supportpanel_user(user):
    return user.groups.filter(name="SupportPanel").exists()
