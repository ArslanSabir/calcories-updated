from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
# from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User, Profile, FoodItem
from django.utils.translation import gettext_lazy as _


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    # form = UserChangeForm
    # add_form = UserCreationForm

    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'last_login',
        'is_superuser',
        'created',
        'modified',
        'is_active',
        'is_staff',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'created',
        'modified',
        'is_active',
        'is_staff',
    )
    ordering = ('email',)
    raw_id_fields = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ("email", "password", "first_name", "last_name")}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'user',
        'gender',
        'life_style',
        'height',
        'weight',
        'dob',
    )
    list_filter = ('created', 'modified', 'user', 'dob')


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'name',
        'calories',
        'consumed_at',
        'created',
        'modified',
    )
    list_filter = ('created', 'modified', 'user')
    search_fields = ('name',)
