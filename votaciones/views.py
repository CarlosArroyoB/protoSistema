from django.shortcuts import render, redirect
from .forms import VotanteForm
from .models import Votante

def get_name(request):
    if request.method == "POST":
        form = VotanteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos en SQL Server  # Redirige a una página de éxito
    else:
        form = VotanteForm()

    return render(request, "votante.html", {"form": form})
