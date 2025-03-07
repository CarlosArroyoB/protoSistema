from django.db import models

class Votante(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    OPCIONES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=20, choices=[('Opción1', 'Opción 1'), ('Opción2', 'Opción 2')])
    numero_documento = models.CharField(max_length=20, unique=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    localidad = models.CharField(max_length=10, choices=OPCIONES)  # Para la restricción de localidad
    #def Meta: 
        #db
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.numero_documento})"

#dev meta nombre de la tabla 
#class Candidato(models.Model):

    #OPCIONES = [
        #('A', 'A'),
        #('B', 'B'),
       # ('C', 'C'),
      #  ('D', 'D'),
     #   ('E', 'E'),
    #]

    #nombre = models.CharField(max_length=100)
    #partido = models.CharField(max_length=100)
    #localidad = models.CharField(max_length=10, choices=OPCIONES)  # Debe coincidir con la del votante

    #def __str__(self):
       # return f"{self.nombre} ({self.partido})"


#class Voto(models.Model):
    #votante = models.OneToOneField(Votante, on_delete=models.CASCADE)  # Un votante solo puede votar una vez
    #candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)  # Relación con el candidato
    #fecha = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return f"Votante {self.votante.numero_documento} votó por {self.candidato.nombre}"
