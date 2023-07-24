from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

from users.models import MyUser


class IsAdminOrReadOnly(BasePermission):
    """Разрешение редактирования только Админу."""

    def has_permission(self, request: Request, view: None) -> bool:
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.role == MyUser.ADMIN or request.user.is_superuser)
        )


class IsUserOrReadOnly(BasePermission):
    """Разрешение редактирования только Автору. """

    def has_permission(self, request: Request, view: None) -> bool:
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request: Request, view: None, obj) -> bool:
        return request.method in SAFE_METHODS or obj.author == request.user