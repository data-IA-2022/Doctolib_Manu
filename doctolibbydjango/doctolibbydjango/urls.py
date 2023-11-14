"""doctolibbydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from application.views import accueil, comptes, edaia, associationMedecinPatient, evaluation_symptomes, form_general_view ,info_medicales_view,caldio_view, prise_Medoc_view, alimentation_view, activite_physique_view, autres_symptomes_view, histo
from authentification.views import connexion, deconnexion, inscription 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accueil/", accueil, name="accueil"),
    path("", connexion, name="connexion"),
    path("comptes", comptes, name="comptes"),
    path("edaia", edaia, name="edaia"),
    path("histo", histo, name="histo"),
    path("associationMedecinPatient", associationMedecinPatient, name="associationMedecinPatient"),
    path("deconnexion", deconnexion, name="deconnexion"),
    path("inscription", inscription, name="inscription"),
    path("evaluation/", evaluation_symptomes, name="evaluation_symptomes"),
    path('form-general/', form_general_view, name='form_general'),
    path('prs_medoc', prise_Medoc_view, name='prise_medoc'),
    path('cardio_', caldio_view, name='cardio'),
    path('alimentation', alimentation_view, name='alimentation'),
    path('activite_physique', activite_physique_view, name='activite_physique'),
    path('autres_symptomes', autres_symptomes_view, name='autres_symptomes'),
    path('info_medicales', info_medicales_view, name='info_medicales'),
] 
