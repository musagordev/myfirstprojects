from django.urls import path

from . import views

app_name ="hello_session"
urlpatterns = [
    path('', views.sessfun, name='sessfun'),
]