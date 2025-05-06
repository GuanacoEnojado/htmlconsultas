from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, Id, password=None, **extra_fields):
        if not Id:
            raise ValueError('Necesitas llenar rut/pasaporte')
        user = self.model(Id=Id, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(null=False, blank=False)
    email = models.EmailField(max_length=50)
    telefono = models.IntegerField(max_length=9)
    Id = models.CharField(max_length=20, unique=True)
    USERNAME_FIELD = 'Id'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'email', 'Id', 'fecha_nacimiento']
    objects = CustomUserManager()
    
    
# Si el usuario de elimina de la base de datos, se eliminarían todas sus citas


class trabajador(models.Model):
    nombre_especialista = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=80)
    telefono_contacto = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.specialization}"

class Agenda(models.Model):
    profesional = models.ForeignKey(trabajador, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    dia = models.DateField()
    hora = models.TimeField()

class horas(models.Model):
    estados = (
        ('agendado', 'Agendado'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado')
    )
    paciente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    doctor = models.ForeignKey(trabajador, on_delete=models.CASCADE)
    hora = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=estados, default='agendado')

def __str__(self):
    return f"{self.paciente.nombre} {self.paciente.apellido} con {self.doctor.nombre_especialista} en {self.hora.dia} {self.hora.hora}"

def save(self, *args, **kwargs):
    if self.status == 'Agendado':
        self.agenda.disponible = False
        self.agenda.save()
    super().save(*args, **kwargs)

