from django.urls import path
from . import views

urlpatterns = [
    path('subscribe/', views.AddSubscriberAPI.as_view(), name = 'subscribe-newsletter'),
    path('send/', views.SendNewsLetterAPI.as_view(), name = 'send-newsletter'),
    path('unsubscribe/<str:email>/', views.UnsubscribeAPI.as_view(), name = 'unsubscribe-newsletter'),
]
