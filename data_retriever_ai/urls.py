from django.urls import path
from . import views

urlpatterns = [
    path('ai-chat/', views.ai_chat_page_view, name='ai_chat'),  # Homepage
    path('send-message/', views.send_message, name='send_message'),
]
