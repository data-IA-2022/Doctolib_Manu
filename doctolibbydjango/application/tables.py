# app/tables.py
import django_tables2 as tables
from .models import Symptome, Rapport

class VotreModelTable(tables.Table):
    class Meta:
        model = Symptome
        template_name = 'django_tables2/bootstrap.html'  # si vous utilisez Bootstrap

class RapportTable(tables.Table):
    symptome_irritabilite = tables.Column(accessor='symptome.irratibilite', verbose_name='Irritabilité')
    symptome_sentiment_depressif = tables.Column(accessor='symptome.sentiment_depressif', verbose_name='Sentiment dépressif')
    symptome_bouche_gorge_seche = tables.Column(accessor='symptome.bouche_gorge_seche', verbose_name='Bouche/gorge sèche')
    symptome_actions_gestes_impulsif = tables.Column(accessor='symptome.actions_gestes_impulsif', verbose_name='Actions/gestes impulsifs')
    symptome_grincement_dents = tables.Column(accessor='symptome.grincement_dents', verbose_name='Grincement de dents')
    symptome_difficulte_a_rester_assis = tables.Column(accessor='symptome.difficulte_a_rester_assis', verbose_name='Difficulté à rester assis')
    symptome_cauchemars = tables.Column(accessor='symptome.cauchemars', verbose_name='Cauchemars')
    symptome_diarrhee = tables.Column(accessor='symptome.diarrhee', verbose_name='Diarrhée')
    symptome_attaques_verbales_envers_qq1 = tables.Column(accessor='symptome.attaques_verbales_envers_qq1', verbose_name='Attaques verbales envers quelqu’un')
    symptome_haut_bas_emotifs = tables.Column(accessor='symptome.haut_bas_emotifs', verbose_name='Hauts et bas émotifs')
    symptome_grande_envie_pleurer = tables.Column(accessor='symptome.grande_envie_pleurer', verbose_name='Grande envie de pleurer')
    formulaire_general_poids = tables.Column(accessor='formulaire.general.poids', verbose_name='Poids général')
    formulaire_alimentation_consommation_alcool = tables.BooleanColumn(accessor='formulaire.alimentation.conso_alcool', verbose_name='Consommation d’alcool', yesno='Oui,Non')
    formulaire_alimentation_grignotage_sucre = tables.BooleanColumn(accessor='formulaire.alimentation.grignotage_sucre', verbose_name='Grignotage sucre', yesno='Oui,Non')
    formulaire_alimentation_grignotage_sale = tables.BooleanColumn(accessor='formulaire.alimentation.grignotage_sale', verbose_name='Grignotage sale', yesno='Oui,Non')

    class Meta:
        model = Rapport
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'symptome_irritabilite', 'symptome_sentiment_depressif', 
            'symptome_bouche_gorge_seche', 'symptome_actions_gestes_impulsif',
            'symptome_grincement_dents', 'symptome_difficulte_a_rester_assis',
            'symptome_cauchemars', 'symptome_diarrhee',
            'symptome_attaques_verbales_envers_qq1', 'symptome_haut_bas_emotifs',
            'symptome_grande_envie_pleurer', 'formulaire_general_poids', 
            'formulaire_alimentation_consommation_alcool',
        )

class Rapport_PatientTable(tables.Table):
    symptome_irritabilite = tables.Column(accessor='rapport.symptome.irratibilite', verbose_name='Irritabilité')
    symptome_sentiment_depressif = tables.Column(accessor='symptome.sentiment_depressif', verbose_name='Sentiment dépressif')
    symptome_bouche_gorge_seche = tables.Column(accessor='symptome.bouche_gorge_seche', verbose_name='Bouche/gorge sèche')
    symptome_actions_gestes_impulsif = tables.Column(accessor='symptome.actions_gestes_impulsif', verbose_name='Actions/gestes impulsifs')
    symptome_grincement_dents = tables.Column(accessor='symptome.grincement_dents', verbose_name='Grincement de dents')
    symptome_difficulte_a_rester_assis = tables.Column(accessor='symptome.difficulte_a_rester_assis', verbose_name='Difficulté à rester assis')
    symptome_cauchemars = tables.Column(accessor='symptome.cauchemars', verbose_name='Cauchemars')
    symptome_diarrhee = tables.Column(accessor='symptome.diarrhee', verbose_name='Diarrhée')
    symptome_attaques_verbales_envers_qq1 = tables.Column(accessor='symptome.attaques_verbales_envers_qq1', verbose_name='Attaques verbales envers quelqu’un')
    symptome_haut_bas_emotifs = tables.Column(accessor='symptome.haut_bas_emotifs', verbose_name='Hauts et bas émotifs')
    symptome_grande_envie_pleurer = tables.Column(accessor='symptome.grande_envie_pleurer', verbose_name='Grande envie de pleurer')
    formulaire_general_poids = tables.Column(accessor='formulaire.general.poids', verbose_name='Poids général')
    formulaire_alimentation_consommation_alcool = tables.BooleanColumn(accessor='formulaire.alimentation.conso_alcool', verbose_name='Consommation d’alcool', yesno='Oui,Non')
    formulaire_alimentation_grignotage_sucre = tables.BooleanColumn(accessor='formulaire.alimentation.grignotage_sucre', verbose_name='Grignotage sucre', yesno='Oui,Non')
    formulaire_alimentation_grignotage_sale = tables.BooleanColumn(accessor='formulaire.alimentation.grignotage_sale', verbose_name='Grignotage sale', yesno='Oui,Non')

    class Meta:
        model = Rapport
        template_name = "django_tables2/bootstrap.html"
        fields = (
            'symptome_irritabilite', 'symptome_sentiment_depressif', 
            'symptome_bouche_gorge_seche', 'symptome_actions_gestes_impulsif',
            'symptome_grincement_dents', 'symptome_difficulte_a_rester_assis',
            'symptome_cauchemars', 'symptome_diarrhee',
            'symptome_attaques_verbales_envers_qq1', 'symptome_haut_bas_emotifs',
            'symptome_grande_envie_pleurer', 'formulaire_general_poids', 
            'formulaire_alimentation_consommation_alcool',
        )
