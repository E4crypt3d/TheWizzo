from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from .forms import CustomUserCreationForm
# Register your models here.


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    # readonly_fields = ('followers',)


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            # group heading of your choice; set to None for a blank space instead of a header
            'User Profile',
            {
                'fields': (
                    'date_of_birth', 'gender'
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ['id', 'user',
                    'updated', 'created', 'profile_pic']
    list_display_links = ['id', 'user',
                          'updated', 'created', 'profile_pic']
    list_select_related = ['user']
