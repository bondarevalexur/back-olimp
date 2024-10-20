from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from olimApp.views import FileViewSet, ApplicationView, PageViewSet, CustomUserViewSet, UserProfileView, \
    ActivateUserProfileView

router = DefaultRouter()
router.register(r"pages", PageViewSet)
router.register(r"files", FileViewSet)

urlpatterns = [
    path("api/", include(router.urls)),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('api/users/', CustomUserViewSet.as_view(), name='users'),
    path('api/users/activate/', ActivateUserProfileView.as_view(), name='activate_profile'),
    path("api/users/show/", UserProfileView.as_view(), name="user_profile"),

    path("api/applications/", ApplicationView.as_view(), name="application"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
