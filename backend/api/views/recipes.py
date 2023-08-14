from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers.recipes import (FavoriteSerializer, IngredientSerializer,
                                     RecipeGETSerializer, RecipeSerializer,
                                     ShoppingCartSerializer, TagSerializer)
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)

from ..filters import IngredientSearchFilter, RecipeFilter
from ..pagination import CustomPageNumberPagination
from ..permissions import AuthorOrReadOnly
from ..utils_shopping_cart_pdf import create_shopping_cart


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для создания обьектов класса Tag."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для создания обьектов класса Ingredient."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания обьектов класса Recipe."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, AuthorOrReadOnly
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    @staticmethod
    def favorite_shopping_cart(serilizers, request, pk):
        """Общий метод добавления рецептов (ингредиентов) в избранное."""
        context = {'request': request}
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        serializer = serilizers(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['post'],
        url_path='favorite',
        url_name='favorite',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        """Позволяет текущему пользователю добавлять рецепты в избранное."""
        return self.favorite_shopping_cart(FavoriteSerializer, request, pk)

    @favorite.mapping.delete
    def destroy_favorite(self, request, pk):
        """Позволяет текущему пользователю удалять рецепты в избранное."""
        get_object_or_404(
            Favorite,
            user=request.user,
            recipe=get_object_or_404(Recipe, pk=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['post'],
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        """Позволяет текущему пользователю добавлять рецепты
        в список покупок."""
        return self.favorite_shopping_cart(
            ShoppingCartSerializer,
            request,
            pk
        )

    @shopping_cart.mapping.delete
    def destroy_shopping_cart(self, request, pk):
        """Позволяет текущему пользователю удалять рецепты
        из списка покупок."""
        get_object_or_404(
            ShoppingCart,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, pk=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Позволяет текущему пользователю загрузить список покупок."""
        ingredients_cart = (
            IngredientAmount.objects.filter(
                recipe__shopping_list__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit',
            ).annotate(ingredient_value=Sum('amount'))
            .order_by(
                'ingredient__name'
            )
        )
        return create_shopping_cart(ingredients_cart)

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        для разных типов запроса."""
        if self.request.method == 'GET':
            return RecipeGETSerializer
        return RecipeSerializer
