from django.urls import include, path
from rest_framework.routers import DefaultRouter
from olimApp.views import FileViewSet, PageViewSet, CustomUserViewSet, UserProfileView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r"pages", PageViewSet)
router.register(r"files", FileViewSet)
router.register(r"users", CustomUserViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/profile/", UserProfileView.as_view(), name="user_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
