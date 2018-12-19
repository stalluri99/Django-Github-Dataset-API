
import os
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event

@receiver(post_save, sender=Event)
def update_actor_event_count(sender, instance, **kwargs):
    actor = instance.actor
    actor.event_count = actor.event_set.count()
    actor.latest_event_timestamp = instance.created_at
    actor.save()
