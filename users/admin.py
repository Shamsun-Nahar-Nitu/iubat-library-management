from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser
from books.models import Book, Category
from borrowing.models import Borrowing


class LibraryAdminSite(admin.AdminSite):
    site_header = 'IUBAT Library Administration'  # Top bar title
    site_title = 'IUBAT Library Administration'   # Browser tab title
    index_title = 'Library Management Panel'      # Main dashboard title
    site_url = '/'                                # Changes the "View site" link to go to home page

    def get_app_list(self, request, app_label=None):
        """
        Override to ensure site_url is set correctly.
        """
        app_list = super().get_app_list(request, app_label)
        # Ensure the "View site" button points to the main site
        self.site_url = '/'
        return app_list

    def index(self, request, extra_context=None):
        """
        Override the index view to pass site_url to the template
        so the "View site" button uses the correct URL and text.
        """
        extra_context = extra_context or {}
        extra_context['site_url'] = self.site_url
        return super().index(request, extra_context=extra_context)


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