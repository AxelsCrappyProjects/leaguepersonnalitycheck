# Generated by Django 4.1.5 on 2023-01-27 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0007_remove_word_champion_word_champion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championmastery',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.DeleteModel(
            name='Word',
        ),
    ]
