from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Optional: customize how your user appears in admin,
    # for example adding fields like date_of_birth and profile_photo
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)




# from django.contrib import admin
# from .models import Book

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     # Fields to display in the admin list view
#     list_display = ('title', 'author', 'published_year')

#     # Enable filtering by publication_year
#     list_filter = ('published_year',)

#     # Enable search functionality for title and author fields
#     search_fields = ('title', 'author')