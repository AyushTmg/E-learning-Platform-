from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import User,Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id',"first_name","last_name","email",'birth_date', "is_staff", "is_active",'is_superuser',"created_at","updated_at")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("first_name","last_name","email",'birth_date')}),
        ("Permissions", {"fields": ("is_staff", "is_active",'is_superuser', "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "first_name","last_name","email",'birth_date',"password1","password2", "is_staff",
                "is_active",'is_superuser', "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=['pk','user','bio']