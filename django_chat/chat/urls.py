from django.conf import settings
from django.urls import path

from . import views

# api_router = routers.SimpleRouter()
#
# api_router.register(prefix="messages", viewset=views.MessagesAPIView)

urlpatterns = [
    path('', views.home_view, name='home'),
    path('chat/', views.chat_view, name='chat'),
    path(settings.API_URL[1:] + "chat/messages/", views.MessagesAPIView.as_view())
]
