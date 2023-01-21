from django.db import models

class Region(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)


class SummonerName(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=30)


class Champion(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    valid = models.BooleanField()
    reason = models.CharField(max_length=30)


class ChampionMastery(models.Model):
    name = models.CharField(max_length=30)
    valid = models.BooleanField()
    reason = models.CharField(max_length=30)
    points = models.IntegerField()
    percentage = models.IntegerField()