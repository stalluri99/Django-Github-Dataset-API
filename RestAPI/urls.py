# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('events', views.EventViewSet)
router.register('repos', views.RepoViewSet)

app_name = 'RestAPI'

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^erase/$', views.erase_all_events),
    url(r'^actors/$', views.actors_index),
    url(r'^actors/streak/$', views.actors_by_streak),
    url(r'^events/actors/(?P<id>[0-9]+)/$', views.actor_events, name='actor_events'),
    url(r'^api-auth/', include('rest_framework.urls'), name='rest_framework')
]
