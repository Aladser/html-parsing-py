from django.urls import path

from game.apps import GameConfig
from game.views import GameListView, GameView

app_name = GameConfig.name

urlpatterns = [
    path('', GameListView.as_view()),
    path('detail/<str:id>', GameView.as_view())
]
