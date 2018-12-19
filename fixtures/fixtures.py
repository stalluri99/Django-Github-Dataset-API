# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import RequestsClient
import json
from dateutil.parser import parse
from RestAPI.models import Actor, Repo

data = []
with open('fixtures/events_data.json') as f:
    for line in f:
        data.append(line)

def create_data():
    Actor.objects.all().delete()
    Repo.objects.all().delete()

    client = RequestsClient()
    for ro in data:
        row = json.loads(ro)
        res = {}
        if row['request']['method'] == "GET":
            res = client.get('http://localhost:8000' + row['request']['url'] + '/')
        elif row['request']['method'] == "POST":
            res = client.post(
                'http://localhost:8000' + row['request']['url'] + '/', json=row['request']['body'])
        elif row['request']['method'] == "DELETE":
            res = client.delete(
                'http://localhost:8000' + row['request']['url'] + '/')
        elif row['request']['method'] == "PUT":
            res = client.put('http://localhost:8000' + row['request']['url'] + '/', json=row['request']['body'])
        if row['response']['headers'] != {}:
            pass
        if row['request']['url'] in ['/actors','/actors/streak'] and row['request']['method'] == 'GET':
            pass
        elif row['response']['body'] != {}:
            response = json.loads(res.text)
            for resp in response:
                if resp['created_at']:
                    temp = parse(resp['created_at'])
                    temp = temp.replace(tzinfo=None)
                    temp = str(temp)
                    resp['created_at'] = temp

if __name__=="__main__":
    create_data()
