from django.urls import path
from .views import userManagement, dataManagement


urlpatterns = [
    path('login/', userManagement.login, name='login'),
    path('logout/', userManagement.logout, name='logout'),
    path('sing-in/', userManagement.createUser, name='sing-in'),
    path('edit-profile/', userManagement.editUser, name='edit profile'),
    path('insert/', dataManagement.insert, name='insert data')
]