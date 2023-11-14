# app/tables.py
import django_tables2 as tables
from .models import Symptome, Rapport,Rapport_Patient
from authentification.models import Utilisateur

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
    medecin = tables.Column(accessor='medecin_patient.idMedecin.username', verbose_name='Nom du médecin')
    patient = tables.Column(accessor='medecin_patient.idPatient.username', verbose_name='Nom du patient')
    date_rapport = tables.Column(accessor='rapport.date_saisie', verbose_name='Date du rapport')

    # Initialiser la colonne 'action_medecin' ici pour l'ajouter conditionnellement plus tard
    action_medecin = tables.TemplateColumn(
        template_code='<a href="{% url \'accueil\' %}" class="btn btn-primary btn-sm">Détails</a>',
        verbose_name='Action',
        orderable=False,
        empty_values=(),
        attrs={"td": {"class": "text-center"}},
        extra_context={'user_role': 'medecin'},
    )

    def __init__(self, *args, username=None, user_role=None, **kwargs):
        user_role = kwargs.pop('user_role', None)
        super(Rapport_PatientTable, self).__init__(*args, **kwargs)

        # Conditionne l'affichage des colonnes d'action en fonction du rôle de l'utilisateur
        if user_role == 'medecin':
            # Ajoute la colonne d'action si l'utilisateur est un médecin
            self.base_columns['action_medecin'] = self.action_medecin
            self.sequence.append('action_medecin')
        elif user_role == 'patient':
            # Retire la colonne d'action si l'utilisateur est un patient
            self.base_columns.pop('action_medecin', None)
            self.sequence = [column for column in self.sequence if column != 'action_medecin']

    class Meta:
        model = Rapport_Patient
        template_name = "django_tables2/bootstrap.html"
        fields = ('medecin', 'patient', 'date_rapport')  # Ne pas inclure 'action_medecin' ici
