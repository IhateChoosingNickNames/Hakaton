from django.contrib import admin
from .models import Recipe, Category, Type
# from .models import Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('category', 'type', 'title')
    search_fields = ('title', 'text',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#    list_display = ('title')
#    search_fields = ('title',)
#    empty_value_display = '-пусто-'
