# Generated by Django 5.1.4 on 2025-01-26 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_game_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='price',
            field=models.CharField(blank=True, null=True, verbose_name='Цена'),
        ),
    ]
