from django.urls import path
from . import views
urlpatterns = [
    path('', views.chatboat_view, name='chat_page'), 
    path('course', views.home_view, name='home'), 
]
