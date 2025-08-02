# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User
# from .models import UserProfile


# class UserProfileInline(admin.StackedInline):
#     """
#     Inline admin descriptor for UserProfile model
#     which acts a bit like a singleton
#     """
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'User Profiles'
#     fk_name = 'user'


# class UserAdmin(BaseUserAdmin):
#     """
#     Extended UserAdmin to include UserProfile inline
#     """
#     inlines = (UserProfileInline,)

#     def get_inline_instances(self, request, obj=None):
#         if not obj:
#             return list()
#         return super().get_inline_instances(request, obj)


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     """
#     Admin configuration for UserProfile model
#     """
#     list_display = ('user', 'role', 'get_email', 'get_date_joined')
#     list_filter = ('role', 'user__date_joined')
#     search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
#     ordering = ('user__username',)
    
#     def get_email(self, obj):
#         return obj.user.email
#     get_email.short_description = 'Email'
#     get_email.admin_order_field = 'user__email'
    
#     def get_date_joined(self, obj):
#         return obj.user.date_joined
#     get_date_joined.short_description = 'Date Joined'
#     get_date_joined.admin_order_field = 'user__date_joined'


# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)



from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'isbn']
    list_filter = ['publication_year', 'author']
    search_fields = ['title', 'author', 'isbn']
    ordering = ['title']