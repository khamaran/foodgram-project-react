from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, MyUserViewSet, FollowersViewSet

app_name = 'api'

router = DefaultRouter()
router_1 = DefaultRouter()
router_1.register(
    r'users/subscriptions',
    FollowersViewSet,
    basename='subscriptions')

router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'users', MyUserViewSet, basename='user')

urlpatterns = [
    # path('api/users/set_password/', ChangePasswordView.as_view()),
    path('', include(router.urls)),
    path('', include(router_1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
