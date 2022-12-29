from django.shortcuts import render, get_object_or_404
from .models import Meal, MealClick
from django.db.models import Count
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
    MealClick.objects.create(meal=meal)
    meal_score = MealClick.objects.values('meal_id').annotate(score=Count('meal_id')).filter(meal_id=meal_id)[:1]
    return render(request, 'cafe_core_app/meal.html', {'meal': meal, 'meal_score': list(meal_score)[0]["score"]})


def meal_top(request):
    #meal_scores = MealClick.objects.values('meal_id').annotate(score=Count('meal_id')).order_by('-score')[:3]
    meals_scores = Meal.objects.raw("""
            SELECT meal.id, meal.name, count(mc.id) as click_count
            FROM cafe_core_app_mealclick mc
            JOIN cafe_core_app_meal meal on meal_id=meal.id
            GROUP BY meal.id
            ORDER BY click_count DESC
        """)[:3]
    meals = list(meals_scores)
    return render(request, 'cafe_core_app/meal_top3.html', {'meal_scores': meals})




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