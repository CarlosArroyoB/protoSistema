
from django.urls import path
from .views import votante_list_api, votante_form_view, candidato_list_api, candidato_form_view, buscar_votante,listar_candidatos,registrar_voto,votar

urlpatterns = [
    path('api/votantes/', votante_list_api, name='votante_api'),  
    path('', votante_form_view, name='votante_form'), 

    path('api/candidatos/',candidato_list_api, name="candidato_api"),
    path('candidatos/',candidato_form_view ,name = "candidato_form") ,

    path('api/buscar-votante/', buscar_votante, name='buscar_votante'),
    path('api/candidatos/<str:localidad>/', listar_candidatos, name='listar_candidatos'),
    path('api/registrar-voto/', registrar_voto, name='registrar_voto'),
    path('votar/',votar,name="votar")    
]