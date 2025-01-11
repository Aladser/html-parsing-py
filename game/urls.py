from django.urls import path

from game.apps import GameConfig
from game.views import GameListView, GameDetailView

app_name = GameConfig.name

urlpatterns = [
    path('', GameListView.as_view()),
    path('detail/<int:pk>', GameDetailView.as_view()),
]
