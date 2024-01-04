from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Recipe


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль:', strip=False,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
                                help_text='Не менее 12 знаков, включая строчные, заглавные буквы, спецсимволы и цифры')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class RecipeAddForm(forms.Form):
    recipe_name = forms.CharField(label='Название рецепта:', max_length=100, required=True, widget=forms.TextInput(
        attrs={'class': 'recipe_name', 'placeholder': 'Введите название рецепта'}))
    recipe_description = forms.CharField(label='Описание рецепта:', widget=forms.Textarea(
        attrs={'class': 'recipe_description', 'placeholder': 'Введите описание рецепта'}))
    recipe_cooking_steps = forms.CharField(label='Шаги приготовления:', required=True, widget=forms.Textarea(
        attrs={'class': 'cooking_steps', 'placeholder': 'Введите шаги приготовления.'}))
    recipe_cooking_time = forms.IntegerField(label='Время приготовления (мин):', min_value=1, required=True,
                                             widget=forms.NumberInput(attrs={
                                                 'class': 'cooking_time',
                                                 'placeholder': 'Введите время приготовления в минутах'}))
    recipe_category = forms.CharField(label='Категория рецепта:', widget=forms.TextInput(
        attrs={'class': 'recipe_category', 'placeholder': 'Укажите категорию рецепта:'}))
    recipe_image = forms.ImageField(label='Изображение рецепта:',
                                    widget=forms.ClearableFileInput(attrs={'class': 'recipe_image'}),)


class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cooking_steps', 'cooking_time', 'img', 'category']
        labels = {
            'name': 'Название рецепта:',
            'description': 'Описание рецепта:',
            'cooking_steps': 'Шаги приготовления',
            'cooking_time': 'Время приготовления',
            'img': 'Изображение рецепта',
            'category': 'Категория рецепта',
        }
