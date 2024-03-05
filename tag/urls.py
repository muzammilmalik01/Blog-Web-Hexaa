from django.urls import path
from . import views

urlpatterns = [
    path('',views.ListCreateAPI.as_view(), name = 'list-tags'),
    path('detail/<int:pk>', views.DetailAPI.as_view(), name = 'detail-tag'),
]
