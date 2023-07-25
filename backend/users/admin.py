from django.contrib import admin

from .models import MyUser, Follow


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('name',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'following',
        'user',
    )
    search_fields = ('user',)
