from django.shortcuts import render
from django.http import HttpResponse
from neo4j import GraphDatabase, basic_auth
# Create your views here.


def helloWorld(request):
    return HttpResponse('hello world')


def authUser(request):
    driver = GraphDatabase.driver('bolt://127.0.0.1:7687',
                                  auth=basic_auth('neo4j', '123456'))
    with driver.session() as session:
        result = session.run('CREATE (a:User{nome:\'pedro\'}) return a.nome as nome')
    return HttpResponse(result)
