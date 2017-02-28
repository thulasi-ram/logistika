from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.urlresolvers import reverse
from django.template import loader

from users.models import User, Profile, Roles


admin.site.register(Roles)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
    'id', 'first_name', 'last_name', 'email', 'phone_number', 'is_superuser', 'is_staff', 'is_active', 'organization',
    'role')
    search_fields = ('email',)
    ordering = ('email',)
    list_filter = ('is_superuser', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions and Groups', {'fields': ('is_staff', 'is_active', 'is_superuser',
                                               'groups')}),
        ('Organization', {'fields': ('organization', 'role')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions and Groups', {'fields': ('is_staff', 'is_active', 'is_superuser',
                                               'groups')})
    )

    def save_model(self, request, obj, form, change):
        if not change:
            context = {
                'user': obj,
                'password': form.cleaned_data['password1'],
                'admin_url': request.build_absolute_uri(reverse('admin:index')),
                'home_url': request.build_absolute_uri(reverse('admin:index')).rstrip('admin/')
            }
            message = loader.render_to_string("admin/registration/welcome_email.html", context)
            subject = loader.render_to_string("admin/registration/welcome_email_subject.html", context).strip()
            obj.email_user(subject, message)
            obj.is_staff = True
        super(UserAdmin, self).save_model(request, obj, form, change)


admin.site.register(Profile)
