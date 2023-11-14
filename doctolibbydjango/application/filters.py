# app/filters.py
import django_filters
from .models import Symptome, Rapport, Rapport_Patient, Utilisateur
from django import forms
from django.db.models.functions import Concat
from django.db.models import Value 


class VotreModelFilter(django_filters.FilterSet):
    class Meta:
        model = Symptome
        fields = '__all__'#['champ1', 'champ2']''  # Spécifiez les champs que vous souhaitez filtrer.

class SymptomeFilter(django_filters.FilterSet):
    class Meta:
        model = Symptome
        fields = '__all__'

class RapportFilter(django_filters.FilterSet):
    # Exemples de filtres pour des champs de Symptome
    symptome_irritabilite = django_filters.ChoiceFilter(field_name='symptome__irratibilite', choices=Symptome.choises_evaluation)
    symptome_sentiment_depressif = django_filters.ChoiceFilter(field_name='symptome__sentiment_depressif', choices=Symptome.choises_evaluation)
    symptome_bouche_gorge_seche = django_filters.ChoiceFilter(field_name='symptome__bouche_gorge_seche', choices=Symptome.choises_evaluation)
    symptome_actions_gestes_impulsif = django_filters.ChoiceFilter(field_name='symptome__actions_gestes_impulsif', choices=Symptome.choises_evaluation)
    symptome_grincement_dents = django_filters.ChoiceFilter(field_name='symptome__grincement_dents', choices=Symptome.choises_evaluation)
    symptome_difficulte_a_rester_assis = django_filters.ChoiceFilter(field_name='symptome__difficulte_a_rester_assis', choices=Symptome.choises_evaluation)
    symptome_cauchemars = django_filters.ChoiceFilter(field_name='symptome__cauchemars', choices=Symptome.choises_evaluation)
    symptome_diarrhee = django_filters.ChoiceFilter(field_name='symptome__diarrhee', choices=Symptome.choises_evaluation)
    symptome_attaques_verbales_envers_qq1 = django_filters.ChoiceFilter(field_name='symptome__attaques_verbales_envers_qq1', choices=Symptome.choises_evaluation)
    symptome_haut_bas_emotifs = django_filters.ChoiceFilter(field_name='symptome__haut_bas_emotifs', choices=Symptome.choises_evaluation)
    symptome_grande_envie_pleurer = django_filters.ChoiceFilter(field_name='symptome__grande_envie_pleurer', choices=Symptome.choises_evaluation)

    # Exemples de filtres pour des champs de Formulaire
    formulaire_general_poids = django_filters.NumberFilter(field_name='formulaire__general__poids')
    formulaire_alimentation_consommation_alcool = django_filters.BooleanFilter(field_name='formulaire__alimentation__conso_alcool')
    formulaire_alimentation_grignotage_sucre = django_filters.BooleanFilter(field_name='formulaire__alimentation__grignotage_sucre')
    formulaire_alimentation_grignotage_sale = django_filters.BooleanFilter(field_name='formulaire__alimentation__grignotage_sale')

    # ... Autres champs de Formulaire

    class Meta:
        model = Rapport
        fields = []  # Spécifiez des champs si nécessaire, mais avec des filtres personnalisés, cela peut ne pas être nécessaire.

class Rapport_PatientFilter(django_filters.FilterSet):
    # Créer un filtre pour le nom complet du patient
    nom_patient = django_filters.ModelChoiceFilter(
        queryset=Utilisateur.objects.filter(role='patient').annotate(
            nom_complet=Concat('first_name', Value(' '), 'last_name')
        ).order_by('nom_complet'),
        field_name='medecin_patient__idPatient',
        label='Nom du patient',
        to_field_name='id'  # Assurez-vous d'utiliser le bon champ ici
    )
    # Créer un filtre pour le nom complet du médecin
    nom_medecin = django_filters.ModelChoiceFilter(
        queryset=Utilisateur.objects.filter(role='medecin').annotate(
            nom_complet=Concat('first_name', Value(' '), 'last_name')
        ).order_by('nom_complet'),
        field_name='medecin_patient__idMedecin',
        label='Nom du médecin',
        to_field_name='id'  # Assurez-vous d'utiliser le bon champ ici
    )

    # date_min = django_filters.DateFilter(
    #     field_name='rapport__date_saisie',
    #     lookup_expr='gte',
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     label='Date depuis'
    # )
    # date_max = django_filters.DateFilter(
    #     field_name='rapport__date_saisie',
    #     lookup_expr='lte',
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     label='Date jusqu’à'
    # )

    class Meta:
        model = Rapport_Patient
        fields = ['nom_patient', 'nom_medecin']#, 'date_min', 'date_max']