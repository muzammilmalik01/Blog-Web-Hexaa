from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryCreate.as_view(), name = 'list-category'),
    path('detail/<int:pk>', views.CategoryDetail.as_view(), name = 'category-detail'),
]