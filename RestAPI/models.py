# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import reverse
from django.conf import settings

from django.db import models


class Actor(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=50)
    avatar_url = models.URLField()
    event_count = models.IntegerField(default=0)
    latest_event_timestamp = models.DateTimeField(blank=True, null=True)
    streak = models.IntegerField(default=0)
    pushed_today = models.BooleanField(default=False)

    class Meta:
        ordering = ('-event_count', '-latest_event_timestamp', 'login')

    def __str__(self):
        return self.login

    def actor_events_queryset(self):
        return self.event_set.all().order_by('-created_at', )

    def actor_events_url(self):
        return settings.BASE_URL + reverse('RestAPI:actor_events', args=[self.id])

class Repo(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __str__(self):
        return self.name

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=12)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    created_at = models.DateTimeField()

    class Meta:
        ordering = ("id", )

    def __str__(self):
        return "{}".format(self.id)
