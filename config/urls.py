from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from game.views import GameListView, GameView

urlpatterns = [
    path('', GameListView.as_view(), name="index"),
    path('detail/<int:id>', GameView.as_view()),
    path('game/', include('game.urls', namespace='game'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
