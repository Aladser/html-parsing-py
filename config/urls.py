from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', include('game.urls', namespace='game'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
