# app/filters.py
import django_filters
from .models import Symptome, Rapport, Rapport_Patient, Utilisateur
from django import forms
from django.db.models.functions import Concat
from django.db.models import CharField, Value 


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
    nom_patient = django_filters.ModelChoiceFilter(
        field_name='medecin_patient__idPatient',
        queryset=Utilisateur.objects.none(),  # Défini à 'none' par défaut, sera remplacé si l'utilisateur est médecin
        label='Nom du patient',
    )
    nom_medecin = django_filters.ModelChoiceFilter(
        field_name='medecin_patient__idMedecin',
        queryset=Utilisateur.objects.none(),  # Défini à 'none' par défaut, sera remplacé si l'utilisateur est patient
        label='Nom du médecin',
    )

    class Meta:
        model = Rapport_Patient
        fields = []

    def __init__(self, *args, username=None, user_role=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_role == 'medecin':
            self.filters['nom_patient'].queryset = Utilisateur.objects.filter(
                role='patient'
            ).annotate(
                nom_complet=Concat(
                    'first_name', Value(' '), 'last_name', output_field=CharField()
                )
            ).order_by('nom_complet')

            del self.filters['nom_medecin']

        elif user_role == 'patient':
            self.filters['nom_medecin'].queryset = Utilisateur.objects.filter(
                role='medecin'
            ).annotate(
                nom_complet=Concat(
                    'first_name', Value(' '), 'last_name', output_field=CharField()
                )
            ).order_by('nom_complet')

            del self.filters['nom_patient']