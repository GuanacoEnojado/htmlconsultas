from django.urls import path, include
from . import views
from .views import api_Usuarios, AgendaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Agenda', AgendaViewSet, basename = 'Agenda')

urlpatterns = [
    path('', views.home, name='index'),
    path('registrarse', views.pagregistro, name='registrarse'),
    path('login', views.paglogin, name='login' ),
    path('api/usuarios', api_Usuarios, name='api_usuarios'),
    path('api/', include(router.urls))
]

