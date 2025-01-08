from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.views import MainView, GameView

urlpatterns = [
    path('', MainView.as_view(), name="index"),
    path('game/<int:id>', GameView.as_view(), name="game"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
