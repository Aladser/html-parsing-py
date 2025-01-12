from django.db import models

from config.settings import NULLABLE
from libs.truncate_table_mixin import TruncateTableMixin

class Genre(TruncateTableMixin, models.Model):
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ("name",)

    def __str__(self):
        return self.name

class Category(TruncateTableMixin, models.Model):
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name

class Developer(TruncateTableMixin, models.Model):
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    class Meta:
        verbose_name = "Разработчик"
        verbose_name_plural = "Разработчики"
        ordering = ("name",)

    def __str__(self):
        return self.name

class Publisher(TruncateTableMixin, models.Model):
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    class Meta:
        verbose_name = "Издатель"
        verbose_name_plural = "Издатели"
        ordering = ("name",)

    def __str__(self):
        return self.name

class Game(TruncateTableMixin, models.Model):
    id = models.IntegerField(verbose_name="APPID", primary_key=True, unique=True)
    name = models.CharField(verbose_name="Название", max_length=255, unique=True)
    short_description = models.CharField(verbose_name="Резюме", max_length=255, **NULLABLE)
    metacritic = models.IntegerField(verbose_name="Оценка", **NULLABLE)
    metacritic_link = models.CharField(verbose_name="Metacritic ссылка", max_length=255, **NULLABLE)
    release_date = models.CharField(verbose_name="Дата выхода", max_length=255, **NULLABLE)
    header_image = models.CharField(verbose_name="Изображение", max_length=255, **NULLABLE)
    background = models.CharField(verbose_name="Фон", max_length=255, **NULLABLE)
    last_updated_at = models.DateTimeField(verbose_name="Последнее обновление", auto_now=True)

    developers = models.ManyToManyField(Developer, verbose_name="Разработчики", **NULLABLE)
    publishers = models.ManyToManyField(Publisher, verbose_name="Издатели", **NULLABLE)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", **NULLABLE)
    categories = models.ManyToManyField(Category, verbose_name="Категории", **NULLABLE)

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ("name",)

    def __str__(self):
        return f"{self.id}: {self.name}"

