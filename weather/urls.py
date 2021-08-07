from django.urls import path
from . import views
from .views import delete

urlpatterns = [
    path('', views.index,name="home"),
    path('delete/<city_name>', views.delete,name='delete_city'),
]
