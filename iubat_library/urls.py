from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from books.views import home
from users.views import (
    user_login, user_logout, dashboard,
    admin_create_user, admin_update_user, admin_delete_user,  # updated imports
)
from borrowing.views import borrow_request, issue_book, return_book  # Added return_book
from users.admin import library_admin_site  # Import custom site

urlpatterns = [
    # Use custom admin site
    path('admin/', library_admin_site.urls),
    # path('admin/', admin.site.urls),  # keep commented if using custom site

    # Authentication
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # User dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Borrowing & librarian actions
    path('borrow/<int:book_id>/', borrow_request, name='borrow_request'),
    path('librarian/issue/', issue_book, name='issue_book'),
    path('librarian/return/', return_book, name='return_book'),  # New return page

    # Admin tools (renamed functions)
    path('admin-tools/create-user/', admin_create_user, name='admin_create_user'),
    path('admin-tools/update-user/', admin_update_user, name='admin_update_user'),
    path('admin-tools/delete-user/', admin_delete_user, name='admin_delete_user'),

    # Home page
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
