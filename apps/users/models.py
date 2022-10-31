from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel

from apps.users.managers import UserManager

# Create your models here.


class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        Male = 'male', 'Male'
        Female = 'female', 'Female'
        Other = 'other', 'Other'

    class Question(models.TextChoices):
        GAIN = 'gain', 'Gain'
        LOSE = 'lose', 'Lose'

    class LifeStyle(models.TextChoices):
        Sedentary = 'sedentary', 'Sedentary'
        Lightly_Active = 'lightly_active', 'Lightly Active'
        Moderately_Active = 'moderately_active', 'Moderately Active'
        Very_Active = 'very_active', 'Very Active'
        Extra_Active = 'extra_active', 'Extra Active'

    user = models.OneToOneField(to=get_user_model(), related_name="profile", on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=Gender.choices, default='', null=True, blank=True)
    life_style = models.CharField(max_length=20, choices=LifeStyle.choices, default='', null=True, blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    dob = models.DateField(_('data of birth'), null=True)
    question = models.CharField(max_length=10, choices=Question.choices, blank=True, null=True)
    is_profile_complete = models.BooleanField(null=True, blank=True, default=False)

    def get_life_style(self):
        return self.life_style.replace("_", ' ')

    def get_age(self):
        return timezone.now().year - self.dob.year

    def get_height_in_centimeter(self):
        return self.height

    def get_bmr(self):
        multiply = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }

        bmr = (10 * self.weight) + (6.25 * self.get_height_in_centimeter()) - (5 * self.get_age()) 
        bmr = bmr + 5 if self.gender == self.Gender.Male.value else bmr - 161

        bmr *= multiply[self.life_style]

        return round(bmr)


class FoodItem(TimeStampedModel):
    class ConsumedAtChoices(models.TextChoices):
        Lunch = 'lunch', 'Lunch'
        Dinner = "dinner", 'Dinner'
        Break_Fast = 'break_fast', 'Break Fast'

    name = models.CharField(max_length=100)
    calories = models.FloatField()
    consumed_at = models.CharField(max_length=12, choices=ConsumedAtChoices.choices)

    user = models.ForeignKey(to=get_user_model(), related_name='foods', on_delete=models.CASCADE, null=True)

    def get_consumed_at(self):
        return self.consumed_at.replace('_', ' ')
