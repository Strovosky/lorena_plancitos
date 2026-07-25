from django.contrib import admin
from .models import Aventurero
from django.contrib.auth.admin import UserAdmin

class AventureroAdmin(UserAdmin):
    model = Aventurero
    list_display = ("correo", "usuario", "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("correo", "password")}),
        ("Personal info", {"fields": ("usuario", "nombre", "apellido", "telefono")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("correo", "usuario", "nombre", "apellido", "telefono", "password1", "password2", "is_staff", "is_active", "is_superuser"),
        }),
    )
    search_fields = ("correo",)
    ordering = ("correo",)

admin.site.register(Aventurero)
