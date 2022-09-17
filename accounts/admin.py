from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "username",
        "email",
        "first_name",

    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("address", "phone")}),)
    fieldsets_add = UserAdmin.add_fieldsets + ((None, {"fields": ("address", "phone")}),)


admin.site.register(CustomUser, CustomUserAdmin)
