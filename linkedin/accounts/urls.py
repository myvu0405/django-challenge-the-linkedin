from django.urls import path

from .views import *


urlpatterns = [
    path('login/', joinPage, name='login'),
    # path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name='logout'),
    path('profile/<int:pk>/', profilePage, name='profile'),
    path('members/', membersPage, name='members'),

    
]
