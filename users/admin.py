from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser
from books.models import Book, Category
from borrowing.models import Borrowing

class LibraryAdminSite(admin.AdminSite):
    site_header = 'IUBAT Library Administration'
    site_title = 'IUBAT Library Admin'
    index_title = 'Library Management Panel'

library_admin_site = LibraryAdminSite(name='library_admin')

# Register CustomUser
@admin.register(CustomUser, site=library_admin_site)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'student_id', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'student_id')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role', 'student_id', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'student_id', 'phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.groups.clear()
        obj.user_permissions.clear()
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        pass

    inlines = []

    ordering = ('username',)

# Register other models
@admin.register(Group, site=library_admin_site)
class GroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Book, site=library_admin_site)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'available', 'price')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('category',)

@admin.register(Category, site=library_admin_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Borrowing, site=library_admin_site)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'status', 'borrow_date', 'due_date', 'return_date', 'fine')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')