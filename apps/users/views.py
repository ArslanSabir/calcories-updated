import calendar
from collections import Counter
from django.db.models import Sum
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import get_user_model

from apps.users.models import Profile, FoodItem

User = get_user_model()

class Home(View):
    def get(self, request):
        return redirect("users:dashboard")

class RegisterationView(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        data = request.POST
        if data.get("password") == data.get("confirm_password"):
            user = User.objects.create(
                email=data.get("email"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name")
            )
            user.set_password(data.get("password"))
            user.save()
            Profile.objects.create(user=user)
            user = authenticate(email=data.get("email"), password=data.get("password"))
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 message="Account Created Successfully! Please complete your profile")

            return redirect("users:create_profile")

        messages.add_message(request, messages.ERROR, message="Check your email and password")
        return render(request, "register.html")


class CompleteProfile(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.profile.is_profile_complete:
            return redirect("users:dashboard")
        return render(request, 'create_profile.html')


    def post(self, request):
        data = request.POST
        profile = request.user.profile
        profile.gender = data.get("gender")
        profile.life_style = data.get("life_style")
        profile.height = data.get("height")
        profile.weight = data.get("weight")
        profile.dob = data.get("dob")
        profile.question = data.get("question")
        profile.is_profile_complete = True
        profile.save()
        return redirect("users:dashboard")


class LoginView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('users:dashboard')
        return render(request, 'login.html')

    def post(self, request):
        data = request.POST
        user = User.objects.get(email=data.get("email"))
        if user.check_password(data.get("password")):
            user = authenticate(email=data.get("email"), password=data.get("password"))
            login(request, user)
            return redirect("users:dashboard")
        return redirect("users:login")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_superuser:
            return redirect(to='/admin')
        if user.profile.is_profile_complete:
            today_calories = user.foods.filter(created__date=timezone.now().date()).aggregate(calories=Sum('calories'))['calories']
            if today_calories:
                if today_calories > user.profile.get_bmr():
                    messages.add_message(request, messages.WARNING, "You have to take less calories to reduce your weight")
            else:
                messages.add_message(request, messages.WARNING, "You have to take more calories to increase your weight")

            context = {
                'today_calories': today_calories if today_calories else 0,

            }
            return render(request, 'dashboard.html', context)
        return redirect("users:create_profile")


class AddItemsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'add_items.html')

    def post(self, request):
        user = request.user
        data = request.POST

        food_name = data.getlist('food')
        calories = data.getlist('calories')
        time = data.getlist('time')
        food_items = []
        for item_index in range(0, len(food_name)):
            food_item = FoodItem(user=user, name=food_name[item_index], calories=calories[item_index],
                                 consumed_at=time[item_index])
            food_items.append(food_item)
        FoodItem.objects.bulk_create(food_items)

        return render(request, 'add_items.html')


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "edit_profile.html")

    def post(self, request):
        user = request.user
        data = request.POST

        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.save()

        user.profile.height = data.get("height")
        user.profile.weight = data.get("weight")
        user.profile.gender = data.get("gender")
        user.profile.life_style = data.get("life_style")
        user.profile.dob = data.get("dob")
        user.profile.question = data.get("question")
        user.profile.save()
        return redirect('users:dashboard')


class MonthlyCalories(View):
    def post(self, request):
        fooditem_days = {}

        user = request.user
        month = int(request.POST["month"]) + 1
        year = int(request.POST["year"])
        month_name = calendar.month_name[month]
        _, month_len = calendar.monthrange(year=year, month=month)

        days = [day for day in range(1, month_len + 1)]
        food_items = FoodItem.objects.filter(user=user, created__month=month, created__year=year)
        for food_item in food_items:
            if fooditem_days.get(food_item.created.day):
                fooditem_days[food_item.created.day] += food_item.calories
            else:
                fooditem_days[food_item.created.day] = food_item.calories

        monthly_calories = {}
        for day in days:
            if fooditem_days.get(day):
                monthly_calories[day] = fooditem_days[day]
            else:
                monthly_calories[day] = 0

        data = {
            "days": list(monthly_calories.keys()),
            "calories": list(monthly_calories.values())
        }

        return JsonResponse(data)


class CaloriesByWeekView(View):
    def get(self, request, year, week):
        user = request.user
        calories = 0
        for food in user.foods.filter(created__week=week, created__year=year):
            calories += food.calories
        context = {
            'calories': calories
        }
        return JsonResponse(context)


class Search(LoginRequiredMixin, View):
    template = "search.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {}
        data = request.GET
        date = data.get('date')
        week = data.get('week')
        day = data.get('day')
        item_key = 'items'
        if data:
            context[item_key] = user.foods.filter(created__date=date)
        if week:
            year, week = week.split('-W')
            context[item_key] = user.foods.filter(created__week=week, created__year=year)
        if day and int(day) in list(range(1, 32)):
            context[item_key] = user.foods.filter(created__date__day=day)

        return render(request, self.template, context=context)

