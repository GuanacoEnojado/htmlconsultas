from django.urls import path
from .views import index, registrarse

urlpatterns = [
    path('', index, name='index'),
    path('registrarse/', registrarse, name='registrarse')
    ]
