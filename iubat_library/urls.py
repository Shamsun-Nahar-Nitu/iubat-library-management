from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from books.views import home
from users.views import (
    user_login, user_logout, dashboard,
    admin_create_user, admin_update_user, admin_delete_user,
)
from borrowing.views import (
    borrow_request, issue_book, return_book, update_stock, send_overdue_notification,
)
from users.admin import library_admin_site  # Import custom admin site

urlpatterns = [
    # Custom Admin Panel
    path('admin/', library_admin_site.urls),

    # Authentication
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # User Dashboard
    path('dashboard/', dashboard, name='dashboard'),

    # Book List & Details (home handles list, add book_detail if separate)
    path('', home, name='home'),

    # Student Borrow Request
    path('borrow/<int:book_id>/', borrow_request, name='borrow_request'),

    # Librarian Panels
    path('librarian/issue/', issue_book, name='issue_book'),
    path('librarian/return/', return_book, name='return_book'),
    path('librarian/update-stock/', update_stock, name='update_stock'),
    path('librarian/send-overdue/', send_overdue_notification, name='send_overdue_notification'),

    # Admin Tools (separate from admin panel)
    path('admin-tools/create-user/', admin_create_user, name='admin_create_user'),
    path('admin-tools/update-user/', admin_update_user, name='admin_update_user'),
    path('admin-tools/delete-user/', admin_delete_user, name='admin_delete_user'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
