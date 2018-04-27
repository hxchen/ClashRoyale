from django.db import models

# Create your models here.
from django.db import models


class Test(models.Model):
    name = models.CharField(max_length=20)


class Contact(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    email = models.EmailField()


class Tag(models.Model):
    contact = models.ForeignKey(Contact)
    name = models.CharField(max_length=50)


class Profile(models.Model):
    uid = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    level = models.IntegerField(default=0)
    clan = models.CharField(max_length=20)
    level = models.IntegerField(default=0)
    highest_trophies = models.IntegerField(default=0)
    last_known_trophies = models.IntegerField(default=0)
    challenge_cards_won = models.IntegerField(default=0)
    tourney_cards_won = models.IntegerField(default=0)
    total_donations = models.IntegerField(default=0)
    prev_season_rank = models.IntegerField(default=0)
    prev_season_trophies = models.IntegerField(default=0)
    prev_season_highest = models.IntegerField(default=0)
    best_season_rank = models.IntegerField(default=0)
    previous_season_rank = models.IntegerField(default=0)
    legendary_trophies = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    update_time = models.DateTimeField()


class Clan(models.Model):
    pid = models.CharField(max_length=20)
    rank = models.CharField(max_length=20)
    uid = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    league = models.CharField(max_length=264)
    score = models.IntegerField(default=0)
    donations = models.IntegerField(default=0)
    role = models.CharField(max_length=20)
    update_time = models.DateTimeField()


















