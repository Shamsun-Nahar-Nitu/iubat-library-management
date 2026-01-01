from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from books.views import home
from users.views import user_login, user_logout, dashboard
from borrowing.views import borrow_request  # <-- Must be here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('borrow/<int:book_id>/', borrow_request, name='borrow_request'),  # <-- Must be here
    path('', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)