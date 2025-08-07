from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Topic,Question,WrongAnswer

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('name', 'is_staff', 'is_superuser')
    ordering = ('name',)
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )

class customTopic(admin.ModelAdmin):
    list_display=('id','name')
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Topic,customTopic)
admin.site.register(Question)
admin.site.register(WrongAnswer)