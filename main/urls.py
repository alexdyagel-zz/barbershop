from django.urls import path, include

from main import views

app_name = 'main'

urlpatterns = [
    path('main/', include('django.contrib.auth.urls')),
    path('registration/', views.register, name='registration'),
    path('order1/', views.step1, name='order1'),
    path('order2/', views.step2, name='order2'),
    path('order3/', views.step3, name='order3'),
    path('', views.index, name='home'),
]
