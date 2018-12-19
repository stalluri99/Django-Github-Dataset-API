# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.test import RequestsClient
import json
from dateutil.parser import parse
from RestAPI.models import Actor, Repo

data = []
with open('TestData/http_fix.json') as f:
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
            print("GET request in fixtures")
            res = client.get('http://localhost:8000' + row['request']['url'] + '/')
        elif row['request']['method'] == "POST":
            print("POST request in fixtures")
            res = client.post(
                'http://localhost:8000' + row['request']['url'] + '/', json=row['request']['body'])
        elif row['request']['method'] == "DELETE":
            print("DELETE request in fixtures")
            res = client.delete(
                'http://localhost:8000' + row['request']['url'] + '/')
        elif row['request']['method'] == "PUT":
            print("PUT request in fixtures")
            res = client.put('http://localhost:8000' + row['request']['url'] + '/', json=row['request']['body'])
        # assertEqual(res.status_code, row['response']['status_code'])
        if row['response']['headers'] != {}:
            pass
            # assertEqual(res.headers['Content-Type'], row['response']['headers']['Content-Type'])
        if row['request']['url'] in ['/actors','/actors/streak'] and row['request']['method'] == 'GET':
            pass
            # assertEqual(sorted(json.loads(res.text)), sorted(row['response']['body']))
        elif row['response']['body'] != {}:
            response = json.loads(res.text)
            for resp in response:
                if resp['created_at']:
                    temp = parse(resp['created_at'])
                    temp = temp.replace(tzinfo=None)
                    temp = str(temp)
                    resp['created_at'] = temp
            # assertEqual(response, row['response']['body'])

if __name__=="__main__":
    create_data()
