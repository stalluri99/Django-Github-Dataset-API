# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import make_aware

from rest_framework import viewsets
from rest_framework.decorators import api_view

from .serializers import ActorSerializer, RepoSerializer, EventSerializer
from .models import Actor, Repo, Event
from .utils import make_datetime_object

# @api_view(['GET', 'POST'])
# def events_index(request):
#     """Docstring"""

#     if request.method == 'POST':
        
#         data = request.data
#         print("REQUEST DATA: ", data)

#         event_id = int(data["id"])
#         event_type = data["type"]
#         created_at = make_aware(make_datetime_object(data["created_at"]))

#         actor = data["actor"]
#         actor_id = int(actor["id"])
#         login = actor["login"]
#         avatar_url = actor["avatar_url"]

#         repo = data["repo"]
#         repo_id = int(repo["id"])
#         repo_name = repo["name"]
#         repo_url = repo["url"]

#         act = Actor.objects.get_or_create(id=actor_id, login=login, avatar_url=avatar_url)[0]
#         rep = Repo.objects.get_or_create(id=repo_id, name=repo_name, url=repo_url)[0]
#         try:
#             Event.objects.get(id=event_id)
#             return HttpResponse("Event already exists", status=400)
#         except:
#             eve, created = Event.objects.get_or_create(id=event_id, type=event_type, actor=act, repo=rep, created_at=created_at)
#             return HttpResponse("Object created", status=201)
#     if request.method == 'GET':
#         events = []
#         for e in Event.objects.all():
#             serialized_event = EventSerializer(e)
#             events.append(serialized_event.data)
#         return JsonResponse(events, safe=False)


class EventViewSet(viewsets.ModelViewSet):
    """Docstring"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request):
        if request.method == 'POST':
            data = request.data

            event_id = int(data["id"])
            event_type = data["type"]
            created_at = make_aware(make_datetime_object(data["created_at"]))

            actor = data["actor"]
            actor_id = int(actor["id"])
            login = actor["login"]
            avatar_url = actor["avatar_url"]

            repo = data["repo"]
            repo_id = int(repo["id"])
            repo_name = repo["name"]
            repo_url = repo["url"]

            act = Actor.objects.get_or_create(id=actor_id, login=login, avatar_url=avatar_url)[0]
            rep = Repo.objects.get_or_create(id=repo_id, name=repo_name, url=repo_url)[0]
            try:
                Event.objects.get(id=event_id)
                return HttpResponse("Event already exists", status=400)
            except:
                eve, created = Event.objects.get_or_create(id=event_id, type=event_type, actor=act, repo=rep, created_at=created_at)
                return HttpResponse("Object created", status=201)      

    def destroy(self, request, *args, **kwargs):
        print("Destroy called")
        if request.method == 'DELETE':
            return super().destroy(request, *args, **kwargs)


class ActorViewSet(viewsets.ModelViewSet):
    """Docstring"""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def put(self, request, pk=None):
        data = request.data
        actor_id = data["id"]
        login = data["login"]
        avatar_url = data["avatar_url"]
        try:
            actor = Actor.objects.get(id=actor_id)
            actor.avatar_url = avatar_url # update the avatar_url

            if actor.login != login: # if the login has changed, return 400
                actor.login = login
                status = 400
            else:
                status = 200
            actor.save()
            return HttpResponse("Actor avatar_url updated successfully", status=status)
        except Actor.DoesNotExist:
            raise Http404("Actor does not exist")


@api_view(['GET', 'PUT'])
def actors_view_index(request):
    print("Actor indexw")
    if request.method == 'GET':
        actors = []
        for actor in Actor.objects.all():
            serialized_actor = ActorSerializer(actor)
            actors.append(serialized_actor.data)
        return JsonResponse(actors, safe=False)

    if request.method == 'PUT':
        data = request.data
        actor_id = data["id"]
        login = data["login"]
        avatar_url = data["avatar_url"]
        try:
            actor = Actor.objects.get(id=actor_id)
            actor.avatar_url = avatar_url # update the avatar_url

            if actor.login != login: # if the login has changed, return 400
                actor.login = login
                status = 400
            else:
                status = 200
            actor.save()
            return HttpResponse("Actor avatar_url updated successfully", status=status)
        except Actor.DoesNotExist:
            raise Http404("Actor does not exist")


@api_view(['GET', 'POST'])
def actor_events(request, id):
    print("actor id", id)
    try:
        actor = Actor.objects.get(id=int(id))
        actor_events = Event.objects.filter(actor__id=int(id))
        data = []
        for event in actor_events:
            serialized_event = EventSerializer(event)
            data.append(serialized_event.data)
        return JsonResponse(data, safe=False)
    except Actor.DoesNotExist:
        raise Http404("Actor does not exist")


@api_view(['GET', 'POST'])
def actors_by_streak(request):
    if request.method == 'GET':
        print("Actors streak")
        actors = []
        for actor in Actor.objects.all().order_by('-streak',  '-latest_event_timestamp', 'login'):
            serialized_actor = ActorSerializer(actor)
            actors.append(serialized_actor.data)
        return JsonResponse(actors, safe=False)


class RepoViewSet(viewsets.ModelViewSet):
    """Docstring"""
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer


@api_view(['GET', 'DELETE'])
def erase_all_events(request):
    print("Erase view called")
    Event.objects.all().delete()
    return JsonResponse({'erase' : 'Deleted all events'})
