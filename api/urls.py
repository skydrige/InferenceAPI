from django.urls import path
from . import views

urlpatterns = [
    path('api', views.index, name='index'),
    path('s', views.test, name='test'),
    path('', views.directForm, name='directForm'),
    path('summary', views.directSummary, name='directSummary'),
]
