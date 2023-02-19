from django.db import models


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

    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)
    # image = models.ImageField(
    #     upload_to='hakaton/', null=True, blank=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
