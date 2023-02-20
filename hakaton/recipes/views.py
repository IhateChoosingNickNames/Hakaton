from .exceptions import WrongInputError
from .models import Category, Recipe, Type, User
from django.core.exceptions import ObjectDoesNotExist


def get_my_recipes(author):
    return Recipe.objects.filter(author__username=author)


def get_categories():
    return Category.objects.all()


def get_types():
    return Type.objects.all()


def get_random_recipe():
    return Recipe.objects.order_by("?")[0]


def get_recipe(data):
    '''Получает рецепты.'''

    category, type_, amount = data["category"].strip(), data["type_"], data["amount"]

    if amount is None:
        amount = 5

    try:
        category = Category.objects.get(title=category.capitalize())
        if type_ is not None:
            type_ = Type.objects.get(title=type_.capitalize().strip())
            recipes = Recipe.objects.filter(type=type_, category=category)

        else:
            recipes = category.recipies.all()
    except ObjectDoesNotExist:
        return []
    return recipes[:amount]


def add_recipe(data):
    '''Добавляет рецепты.'''

    category, type_, title, text, author = data["category"].strip(), data["type_"].strip(), data["title"].strip(), data["text"].strip(), data["author"]

    try:
        category = Category.objects.get(title=category.capitalize())
        type_ = Type.objects.get(title=type_.capitalize())
        author, _ = User.objects.get_or_create(**author)
        recipe, _ = Recipe.objects.get_or_create(category=category, type=type_, title=title, text=text, author=author)
    except Exception:
        raise WrongInputError
