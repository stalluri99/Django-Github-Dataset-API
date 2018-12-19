# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from .models import Actor, Repo, Event

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'login', 'avatar_url')

class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'name', 'url')

class EventSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    repo = RepoSerializer()

    class Meta:
        model = Event
        fields = ('id', 'type', 'actor', 'repo', 'created_at')
