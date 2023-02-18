# from django.contrib.auth import get_user_model
from django.db import models

# User = get_user_model()


# class Сuisine(models.Model):
#    '''Класс кухня: европейская, русская, азиатская и т.д.'''
#     title = models.CharField(max_length=256)
#     slug = models.SlugField(max_length=50, unique=True)
    
#     def __str__(self):
#         return self.title


class Category(models.Model):
    '''Класс категории блюд: супы, каши, десерты, напитки и т.д.'''
    
    title = models.CharField(max_length=256, unique=True, verbose_name='Название')
 
    def __str__(self):
        return self.title
 
   
class Type(models.Model):
    '''Класс типы блюд: щи, овсяная каша, коктейли и т.д.'''
    
    title = models.CharField(max_length=256, unique=True, verbose_name='Название')
    
    def __str__(self):
        return self.title


class Author(models.Model):
    '''Класс типы блюд: щи, овсяная каша, коктейли и т.д.'''
    
    id_telegram = models.CharField(max_length=256, unique=True, verbose_name='ID пользователя в телеграм')
    
    def __str__(self):
        return self.id_telegram
    
    
class Recipe(models.Model):
    '''Класс рецепты'''
    
    # cuisine = models.ForeignKey(
    #     Сuisine, on_delete=models.SET_NULL, related_name='recipies'
    # )
    category = models.ForeignKey(
        Category, verbose_name='Категории', on_delete=models.CASCADE, related_name='recipies'
    )
    type =  models.ForeignKey(
        Type, verbose_name='Типы', on_delete=models.CASCADE, related_name='recipies'
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    text = models.TextField(verbose_name='Описание рецепта')
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='recipies'
    )
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    # image = models.ImageField(
    #     upload_to='hakaton/', null=True, blank=True)

    class Meta:
            ordering = ('-pub_date',)

    def __str__(self):
        return self.title


# class Ingredient(models.Model):
#     title = models.CharField(max_length=256)
#     slug = models.SlugField(max_length=50, unique=True)
    
#     def __str__(self):
#         return self.title


# class RecipeIngredient(models.Model):
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE,
#         related_name='recipe'
#     )
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE,
#         related_name='ingredient'
#     )
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['recipe', 'ingredient'],
#                                     name='unique ingredient')
#         ]