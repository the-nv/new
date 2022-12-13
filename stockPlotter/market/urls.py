from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gann/1/<str:pivotTimestamp>/', views.gannDateForecast1, name='gannDateForecast1'),
    path('<str:securityName>/', views.detail, name='detail'),
]