#why i created new urls.py?
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data/', views.data_table, name='data_table'),
    path('clear_data/', views.clear_data, name='clear_data'),
    path('update_data/', views.update_data, name='update_data'),
]
