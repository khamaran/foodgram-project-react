from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import MyUser
from .constants import NAME_MAX_LENGTH, COLOR_MAX_LENGTH
from django.conf import settings


class Tag(models.Model):
    """Модель Тэга."""
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name='Тэг',
                            unique=True)
    color = models.CharField(max_length=COLOR_MAX_LENGTH, unique=True,
                             verbose_name='Цвета тэга')
    slug = models.SlugField(unique=True, max_length=NAME_MAX_LENGTH)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (цвет: {self.color})"


class Ingredient(models.Model):
    """Модель Ингредиентов."""
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Ингредиент')
    measurement_unit = models.CharField(max_length=NAME_MAX_LENGTH,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    """Модель Рецепта."""
    name = models.CharField(max_length=NAME_MAX_LENGTH,
                            verbose_name='Название рецепта')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               verbose_name='Автор')
    image = models.ImageField(
        'Картинка',
        upload_to=settings.IMAGE_UPLOAD_PATH
    )
    text = models.TextField(verbose_name='Описание',
                            help_text='Введите описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientAmount',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1,
                                      message='Минимальное '
                                              'время '
                                              'приготовления 1 минута!')]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f' {self.name}. Автор рецепта: {self.author}'


class IngredientAmount(models.Model):
    """Модель связи количества Ингредиентов в Рецепте."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   verbose_name='Ингредиенты')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredient_amount',
                               verbose_name='Рецепт')
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, message='В списке '
                                         'должен быть хотя '
                                         'бы один ингредиент!')]
    )

    class Meta:
        ordering = ['ingredient']
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='ingredient_unique_amount_in_recipe'
            )
        ]

    def __str__(self):
        return f"{self.amount} {self.ingredient}"


class ShoppingCart(models.Model):
    """Модель Списка покупок."""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'{self.user} добавил(а) "{self.recipe}" в Список покупок!'


class Favorite(models.Model):
    """Модель добавления Рецепта в Избранное."""
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user} добавил(а) "{self.recipe}" в Избранное!'
