from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse({"status": "ok", "service": "chat backend"})


urlpatterns = [
    path("health/", health_check, name="health"),
    path("api/", include("api.urls")),
    path("users/", include("users.urls")),
]
