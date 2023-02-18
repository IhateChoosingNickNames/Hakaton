from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Сuisine(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.title
    
class Type(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.title
    
class Recipe(models.Model):
    cuisine = models.ForeignKey(
        Сuisine, on_delete=models.SET_NULL, related_name='recipies'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='recipies'
    )
    type =  models.ForeignKey(
        Type, on_delete=models.SET_NULL, related_name='recipies'
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipies'
    )
    # score = models.IntegerField(
    #     validators=[MinValueValidator(1), MaxValueValidator(10)]
    # )
    pub_date = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(
    #     upload_to='hakaton/', null=True, blank=True)

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