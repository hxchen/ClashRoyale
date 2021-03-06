# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 15:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClashRoyale_app', '0002_contact_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('clan', models.CharField(max_length=20)),
                ('level', models.IntegerField(default=0, max_length=10)),
                ('highest_trophies', models.IntegerField(default=0, max_length=10)),
                ('last_known_trophies', models.IntegerField(default=0, max_length=10)),
                ('challenge_cards_won', models.IntegerField(default=0, max_length=10)),
                ('tourney_cards_won', models.IntegerField(default=0, max_length=10)),
                ('total_donations', models.IntegerField(default=0, max_length=10)),
                ('prev_season_rank', models.IntegerField(default=0, max_length=10)),
                ('prev_season_trophies', models.IntegerField(default=0, max_length=10)),
                ('prev_season_highest', models.IntegerField(default=0, max_length=10)),
                ('best_season_rank', models.IntegerField(default=0, max_length=10)),
                ('previous_season_rank', models.IntegerField(default=0, max_length=10)),
                ('legendary_trophies', models.IntegerField(default=0, max_length=10)),
                ('wins', models.IntegerField(default=0, max_length=10)),
                ('losses', models.IntegerField(default=0, max_length=10)),
                ('update_time', models.DateTimeField()),
            ],
        ),
    ]
