from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from .models import Profile


# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'

# class CustomUserAdmin(admin.ModelAdmin):
#   inlines = (ProfileInline, )
#     # form = CustomerForm
#   fields = (
#           'username',
#           'first_name',
#           'last_name',
#           'email',
#           'is_active'
#         )
#   list_display = (
#     'username',
#     'first_name',
#     'last_name',
#     'email',
#     'is_active'
#   )

  

# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)



# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline, )
#     exclude = ('password',)

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# class CustomerForm(UserChangeForm):

#     class Meta:
#         model = User
#         fields = (
#           'username',
#           'first_name',
#           'last_name',
#           'email',
#           'is_active'
#         )


