from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user_profile.views import (
    SignUpView,
    ProfileUpdateView,
    ProfileView,
    CustomLoginView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("register/", SignUpView.as_view(), name="register"),
    path('predictions/', include('predictions.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('orders/', include('orders.urls')),
    path('lottery_stats/', include('lottery_stats.urls')),
    path('scraping/', include(('scraping.urls', 'scraping'), namespace='scraping')),
    path('', include('home.urls')),
] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)