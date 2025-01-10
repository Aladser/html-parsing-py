from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from main.views import MainView, GameView

urlpatterns = [
    path('', MainView.as_view(), name="index"),
    path('game_test/<int:id>', GameView.as_view()),
    path('game/', include('game.urls', namespace='game'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
