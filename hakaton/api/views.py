from api.models import Category, Recipe, Type
from django.core.exceptions import ObjectDoesNotExist


def get_recipe(category, type=None, amount=5):
    '''Получает рецепты.'''
    
    amount = int(amount)
    try:
        category = Category.objects.get(title=category.lower())
        if type is not None:
            type = Type.objects.get(title=type.lower())
            recipes = Recipe.objects.filter(type=type, category=category)
        else:
            recipes = category.recipies.all()
    except ObjectDoesNotExist:
        return []
    return recipes[:amount]
