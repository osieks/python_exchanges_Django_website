#why i created new urls.py?
from django.urls import path
from . import views

urlpatterns = [
    path('crypto/', views.index, name='index'),
    path('crypto/data/', views.data_table, name='data_table'),
    path('crypto/clear_data/', views.clear_data, name='clear_data'),
    path('crypto/update_data/', views.update_data, name='update_data'),
]
