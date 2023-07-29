from django.urls import path
from .views.login import login_view
from .views.logout import logout_view
from .views.editUser import editUser
from .views.createUser import createUser
from .views.read import read
from .views.write import insert
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('sign-in/', createUser, name='sign-in'),
    path('edit-profile/', editUser, name='edit profile'),
    path('insert/', insert, name='insert data'),
    path('measurements/', read, name='read data')
]