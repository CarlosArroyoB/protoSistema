from rest_framework import serializers
from .models import Votante, Candidato,Voto

##se convierten los datos complejos en formato JSON o XML

class VotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        fields = '__all__'

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidato
        fields = '__all__'

class VotoSerializer(serializers.ModelSerializer):
    votante_id = serializers.IntegerField(write_only=True)  
    candidato_id = serializers.IntegerField(write_only=True)  

    class Meta:
        model = Voto
        fields = ['id', 'votante_id', 'candidato_id']  

    def create(self, validated_data):
        votante_id = validated_data.pop('votante_id')
        candidato_id = validated_data.pop('candidato_id')

        # Buscar los objetos en la base de datos
        votante = Votante.objects.get(id=votante_id)
        candidato = Candidato.objects.get(id=candidato_id)

        # Crear el voto con las relaciones correctas
        return Voto.objects.create(votante=votante, candidato=candidato)
