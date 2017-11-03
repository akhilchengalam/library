from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from library import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.books.urls')),
    url(r'^user/', include('apps.user.urls')),
    url(r'^books/', include('apps.books.urls')),
    url(r'^accounts/', include('allauth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                        document_root=settings.STATIC_ROOT)