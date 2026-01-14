from django.urls import path
from . import views

urlpatterns = [
    path('', views.CepListView.as_view()),
    path('ceps/', views.CepListView.as_view(), name='ceps'),
]