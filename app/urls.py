from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "ok",
        "service": "chat backend"
    })


urlpatterns = [
    path("health/", health, name="health"),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
