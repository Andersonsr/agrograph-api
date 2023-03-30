from django.urls import path
from .views.login import login
from .views.logout import logout
from .views.editUser import editUser
from .views.createUser import createUser
from .views.read import read
from .views.write import insert

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('sing-in/', createUser, name='sing-in'),
    path('edit-profile/', editUser, name='edit profile'),
    path('insert/', insert, name='insert data'),
    path('read/', read, name='read data')
]