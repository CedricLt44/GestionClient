from django.contrib import admin
# Register your models here.
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_active')  # Champs affichés dans la liste admin
    search_fields = ('name', 'email')  # Champs de recherche
    list_filter = ('is_staff', 'is_active')