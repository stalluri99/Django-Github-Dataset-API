# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Actor, Repo, Event

class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "login", "avatar_url", "actor_events_url", "latest_event_timestamp", "streak", "event_count", "actor_events_queryset")

class RepoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")

class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "actor", "repo", "created_at")
    search_fields = ("id", "actor",)
    
admin.site.register(Actor, ActorAdmin)
admin.site.register(Repo, RepoAdmin)
admin.site.register(Event, EventAdmin)
