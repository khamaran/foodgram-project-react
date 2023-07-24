from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import filters, status
from rest_framework import viewsets

from foodgram.models import Tag, Recipe, Ingredient, \
    IngredientAmount, ShoppingCart, Favorite
from rest_framework.status import HTTP_204_NO_CONTENT
from users.models import Follow, MyUser

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .filters import RecipeFilter
from .serializers import TagSerializer, RecipeCreateSerializer, IngredientSerializer, \
    ShortRecipeSerializer, RecipeReadSerializer, MyUserSerializer, FollowSerializer
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
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'ingredients_in_recipe_amount__ingredient', 'tags'
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

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'GET':
            return self.get_obj(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Favorite, request.user, pk)
        return None

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
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
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name',)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = RecipePagination

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=['POST', 'DELETE']
    )
    def follow(self, request, id):
        user = request.user
        following = get_object_or_404(MyUser, id=id)
        if request.method == 'DELETE':
            follow = get_object_or_404(
                Follow, user=user, following=following
            )
            follow.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        if Follow.objects.filter(user=user, following=following).exists():
            return Response(
                {'errors': 'Вы уже подписаны на этого пользователя!'},
                status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.create(user=user, following=following)
        data = FollowSerializer(follow)
        return Response(data.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=['GET']
    )
    def followers(self, request):
        user = request.user
        queryset = MyUser.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
