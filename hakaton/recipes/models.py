from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    '''Класс категории блюд: супы, каши, десерты, напитки и т.д.'''
    
    title = models.CharField('Название', max_length=256, unique=True)
 
    def __str__(self):
        return self.title


class Type(models.Model):
    '''Класс типы блюд: щи, овсяная каша, коктейли и т.д.'''
    
    title = models.CharField('Название', max_length=256, unique=True)
    
    def __str__(self):
        return self.title

    
class Recipe(models.Model):
    '''Класс рецепты'''

    category = models.ForeignKey(
        Category, verbose_name='Категории', on_delete=models.CASCADE, related_name='recipies'
    )
    type =  models.ForeignKey(
        Type, verbose_name='Типы', on_delete=models.CASCADE, related_name='recipies'
    )
    title = models.CharField('Название', max_length=200)
    text = models.TextField('Описание рецепта')
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)
    image = models.ImageField(
        upload_to='images/%Y/%m/%d', null=True, blank=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'category', 'type', 'title'),
                name='unique_follow'
            ),
        )
    def __str__(self):
        return self.title
