
from random import sample

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, RecipeEditForm
from .models import Author, Category

from .forms import RecipeAddForm
from .models import Recipe




# @login_required  # Декоратор, защиты доступа без логина
def index(request):
    return render(request, 'recipeapp/index.html')


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Author.objects.create(user=user)
            raw_password = form.cleaned_data.get('password1')

            # выполняем аутентификацию
            author = authenticate(username=user.username, password=raw_password)
            login(request, author)

            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'recipeapp/signup.html', {'form': form})


@login_required  # Декоратор, защиты доступа без логина
def add_recipe(request):  # функция создания рецепта
    if request.method == 'POST':
        form = RecipeAddForm(request.POST, request.FILES)
        message = 'Ошибка данных'
        if form.is_valid():
            recipe_name = form.cleaned_data['recipe_name']
            recipe_description = form.cleaned_data['recipe_description']
            recipe_cooking_steps = form.cleaned_data['recipe_cooking_steps']
            recipe_cooking_time = form.cleaned_data['recipe_cooking_time']
            if request.user.is_authenticated:
                author, created = Author.objects.get_or_create(user=request.user)
                recipe_author = author
            recipe_category = form.cleaned_data['recipe_category']
            category, created = Category.objects.get_or_create(name=recipe_category)
            recipe_image = form.cleaned_data['recipe_image']

            recipe = Recipe(name=recipe_name, description=recipe_description, cooking_steps=recipe_cooking_steps,
                            cooking_time=recipe_cooking_time, author=recipe_author, category=category,
                            img=recipe_image)
            recipe.save()
            message = 'Рецепт сохранен!'
    else:
        form = RecipeAddForm()
        message = 'Заполните форму!'
    return render(request, 'recipeapp/add_recipe.html', context={'form': form, 'message': message})


@login_required  # Декоратор, защиты доступа без логина
def edit_recipe(request, recipe_id):   # функция изменения рецепта
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author.user == request.user:
        if request.method == 'POST':
            form = RecipeEditForm(request.POST, request.FILES, instance=recipe)
            if form.is_valid():
                form.save()
                return render(request, 'recipeapp/edit_recipe.html',
                              {'form': form, 'recipe': recipe, 'message': 'Рецепт успешно изменен'})
        else:
            form = RecipeEditForm(instance=recipe)
        return render(request, 'recipeapp/edit_recipe.html',
                      {'form': form, 'recipe': recipe, 'message': 'Внесите необходимые изменения:'})


@login_required  # Декоратор, защиты доступа без логина
def delete_recipe(request, recipe_id):   # функция удаления рецепта
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if recipe.author.user == request.user:
        recipe.delete()
        messages.success(request, 'Рецепт успешно удален.')
        return redirect('/show_all_my_recipe/')
    else:
        return render(request, 'recipeapp/error_page.html',
                      {'message': 'Произошла ошибка удаления, .'})


@login_required  #
def show_all_my_recipe(request):  # функция показа рецептов текущего пользователя
    clear_recipes = Recipe.objects.filter(author_id=request.user.id)

    return render(request, 'recipeapp/show_all_my_recipe.html', {'clear_recipes': clear_recipes, 'user': request.user})


def show_five_recipe(request):  # функция показа 5 случайных рецептов
    n = None
    my_ids = Recipe.objects.values_list('id', flat=True)
    my_ids = list(my_ids)
    if len(my_ids) < 5:

        rand_ids = my_ids
        n = len(my_ids)
    else:
        rand_ids = sample(my_ids, 5)

    random_recipe = Recipe.objects.filter(id__in=rand_ids)


    return render(request, 'recipeapp/show_five_recipe.html',
                  {'random_recipe': random_recipe, 'message': f'Выведено случайных рецептов: {n}'})


# @login_required  # Декоратор, защиты доступа без логина
def show_full_recipe(request, recipe_id):  # Показать 1 полный рецепт
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    return render(request, 'recipeapp/show_full_recipe.html', {'recipe': recipe})
