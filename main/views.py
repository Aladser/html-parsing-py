from django.views.generic import TemplateView
from config.settings import MEDIA_ROOT
from main.services import get_games_info

page = '/site/index.html'

class MainView(TemplateView):
    """Представление главной страницы"""

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = get_games_info(str(MEDIA_ROOT) + page)
        return context
