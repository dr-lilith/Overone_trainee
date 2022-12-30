from django.urls import path
from . import views

app_name = 'cafe_core_app'
urlpatterns = [
    path('meal_top', views.meal_top, name='top'),
    path('users_top', views.users_top, name='top_users'),
    path('users_categories_top', views.users_categories_top, name='top_users_categories'),
    path('menu', views.menu, name='menu'),
    path('<meal_category>', views.meal_category, name='meal_category'),
    path('<int:meal_id>/meal', views.meal, name='meal'),


]
