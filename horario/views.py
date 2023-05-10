from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages #para mandar mensajes de error
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Event, Position


#Ruta principal:
def horario(request):
    return render(request,"horario.html")



#Registro de usuario, login y logout:
def user_login(request):
    
    if request.method == "POST":
        username = request.POST.get("usuario").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,"¡Usuario no existe!")
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(reverse('horario'))
        elif user == None:
            messages.error(request,"¡Clave erronea!")

    return render(request,"user_login.html")


@login_required(login_url = "user_login")
def user_logout(request):
    logout(request)
    return redirect(reverse('user_login'))




def user_register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect(reverse("horario"))
        
    return render(request,'user_register.html',{'UserCreationForm':UserCreationForm})
        
    



#Adquirir datos de sueño:
'''
Atributos:
#User_id 
#priority = 10
#name = horario_suenio
#Event_type = Actividad_no_fija
        

Constraints:
#time_goal: horas semanales sueño
#time_goal_counter: horas semanales sueño
#max_levantarse: hora máxima levantar
#max_acostarse: hora máxima acostar 
#max_time: máximo tiempo de dormir seguido
'''
@login_required(login_url = "user_login")
def suenio(request):
    user = User.objects.get(pk = request.user.pk)
    if request.method == "POST":
        
        #Adquirir atributos y constraints:
        priority = 10
        name = "horario_suenio"
        event_type = "suenio"
        time_goal = request.POST["horas_suenio"]
        time_goal_counter = time_goal
        max_levantarse = request.POST["hora_maxima_levantar"]
        max_acostarse = request.POST["hora_maxima_acostar"]
        max_time = request.POST["longitud_maxima_suenio"]
        constraints = {'time_goal':time_goal,'time_goal_counter':time_goal_counter,'max_levantarse':max_levantarse,'max_acostarse':max_acostarse,'max_time':max_time}

        #Instanciar y guardar Event:
        nuevo_horario_suenio = Event(user_id=user,priority=priority,name=name,event_type=event_type,constraints=constraints)
        nuevo_horario_suenio.save()
        return redirect(reverse("actividades_fijas"))
        

    elif request.method == "GET":
        horario_suenio = Event.objects.filter(user_id = user.pk)
        horario_suenio = horario_suenio.filter(event_type="suenio")
        return render(request,"suenio.html",{"horario_suenio":horario_suenio})
    

@login_required(login_url = "user_login")
def eliminar_suenio(request,ruta_suenio):
    suenio = Event.objects.get(pk = ruta_suenio)
    suenio.delete()
    return redirect(reverse("suenio"))




#Adquirir y mostrar actividades fijas:
'''
Atributos:
#User_id 
#priority = 10
#name
#Event_type = Actividad_no_fija
        

Constraints:
#No maneja constraints
'''
@login_required(login_url = "user_login")
def actividades_fijas(request):
    usuario = User.objects.get(pk=request.user.pk)
    if request.method == "POST":
        
        #Instanciar Event:
        nombre = request.POST['name']
        prioridad = 10
        tipo_evento = "actividad_fija"

        nueva_actividad_fija = Event(user_id = usuario, priority = prioridad, name=nombre, event_type=tipo_evento)
        nueva_actividad_fija.save()

        #Crear registro de Position para cada posicion que ocupa el evento:
        dia_actividad = int(request.POST['dia_actividad'])
        hora_actividad = int(request.POST["hora_actividad"])-1
        duracion_actividad = int(request.POST["duracion_actividad"])
        hora_final = hora_actividad + duracion_actividad

        for hora in range(hora_actividad,hora_final,1):
            posicion_actividad_fija = Position(event_id = nueva_actividad_fija,user_id = usuario,day=dia_actividad,hour = hora)
            posicion_actividad_fija.save()
        return redirect(reverse("actividades_fijas"))

    
    elif request.method == "GET":
        actividades_fijas = Event.objects.filter(user_id = usuario)
        actividades_fijas =actividades_fijas.filter(event_type = "actividad_fija")
        return render(request,"actividades_fijas.html",{"actividades_fijas":actividades_fijas})



@login_required(login_url = "user_login")
def eliminar_actividades_fijas(request,ruta_actividad_fija):
    actividad_fija = Event.objects.get(pk = ruta_actividad_fija)
    actividad_fija.delete()
    return redirect(reverse("actividades_fijas"))


"""
Atributos:
# User_id -
# priority -
# Name -
# Event_type = actividad_no_fija -

Constraints:
# time_goal: horas semanales actividad 
# time_goal_counter: horas semanales actividad 2
# earliest_hour: hora más temprana
# latest_hour: hora máxima realizar actividad  
# max_time: máximo tiempo para realizar actividad
"""

#Adquirir y mostrar actividades no fijas
@login_required(login_url = "user_login")
def actividades_no_fijas(request):
    user = User.objects.get(pk = request.user.pk)
    if request.method == "POST":
         
        #Adquirir atributos y constraints: 
        priority = request.POST["priority"]
        name = request.POST["name"]
        event_type = "actividad_no_fija"
        time_goal = request.POST["horas_semanales"]
        time_goal_counter = time_goal
        earliest_hour = request.POST["hora_mas_temprana"]
        latest_hour = request.POST["hora_mas_tarde"]
        max_time = request.POST["tiempo_maximo"]
        constraints = {'time_goal':time_goal,'time_goal_counter':time_goal_counter,'earliest_hour':earliest_hour,'latest_hour':latest_hour,'max_time':max_time}

        #Instanciar y guardar Evento no fijo:
        nuevo_evento_no_fijo = Event(user_id=user,priority=priority,name=name,event_type=event_type,constraints=constraints)
        nuevo_evento_no_fijo.save()
        return redirect(reverse("actividades_no_fijas"))


    elif request.method == "GET":
        actividades_no_fijas = Event.objects.filter(user_id = user.pk)
        actividades_no_fijas = actividades_no_fijas.filter(event_type = "actividad_no_fija")
        return render(request,"actividades_no_fijas.html",{'actividades_no_fijas':actividades_no_fijas})



@login_required(login_url = "user_login")
def eliminar_actividades_no_fijas(request,ruta_actividad_no_fija):
    actividad_no_fija = Event.objects.get(pk = ruta_actividad_no_fija)
    actividad_no_fija.delete()
    return redirect(reverse("actividades_no_fijas"))




#Vista que crea el horario final y lo muestra en pantalla:
@login_required(login_url = "user_login")
def horario_final(request):
    
    return render(request,"horario_final.html")

