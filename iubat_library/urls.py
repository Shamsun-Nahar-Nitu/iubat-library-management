from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from books.views import home
from users.views import user_login, user_logout, dashboard, create_user, update_user, delete_user  # Added delete_user
from borrowing.views import borrow_request, issue_book, return_book  # Added return_book
from users.admin import library_admin_site  # Import custom site

urlpatterns = [
    path('admin/', library_admin_site.urls),
   # path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('borrow/<int:book_id>/', borrow_request, name='borrow_request'),
    path('librarian/issue/', issue_book, name='issue_book'),
    path('librarian/return/', return_book, name='return_book'),  # New return page
    path('admin/create-user/', create_user, name='create_user'),  # new route
    path('admin/update-user/', update_user, name='update_user'),  # new route
    path('admin/delete-user/', delete_user, name='delete_user'),  # new route for delete user
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)