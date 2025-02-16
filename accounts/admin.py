from django.contrib import admin
from .models import User,UserToken
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    # Define the fields to be used in the admin panel
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal Info', {'fields': ('fullName', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # Removed 'created_at' and 'updated_on' from fieldsets
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'fullName', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('phone', 'fullName', 'email', 'is_staff', 'created_at', 'updated_on')  # You can still display them in the list view
    search_fields = ('phone', 'fullName', 'email')
    ordering = ('phone',)
    readonly_fields = ('created_at', 'updated_on')  # Mark these fields as read-only

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(UserToken)