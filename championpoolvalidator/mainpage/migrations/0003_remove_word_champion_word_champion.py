# Generated by Django 4.1.5 on 2023-01-27 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0002_word'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='champion',
        ),
        migrations.AddField(
            model_name='word',
            name='champion',
            field=models.ManyToManyField(to='mainpage.championmastery'),
        ),
    ]
