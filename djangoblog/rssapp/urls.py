from django.urls import path
from . import views

app_name = 'rssapp'

urlpatterns = [
    path('user/', views.rss_view, name='rssapp'),
    path('api/', views.ApiRssFeedAdmin.as_view(), name='api'),
    path('api/update/', views.ApiRssFeedRetrieve.as_view(), name='api2'),
    path('adding/', views.rss_add, name='add'),
]
