# Generated by Django 4.1.5 on 2023-01-21 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_remove_champion_words_word_champion'),
    ]

    operations = [
        migrations.AddField(
            model_name='champion',
            name='reason',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='champion',
            name='valid',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Word',
        ),
    ]
