from django.contrib import admin

from .models import Ingredient, Tag, Recipe, ShoppingCart, \
    Favorite


class IngredientAmountInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_number')
    search_fields = ['name', 'author__username']
    list_filter = ['tags']
    inlines = (IngredientAmountInline, )

    @admin.display(description='В избранном')
    def favorites_number(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ['name', 'slug']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ['name']


admin.site.register(ShoppingCart)
admin.site.register(Favorite)
