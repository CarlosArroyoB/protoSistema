from django import forms
from .models import Votante

class VotanteForm(forms.ModelForm):
    class Meta:
        model = Votante
        fields = ['nombre', 'apellidos', 'tipo_documento', 'numero_documento', 'genero', 'localidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Documento'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data.get("numero_documento")
        if not numero_documento.isdigit():
            raise forms.ValidationError("El número de documento solo debe contener números.")
        return numero_documento
