# app/filters.py
import django_filters
from .models import Symptome, Rapport

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