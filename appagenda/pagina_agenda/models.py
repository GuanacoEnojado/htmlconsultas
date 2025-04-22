from django.db import models

# Create your models here.
class usuario(models.Model):
    id_usuario=models.IntegerField(max_length=10)
    nombre=models.CharField(max_length=40)
    rut=models.CharField(max_length=12)
    correo=models.CharField(max_length=40)
    telefono=models.IntegerField(max_length=13)
    direccion=models.CharField(max_length=40)

#aqui iria el resto de las tablas generadas al servidor de oracle