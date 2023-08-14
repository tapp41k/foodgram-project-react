from django.conf import settings
from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс настройки раздела тегов."""

    list_display = (
        'pk',
        'name',
        'color',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс настройки раздела ингредиентов."""

    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name',)


class IngredientAmountInline(admin.TabularInline):
    """Класс, позволяющий добавлять ингредиенты в рецепты."""

    model = IngredientAmount
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс настройки раздела рецептов."""

    list_display = (
        'pk',
        'name',
        'author',
        'text',
        'get_tags',
        'get_ingredients',
        'cooking_time',
        'image',
        'pub_date',
        'count_favorite',
    )
    inlines = [
        IngredientAmountInline,
    ]

    empty_value_display = 'значение отсутствует'
    list_editable = ('author',)
    list_filter = ('author', 'name', 'tags')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('author__username', 'name',)

    def get_ingredients(self, object):
        """Получает ингредиент или список ингредиентов рецепта."""
        return '\n'.join(
            (ingredient.name for ingredient in object.ingredients.all())
        )

    get_ingredients.short_description = 'ингредиенты'

    def get_tags(self, object):
        """Получает тег или список тегов рецепта."""
        return '\n'.join((tag.name for tag in object.tags.all()))

    get_tags.short_description = 'теги'

    def count_favorite(self, object):
        """Вычисляет количество добавлений рецепта в избранное."""
        return object.favorites.count()

    count_favorite.short_description = 'Количество добавлений в избранное'


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    """Класс настройки соответствия игредиентов и рецептов."""

    list_display = (
        'pk',
        'ingredient',
        'amount',
        'recipe'
    )
    empty_value_display = 'значение отсутствует'
    list_per_page = settings.LIST_PER_PAGE


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Класс настройки раздела избранного."""

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'значение отсутствует'
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user__username',)
    list_per_page = settings.LIST_PER_PAGE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Класс настройки раздела рецептов, которые добавлены в список покупок."""

    list_display = (
        'pk',
        'user',
        'recipe',
    )

    empty_value_display = 'значение отсутствует'
    list_editable = ('user', 'recipe')
    list_filter = ('user',)
    search_fields = ('user__username',)
    list_per_page = settings.LIST_PER_PAGE
