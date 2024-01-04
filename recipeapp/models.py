from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    cooking_steps = models.TextField(default='', blank=True)
    cooking_time = models.IntegerField()
    img = models.ImageField()
    author = models.ForeignKey(Author, on_delete=models.SET_DEFAULT, default='Author unknown')
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default='Category unknown')
    add_time = models.DateField(auto_now_add=True)
