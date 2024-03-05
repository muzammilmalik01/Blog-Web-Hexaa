from django.urls import path
from . import views

urlpatterns = [
    
    path('all', views.AllAccountsListAPI.as_view(), name = 'all-accounts'), # lists all users
    path('create/',views.CreateAccountAPI.as_view(), name='create-user'), # creates a new users
    path('detail/<int:pk>',views.DetailAccountAPI.as_view(), name='detail-user'), # access details of user
]
