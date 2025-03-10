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
    tipo_documento = models.CharField(max_length=20, choices=[("CC", "Cédula de ciudadanía"), ("CE", "Cédula de extranjería")])
    numero_documento = models.CharField(max_length=20, unique=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    localidad = models.CharField(max_length=10, choices=OPCIONES)  #
        #db
    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.numero_documento})"

#dev meta nombre de la tabla 
class Candidato(models.Model):

    OPCIONES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]

    nombre = models.CharField(max_length=100)
    partido = models.CharField(max_length=100)
    localidad = models.CharField(max_length=10, choices=OPCIONES) 
    def __str__(self):
        return f"{self.nombre} ({self.partido})"


class Voto(models.Model):
    votante = models.ForeignKey(Votante, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)

    dni_votante = models.CharField(max_length=8, default="00000000")  

    def save(self, *args, **kwargs):
        self.dni_votante = self.votante.numero_documento  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.votante.nombre} votó por {self.candidato.nombre} (DNI: {self.dni_votante})"