from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('chat/', views.chat_view, name='chat')
]
