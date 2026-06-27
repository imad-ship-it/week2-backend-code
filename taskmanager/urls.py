from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import MeView, RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tasks.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/me/", MeView.as_view(), name="me"),
]
