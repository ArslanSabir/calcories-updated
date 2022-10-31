from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth.views import LogoutView
from apps.users.views import RegisterationView, \
    CompleteProfile, LoginView, \
    DashboardView, \
    AddItemsView, EditProfileView, MonthlyCalories, Home, CaloriesByWeekView, Search

app_name = 'users'

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("login/", LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", RegisterationView.as_view(), name="registration"),
    path("create/profile/", CompleteProfile.as_view(), name="create_profile"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('add/items/', AddItemsView.as_view(), name="add_food"),
    path('profile/edit/', EditProfileView.as_view(), name="edit_profile"),
    path('monthly/', MonthlyCalories.as_view(), name="monthly_calories"),
    path("week/<int:year>/<int:week>/", CaloriesByWeekView.as_view(), name="week"),
    path('search/', Search.as_view(), name="search")
]
