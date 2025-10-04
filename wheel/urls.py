from django.urls import path
from . import views

urlpatterns = [
    path('', views.wheel_page, name='wheel_page'),
    path('spin/', views.spin_wheel, name='spin_wheel'),
]