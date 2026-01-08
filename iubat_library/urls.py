from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from books.views import home, add_book
from users.views import (
    user_login, user_logout, dashboard,
    admin_create_user, admin_update_user, admin_delete_user,
)
from borrowing.views import (
    borrow_request, issue_book, return_book, update_stock, send_overdue_notification, generate_report,
)
from users.admin import library_admin_site

urlpatterns = [
    path('admin/', library_admin_site.urls),

    path('', home, name='home'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),

    path('borrow/<int:book_id>/', borrow_request, name='borrow_request'),

    path('librarian/issue/', issue_book, name='issue_book'),
    path('librarian/return/', return_book, name='return_book'),
    path('librarian/update-stock/', update_stock, name='update_stock'),
    path('librarian/send-overdue/', send_overdue_notification, name='send_overdue_notification'),

    path('admin-tools/create-user/', admin_create_user, name='admin_create_user'),
    path('admin-tools/update-user/', admin_update_user, name='admin_update_user'),
    path('admin-tools/delete-user/', admin_delete_user, name='admin_delete_user'),
    path('admin-tools/add-book/', add_book, name='add_book'),

    path('librarian/generate-report/', generate_report, name='generate_report'),
]

# Serve media files in development (uploaded cover images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)