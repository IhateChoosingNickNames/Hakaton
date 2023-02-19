from .exceptions import WrongInputError
from .models import Category, Recipe, Type
from django.core.exceptions import ObjectDoesNotExist


def get_categories():
    return Category.objects.all()


def get_types():
    return Type.objects.all()


def get_random_recipe():
    return Recipe.objects.order_by("?")[0]


def get_recipe(data):
    '''Получает рецепты.'''

    category, type_, amount = data["category"], data["type_"], data["amount"]

    if amount is None:
        amount = 5

    try:
        category = Category.objects.get(title=category.capitalize())
        if type_ is not None:
            type_ = Type.objects.get(title=type_.capitalize())
            recipes = Recipe.objects.filter(type=type_, category=category)
        else:
            recipes = category.recipies.all()
    except ObjectDoesNotExist:
        return []
    return recipes[:amount]


def add_recipe(data):
    '''Добавляет рецепты.'''

    category, type_, title, text = data["category"], data["type_"], data["title"], data["text"]

    try:
        category = Category.objects.get(title=category.capitalize())
        type_ = Type.objects.get(title=type_.capitalize())
        obj, created = Recipe.objects.get_or_create(category=category, type=type_, title=title.strip(), text=text.strip())
    except Exception:
        raise WrongInputError
