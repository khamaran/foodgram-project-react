from django_filters import FilterSet, \
    AllValuesMultipleFilter, NumberFilter

from foodgram.models import Recipe


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter('tags__slug')
    is_favorited = NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = NumberFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user.id)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user.id)
        return queryset
