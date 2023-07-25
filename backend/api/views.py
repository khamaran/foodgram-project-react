from django.conf import settings
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import utils
from django_filters.rest_framework import DjangoFilterBackend
from djoser.compat import get_user_email
from djoser.views import UserViewSet
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import filters, status, generics
from rest_framework import viewsets

from foodgram.models import Tag, Recipe, Ingredient, \
    IngredientAmount, ShoppingCart, Favorite
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from users.models import Follow, MyUser

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from .filters import RecipeFilter
from .serializers import TagSerializer, RecipeCreateSerializer, IngredientSerializer, \
    ShortRecipeSerializer, RecipeReadSerializer, MyUserSerializer, MyUserCreateSerializer, \
    FollowSerializer, ChangePasswordSerializer
from .permissions import IsAdminOrReadOnly, IsUserOrReadOnly
from .pagination import RecipePagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = (IsUserOrReadOnly,)
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'ingredient_amount__ingredient', 'tags'
        )
        return recipes

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_obj(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({
                'errors': 'Вы уже добавили этот рецепт к себе в список!'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Вы уже удалили этот рецепт!'
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.get_obj(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self.get_obj(ShoppingCart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(ShoppingCart, request.user, pk)
        return None

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientAmount.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(quantity=Sum('amount'))
        shopping = 'Список покупок\n'
        shopping += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["quantity"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(shopping,
                                'Content-Type: application/pdf')
        response[
            "Content-Disposition"
        ] = 'attachment; filename="shopping.pdf"'
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class MyUserViewSet(UserViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = RecipePagination
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return MyUserSerializer
        return MyUserCreateSerializer

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def set_password(self, request, id=None):
        user = self.request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, id=None):
        serializer = MyUserSerializer(
            MyUser.objects.filter(username=self.request.user),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        following = get_object_or_404(MyUser, id=id)
        follower = self.request.user
        if request.method == 'POST':
            if request.user == following:
                return Response({
                    'errors': 'Вы не можете подписываться на самого себя!'
                }, status=status.HTTP_400_BAD_REQUEST)

            if Follow.objects.filter(following=following,
                                     follower=follower).exists():
                return Response({
                    'errors': f'Вы уже подписанны на автора {following}'
                }, status=status.HTTP_400_BAD_REQUEST)

            new_follow = Follow.objects.create(
                following=following,
                follower=follower
            )
            serializer = FollowSerializer(
                new_follow,
                context={'request': request}
            )
            return Response(serializer.data)
        if request.method == 'DELETE':
            subscription = get_object_or_404(Follow, following=following, follower=follower)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        follower = request.user
        queryset = Follow.objects.filter(follower=follower)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
