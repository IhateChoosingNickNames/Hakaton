from api.models import Author, Category, Recipe, Type
from django.core.exceptions import ObjectDoesNotExist


def get_recipe(category, type=None, amount=5):
    '''Получает рецепты.'''
    amount = int(amount)
    try:
        category = Category.objects.get(title=category.capitalize())
        if type is not None:
            type = Type.objects.get(title=type.capitalize())
            recipes = Recipe.objects.filter(type=type, category=category)
        else:
            recipes = category.recipies.all()
    except ObjectDoesNotExist:
        return []
    return recipes[:amount]


def add_recipe(category, type, title, text, author_id):
    '''Добавляет рецепты.'''
    title, text = title.strip(), text.strip()
    if not title or not text:
        return 404
    author, created = Author.objects.get_or_create(author_id = author_id)
    try:
        category = Category.objects.get(title=category.capitalize())
        type = Type.objects.get(title=type.capitalize())
        Recipe.objects.create(category=category, type=type, title=title, text=text, author=author)
    except Exception:
        return 404
    return 200
    

def get_my_recipes(author_id):
    '''Ищет свои рецепты.'''
    try:
        author = Author.objects.get(author_id = author_id)
        recipes = author.recipies.all()
    except ObjectDoesNotExist:
        return []
    return recipes
