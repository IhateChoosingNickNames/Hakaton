from django.shortcuts import render
from api.models import Recipe

def get_recipe(cat, couisin=None, amount=5):
    return Recipe.objects.all()