from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("name", "email", "is_staff", "is_active", "date_joined")
    list_display_links = ("email",)
    search_fields = ("name", "bio", "email")
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "password")}),
        ("Personal info", {"fields": ("email", "bio", "image", "following")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("name", "password1", "password2"),
            },
        ),
    )
