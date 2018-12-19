
import os
from datetime import timedelta

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event

@receiver(post_save, sender=Event)
def update_actor_event_count(sender, instance, **kwargs):
    actor = instance.actor
    actor.event_count = actor.event_set.count()

    # if actor has no latest_event_timestamp, then actor has not worked today
    # so pushed_today is False
    try:
        if actor.latest_event_timestamp.day == instance.created_at.day:
            actor.pushed_today = True # actor already created an event today
        else:
            actor.pushed_today = False
    except AttributeError:
        actor.pushed_today = False
    actor.save(update_fields=['pushed_today', 'event_count'])

    # update the streak
    # if new event date is 1 day plus actor's latest_event_timestamp, increase streak by 1
    event_day = instance.created_at.day
    print("Event day: ", event_day)

    try:
        actor_latest_event_day = actor.latest_event_timestamp.day
        print("Actor latest event day: ", actor_latest_event_day)
        if (event_day == (actor_latest_event_day + 1)) and (actor.pushed_today is False):
            actor.streak = actor.streak + 1
    except AttributeError:
        actor.streak = 1

    actor.latest_event_timestamp = instance.created_at
    actor.save()
