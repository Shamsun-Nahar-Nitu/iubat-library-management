from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from books.views import home  # We will create this view next

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Home page with book list/search
    # We will add more URLs later (login, dashboard, etc.)
]

# Serve media files (book covers) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)