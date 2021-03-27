from django.urls import path
from . import views

app_name = 'rssapp'

urlpatterns = [
    path('user/', views.rss_view, name='rssapp'),
    path('api/', views.API_rss.as_view(), name='api'),
    path('adding/', views.rss_add, name='add'),
]
