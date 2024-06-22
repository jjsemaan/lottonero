from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('predictions/', include('predictions.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('orders/', include('orders.urls')),
    path('lottery_stats/', include('lottery_stats.urls')),
    path('scraping/', include(('scraping.urls', 'scraping'), namespace='scraping')),
    path('', include('home.urls')),
    path('user/', include(('user_profile.urls', 'user_profile'), namespace='user_profile')),
    path('contact/', include('contact.urls')),
    path('stripe/', include('djstripe.urls', namespace='djstripe')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)