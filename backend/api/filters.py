from django.contrib.auth import get_user_model
from django_filters import FilterSet, CharFilter, \
    AllValuesMultipleFilter, BooleanFilter

from foodgram.models import Recipe

User = get_user_model()


class RecipeFilter(FilterSet):
    author = CharFilter()
    tags = AllValuesMultipleFilter('tags__slug')
    is_favorited = BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
