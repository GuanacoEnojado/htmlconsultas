from rest_framework import serializers
from .models import Usuario, trabajador, Agenda

class trabajadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = trabajador
        fields = '__all__'
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido')
        
class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agenda
        fields = '__all__'