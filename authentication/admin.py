from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role', )
    list_display_links = ('id', 'username',)
    search_fields = ('username', )
    list_filter = ('role',)


admin.site.register(User, UserAdmin)
