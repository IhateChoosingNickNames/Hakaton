from django.shortcuts import render
from api.models import Recipe

def get_reciper(cat, couisin=None, amount=5):
    return Recipe.objects.all()[:amount]