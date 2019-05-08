from django.urls import path, include

from main import views

app_name = 'main'

urlpatterns = [
    path('main/', include('django.contrib.auth.urls')),
    path('', views.index, name='home'),
]
