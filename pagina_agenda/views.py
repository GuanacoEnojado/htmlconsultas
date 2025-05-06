from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CreateUserForm, AuthForm
from django.http import JsonResponse
from .models import horas, Agenda, trabajador, Usuario
from .forms import ElegirHora, ProSelectForm, PatientForm
from .forms import CreateUserForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .serializers import UsuarioSerializer, trabajadorSerializer, AgendaSerializer 
from rest_framework import viewsets


# Create your views here.





def home(request):
    return render(request, 'index.html')

def pagregistro(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro exitoso')
            return redirect('index.html')
        else:
            messages.error(request, 'Registro fallido')
    else:
        form = CreateUserForm()
        context = {'form':form}
    return render(request, 'registrarse.html', context)

def paglogin(request):
    if request.method == 'POST':
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            id = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=id, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'ingreso exitoso!')
                return redirect('index.html')
            else:
                messages.error(request, 'ingreso fallido')
        else:
            form=AuthForm()
        context = {'form':form}
        return render(request, 'login.html', context)
def logout(request):
    logout(request)
    return redirect ('login.html')
#no implementado aun


@login_required
def Agenda1(request):
    #elegir profesional y hora
    pro_form = ProSelectForm()
    
    if request.method == 'POST':
        pro_form = ProSelectForm(request.POST)
        if pro_form.is_valid():
            # guardar info en sesion
            request.session['doctor'] = pro_form.cleaned_data['profesional'].id
            request.session['hora'] = pro_form.cleaned_data['hora'].strftime('%Y-%m-%d')
            return redirect('Agenda2')
    
    return render(request, 'Agenda2.html', {
        'form': pro_form
    })

@login_required
def Agenda2(request):
    #chequea paso 1
    if 'doctor' not in request.session:
        messages.error(request, 'Please select a profesional and hora first.')
        return redirect('Agenda1')
    
    doctor = request.session['doctor']
    hora = request.session['hora']
    
    espacio_hora = ElegirHora(doctor=doctor, hora=hora)
    
    if request.method == 'POST':
        espacio_hora = ElegirHora(request.POST, doctor=doctor, hora=hora)
        
        if espacio_hora.is_valid():
            # sacar datos de paciente registrado
            try:
                paciente = request.user.paciente
            except:
                paciente = Usuario.objects.create(
                    user = request.user,
                    id = id
                )
        #crear cita, no se que estoy haciendo mal, ayudaaa
            cita = ElegirHora.save(commit=False)
            cita.paciente = paciente
            cita.profesional = trabajador.objects.get(id=doctor)
            cita.hora = espacio_hora.cleaned_data['hora']
            cita.save()
            
            # limpiar
            for key in ['doctor', 'hora']:
                if key in request.session:
                    del request.session[key]
            
            messages.success(request, 'Agendado exitosamente!')
            return redirect('confirmacion_cita', cita_id=cita.id)
    
    return render(request, 'Agenda2.html', {
        'espacio_hora': espacio_hora,
    })

def confirmacion_cita(request, cita_id):
    cita = get_object_or_404(cita, id=cita_id)
    return render(request, 'citas/confirmation.html', {
        'cita': cita
    })

def get_available_slots(request):
    doctor = request.GET.get('doctor')
    hora = request.GET.get('hora')
    
    if not doctor or not hora:
        return JsonResponse({'error': 'auxilio'}, status=400)
    
    hora_disp = horas.objects.filter(
        doctor=doctor,
        hora=hora,
        estado=True
    )
    
    data = [{'id': slot.id, 'time': f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"} 
            for slot in hora_disp]
    
    return JsonResponse({'slots': data})

@login_required
def Mis_citas(request):
    """View for users to see their citas."""
    try:
        paciente = Usuario.objects.get(user=request.user)
        citas = cita.objects.filter(paciente=paciente)
    except Usuario.DoesNotExist:
        citas = []
    #no se por que no me reconoce cita, voy a morir
    return render(request, 'consulta.html', {
        'citas': citas
    })
#no implementado aun

@login_required
@require_POST
def cancel_appointment(request, cita_id):
    ##no implementado aun, queda poco tiempo, cortisol al maximo
    cita = get_object_or_404(cita, id=cita_id)
    
    # Chequeo de usuario vs paciente
    if request.user.paciente != cita.paciente:
        messages.error(request, 'No hay permiso')
        return redirect('Mis_citas')
    
    # cancelar y cambiar el estado de la cita en la base de datos
    cita.status = 'Cancelado'
    cita.save()
    
    hora = cita.hora
    hora.estado = True
    hora.save()
    
    messages.success(request, 'cita cancelada exitosamente.')
    return redirect('Mis_citas')

###Esto me está costando muchísimo, algo salió muy mal en algún punto y no puedo partir el servidor. Parece que hay un conflicto con la autenticación 
# y tendré que realizar nuevamente un sistema de registro y login, pero que esté separado del sistema de agenda. Juntarlos quebró el sistema


##API solo GET
def api_Usuarios(request):
    usuarios = Usuario.objects.all()
    data = UsuarioSerializer.objects.all(usuarios, many=True).data
    return JsonResponse(data, safe=False)
##API con POST, GET, DELETE, PUT
class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer