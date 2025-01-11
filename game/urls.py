from django.urls import path

from game.apps import GameConfig
from game.views import GameListView, GameView, GameDetailView

app_name = GameConfig.name

urlpatterns = [
    path('', GameListView.as_view()),
    path('detail/<str:id>', GameView.as_view()),
    path('game/detail/<int:pk>', GameDetailView.as_view())
]
