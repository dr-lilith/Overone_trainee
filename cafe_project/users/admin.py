from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'description', 'avatar')
    list_display_links = ('email', 'username')
    search_fields = ('email', 'username')
    list_editable = ('first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'description', 'avatar')


admin.site.register(User, UserAdmin)
