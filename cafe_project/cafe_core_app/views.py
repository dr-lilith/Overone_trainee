from django.shortcuts import render, get_object_or_404
from .models import Meal, MealClick
from django.utils import timezone
from django.http import HttpResponseRedirect


def menu(request):
    meal_categories = list(filter(lambda el: 'NO_TYPE' not in el[0], Meal.MealType.choices))
    return render(request, 'cafe_core_app/menu.html', {'meal_categories': meal_categories})


def meal_category(request, meal_category):
    meals_by_category = Meal.objects.filter(meal_type=meal_category)
    return render(request, 'cafe_core_app/meals.html', {'meals': meals_by_category, 'meal_category': meal_category})


def meal(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    meal.mealclick_set.create(click_date=timezone.now())
    MealClick.objects.create(meal=meal)
    return render(request, 'cafe_core_app/meal.html', {'meal': meal})


def meal_statistics(request):
    pass


# def menu_list(request, cafe_pk):
#     cafe = Cafe.objects.get(pk=cafe_pk)
#     menu_items = MenuItem.objects.filter(cafe=cafe)
#     return render(request, 'menu/menu_list.html', {'cafe': cafe, 'menu_items': menu_items})
#
# def menu_detail(request, cafe_pk, pk):
#     menu_item = MenuItem.objects.get(pk=pk)
#     return render(request, 'menu/menu_detail.html', {'menu_item': menu_item})
#
# def cafe_list(request):
#     cafes = Cafe.objects.all()
#     return render(request, 'cafes/cafe_list.html', {'cafes': cafes})
#
# def cafe_detail(request, pk):
#     cafe = Cafe.objects.get(pk=pk)
#     return render(request, 'cafes/cafe_detail.html', {'cafe': cafe})