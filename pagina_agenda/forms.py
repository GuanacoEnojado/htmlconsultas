from .models import Usuario
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Agenda, trabajador, horas
from django.forms.widgets import DateInput, TimeInput, Select, TextInput, NumberInput, Textarea



class CreateUserForm(UserCreationForm):
    id = forms.CharField(label='Id', required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Rut o pasaporte'
    }))
    nombre = forms.CharField(label='Nombre', required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Nombre'
    }))
    apellido = forms.CharField(label='Apellido', required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Apellido'
    }))
    fecha_nacimiento = forms.DateField(label='Fecha de nacimiento', required=True, widget=forms.DateInput(attrs={
        'class':'form-control',
        'placeholder':'Fecha de nacimiento'
    }))
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Email'
    }))
    telefono = forms.IntegerField(label='Teléfono', widget=forms.NumberInput(attrs={
        'class':'form-control',
        'placeholder':'Telefono'
    }))
    password = forms.CharField(label='Contraseña1', required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Contraseña'
    }))
    password2 = forms.CharField(label='Contraseña2', required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirma Contraseña'
    }))
    class Meta:
        model = Usuario
        fields = ('nombre', 'apellido', 'fecha_nacimiento', 'email', 'telefono', 'password1', 'password2', 'Id')

class AuthForm(AuthenticationForm):
    username = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Rut o pasaporte'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Contraseña'})
    )
    class Meta:
        model = Usuario
        fields = ('username', 'password')

class PatientForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre','apellido', 'fecha_nacimiento', 'email', 'telefono']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'apellido': TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': DateInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
            'telefono': NumberInput(attrs={'class': 'form-control'}),
        }

class ProSelectForm(forms.Form):
    profesional = forms.ModelChoiceField(
        queryset=trabajador.objects.all(),
        widget=Select(attrs={'class':'form-control', 'id':'pro-select'}),
        empty_label="Elige a un profesional"
    )
    cita = forms.DateField(
        widget=DateInput(attrs={'class':'form-control', 'type':'date', 'id':'fecha-select'})
    )

class ElegirHora(forms.Form):
    hora = forms.ModelChoiceField(
        queryset=Agenda.objects.none(),
        widget=Select(attrs={'class':'form-control'}),
        empty_label="Elige una hora"
    )

def __init__(self, *args, **kwargs):
    doctor_id = kwargs.pop('doctor_id',None)
    hora = kwargs.pop('hora', None)
    super(ElegirHora, self).__init__(*args, **kwargs)

    if doctor_id and hora:
        self.fields['hora'].queryset = horas.objects.filter(
            doctor_id=doctor_id,
            hora=hora,
            estado = True
        )
#
