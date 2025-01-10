from django.db import models

class Game(models.Model):
    steam_appid = models.CharField(verbose_name="APPID", max_length=255)
    name = models.CharField(verbose_name="Название", max_length=255)
    short_description = models.CharField(verbose_name="Резюме", max_length=255)
    metacritic = models.CharField(verbose_name="Оценка", max_length=255)
    metacritic_link = models.CharField(verbose_name="Metacritic ссылка", max_length=255)
    release_date = models.CharField(verbose_name="Дата выхода", max_length=255)
    developers = models.CharField(verbose_name="Разработчики", max_length=255)
    publishers = models.CharField(verbose_name="Издатели", max_length=255)
    genres = models.CharField(verbose_name="Жанры", max_length=255)
    categories = models.CharField(verbose_name="Категории", max_length=255)
    header_image = models.CharField(verbose_name="Изображение", max_length=255)
    background = models.CharField(verbose_name="Фон", max_length=255)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ("name",)

    def __str__(self):
        return self.name
