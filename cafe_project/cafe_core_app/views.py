from django.shortcuts import render, get_object_or_404
from .models import Meal, MealClick
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.db.models.functions import Trunc
from users.models import User


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
    list_of_dicts = list(get_meal_clicks_by_hour(meal_id))
    timelist_for_chart = [dict['hour'].strftime('%Y-%m-%d %H:%M') for dict in list_of_dicts]
    clicklist_for_chart = [dict['clicks'] for dict in list_of_dicts]
    return render(request, 'cafe_core_app/meal.html', {'meal': meal, 'meal_score': list(meal_score)[0]["score"], 'timelist_for_chart': timelist_for_chart, 'clicklist_for_chart': clicklist_for_chart})


def meal_top(request):
    meals_scores = Meal.objects.raw("""
            SELECT meal.id, meal.name, count(mc.id) as click_count
            FROM cafe_core_app_mealclick mc
            JOIN cafe_core_app_meal meal on meal_id=meal.id
            GROUP BY meal.id
            ORDER BY click_count DESC
        """)[:3]
    meals = list(meals_scores)
    return render(request, 'cafe_core_app/meal_top3.html', {'meal_scores': meals})


def users_top(request):
    users_scores = User.objects.raw("""
            SELECT u.id, u.username, count(*) as click_count
            FROM cafe_core_app_mealclick mc
            JOIN users_user u on mc.user_id=u.id
            GROUP BY u.id
            ORDER BY click_count DESC
        """)[:10]
    users = list(users_scores)
    return render(request, 'cafe_core_app/users_top10.html', {'users_scores': users})


def users_categories_top(request):
    users_scores = User.objects.raw("""
            SELECT u.id, u.username, count(*) as click_count
            FROM cafe_core_app_mealclick mc
            JOIN users_user u on mc.user_id=u.id
            GROUP BY u.id
            ORDER BY click_count DESC
        """)[:10]
    users = list(users_scores)
    return render(request, 'cafe_core_app/users_top_by_categories.html', {'users_scores': users})


def get_meal_clicks_by_hour(meal_id):
    return (MealClick.objects.filter(meal_id=meal_id)
            .annotate(hour=Trunc('click_date', 'hour'))
            .values('hour')
            .annotate(clicks=Count('click_date'))
            .order_by('hour'))
