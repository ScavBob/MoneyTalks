from django.urls import path

from . import views

urlpatterns = [
    path('', views.EventView.as_view(), name='index'),
    path('signup/', views.EventView.as_view(), name='sign-up')
]