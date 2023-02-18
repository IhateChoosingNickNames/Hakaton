from api.models import Category, Recipe, Type
from django.core.exceptions import ObjectDoesNotExist


def get_recipe(category, type_=None, amount=5):
    '''Получает рецепты.'''
    amount = int(amount)
    try:
        category = Category.objects.get(title=category.capitalize())
        if type is not None:
            type_ = Type.objects.get(title=type_.capitalize())
            recipes = Recipe.objects.filter(type=type_, category=category)
        else:
            recipes = category.recipies.all()
    except ObjectDoesNotExist:
        return []
    return recipes[:amount]


def add_recipe(category, type_, title, text):
    '''Добавляет рецепты.'''
    title, text = title.strip(), text.strip()
    if not title or not text:
        return 404
    try:
        category = Category.objects.get(title=category.capitalize())
        type_ = Type.objects.get(title=type_.capitalize())
        Recipe.objects.create(category=category, type=type_, title=title, text=text)
    except Exception:
        return 404
    return 200
