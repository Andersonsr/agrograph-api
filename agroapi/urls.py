from django.urls import path
from . import views

urlpatterns =[
    path('hello/', views.helloWorld, name='index'),
    path('auth/', views.authUser, name='auth')
]