from django.contrib import admin

from .models import Ingredient, Tag, Recipe, ShoppingCart, Favorite, IngredientAmount


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_number')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientAmountInline, )

    def favorites_number(self, obj):
        if Favorite.objects.filter(recipe=obj).exists():
            return Favorite.objects.filter(recipe=obj).count()
        return 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(ShoppingCart)
admin.site.register(Favorite)
