from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Votante,Candidato, Voto
from .forms import VotanteForm, CandidatoForm
from .serializers import VotanteSerializer,CandidatoSerializer,VotoSerializer



@api_view(['GET', 'POST'])
def votante_list_api(request):
    if request.method == 'GET':
        votantes = Votante.objects.all()
        serializer = VotanteSerializer(votantes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VotanteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def candidato_list_api(request):
    if request.method == 'GET':
        candidatos = Candidato.objects.all()
        serializer = CandidatoSerializer(candidatos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CandidatoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def buscar_votante(request):
    nombre = request.data.get('nombre')
    dni = request.data.get('numero_documento')

    try:
        votante = Votante.objects.get(nombre=nombre, numero_documento=dni)
        return Response({"localidad": votante.localidad}, status=status.HTTP_200_OK)
    except Votante.DoesNotExist:
        return Response({"error": "Votante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def listar_candidatos(request, localidad):
    candidatos = Candidato.objects.filter(localidad=localidad)
    serializer = CandidatoSerializer(candidatos, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def registrar_voto(request):
    serializer = VotoSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()  # Ahora el serializer maneja la creación del voto

    return Response(serializer.data, status=status.HTTP_201_CREATED)



def votacion_view(request):
    localidad = None
    candidatos = []
    mensaje = ""
    
    if request.method == 'POST':
        if 'buscar_votante' in request.POST: 
            nombre = request.POST.get('nombre')
            dni = request.POST.get('numero_documento')

            try:
                votante = Votante.objects.get(nombre=nombre, numero_documento=dni)
                localidad = votante.localidad
                candidatos = Candidato.objects.filter(localidad=localidad)
                request.session['votante_id'] = votante.id  
            except Votante.DoesNotExist:
                mensaje = "Votante no encontrado."

        elif 'registrar_voto' in request.POST:  
            votante_id = request.session.get('votante_id')
            candidato_id = request.POST.get('candidato_id')

            if votante_id and candidato_id:
                try:
                    votante = Votante.objects.get(id=votante_id)
                    candidato = Candidato.objects.get(id=candidato_id)

                    # Verificar si el votante ya votó
                    if Voto.objects.filter(votante=votante).exists():
                        mensaje = "Este votante ya ha votado."
                    else:
                        Voto.objects.create(votante=votante, candidato=candidato)
                        mensaje = "Voto registrado con éxito."
                except (Votante.DoesNotExist, Candidato.DoesNotExist):
                    mensaje = "Error al registrar el voto."

    return render(request, "votacion.html", {"localidad": localidad, "candidatos": candidatos, "mensaje": mensaje})

    
def candidato_form_view(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid(): 
            return redirect('candidato_form')

    else:
        form = CandidatoForm()
    
    return render(request, "candidato.html", {"form": form})

def votante_form_view(request):
    if request.method == 'POST':
        form = VotanteForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect("votante_form")

    else:
        form = VotanteForm()
    
    return render(request, "votante.html", {"form": form})
 