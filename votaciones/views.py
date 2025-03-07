from django.shortcuts import render
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
    """Valida el nombre y DNI, y devuelve la localidad"""
    nombre = request.data.get('nombre')
    dni = request.data.get('numero_documento')

    try:
        votante = Votante.objects.get(nombre=nombre, numero_documento=dni)
        return Response({"localidad": votante.localidad}, status=status.HTTP_200_OK)
    except Votante.DoesNotExist:
        return Response({"error": "Votante no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def listar_candidatos(request, localidad):
    """Devuelve los candidatos de la misma localidad"""
    candidatos = Candidato.objects.filter(localidad=localidad)
    serializer = CandidatoSerializer(candidatos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def registrar_voto(request):
    """Registra el voto en la base de datos"""
    votante_id = request.data.get('votante_id')
    candidato_id = request.data.get('candidato_id')

    try:
        votante = Votante.objects.get(id=votante_id)
        candidato = Candidato.objects.get(id=candidato_id)

        # Verifica si el votante ya votó
        if Voto.objects.filter(votante=votante).exists():
            return Response({"error": "El votante ya ha votado"}, status=status.HTTP_400_BAD_REQUEST)

        # Registra el voto
        voto = Voto.objects.create(votante=votante, candidato=candidato)
        return Response(VotoSerializer(voto).data, status=status.HTTP_201_CREATED)

    except (Votante.DoesNotExist, Candidato.DoesNotExist):
        return Response({"error": "Votante o Candidato no válido"}, status=status.HTTP_400_BAD_REQUEST)




def votar(request):
    return render(request, "VOTACION.html")
    
def candidato_form_view(request):
    if request.method == 'POST':
        form = CandidatoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda en la base de datos
            return render(request, "success.html")  # Redirige a una página de éxito

    else:
        form = CandidatoForm()
    
    return render(request, "candidato.html", {"form": form})

def votante_form_view(request):
    if request.method == 'POST':
        form = VotanteForm(request.POST)
        if form.is_valid():
            form.save()  # 👈 Guarda directamente en la base de datos
            return render(request, "success.html")  # Redirige a una página de éxito

    else:
        form = VotanteForm()
    
    return render(request, "votante.html", {"form": form})
