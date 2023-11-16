from django.test import TestCase
from django.utils import timezone
from .models import Rapport, Symptome, Formulaire, Form_General, Form_Info_Cardiaque_Tension_Arterielle, Form_Prise_Medoc, Form_Alimentation, Form_Activite_Phisique, Form_Autres_Symptomes, Form_Infos_Medicales
from datetime import datetime, time, timedelta

class SymptomeModelTests(TestCase):
    
    def test_creation_symptome_defaults(self):
        symptome = Symptome.objects.create()
        self.assertEqual(symptome.irratibilite, 0)
        self.assertEqual(symptome.sentiment_depressif, 0)
        self.assertEqual(symptome.bouche_gorge_seche, 0)

    def test_creation_symptome_with_values(self):
        symptome = Symptome.objects.create(
            irratibilite=5,
            sentiment_depressif=10,
            bouche_gorge_seche=1,
        )
        self.assertEqual(symptome.irratibilite, 5)
        self.assertEqual(symptome.sentiment_depressif, 10)
        self.assertEqual(symptome.bouche_gorge_seche, 1)

    def test_update_symptome(self):
        symptome = Symptome.objects.create(irratibilite=5)
        symptome.irratibilite = 10
        symptome.save()
        updated_symptome = Symptome.objects.get(id=symptome.id)
        self.assertEqual(updated_symptome.irratibilite, 10)


    def setUp(self):
        # Création des instances nécessaires pour les clés étrangères
        symptome = Symptome.objects.create(irratibilite=0, sentiment_depressif=1)
        general = Form_General.objects.create(poids=70.0, tour_2_taille=80.0)
        info_cardiaque = Form_Info_Cardiaque_Tension_Arterielle.objects.create(frquence_cardiaque=60.0)
        prise_medoc = Form_Prise_Medoc.objects.create()
        alimentation = Form_Alimentation.objects.create()
        activite_phisique = Form_Activite_Phisique.objects.create()
        autres_symptomes = Form_Autres_Symptomes.objects.create(
            presence_dyspnee=False,
            presence_oedeme=False,
            presence_episode_intectieux=False,
            presence_fievre=False,
            presence_palpitation=False,
            presence_douleur_thoracique=False,
            presence_malaise=False,
            heure_debut_palpitations=time(0, 0),
            duree_total_palpitations=timedelta(minutes=0),
            heure_debut_douleurs_thoracique=time(0, 0),
            duree_total_douleurs_thoracique=timedelta(minutes=0),
            heure_debut_malaises=time(0, 0),
            duree_total_malaises=timedelta(minutes=0)
        )
        infos_medicales = Form_Infos_Medicales.objects.create()

        formulaire = Formulaire.objects.create(
            general=general,
            info_cardiaque=info_cardiaque,
            prise_medoc=prise_medoc,
            alimentation=alimentation,
            activite_phisique=activite_phisique,
            autres_symptomes=autres_symptomes,
            infos_medicales=infos_medicales
        )

        self.rapport = Rapport.objects.create(symptome=symptome, formulaire=formulaire, date_saisie=timezone.now())

    def test_rapport_creation(self):
        self.assertEqual(Rapport.objects.count(), 1)
        self.assertIsNotNone(self.rapport.date_saisie)

    def test_rapport_fields(self):
        rapport = Rapport.objects.get(id=self.rapport.id)
        self.assertEqual(rapport.symptome.irratibilite, 0)
        self.assertEqual(rapport.formulaire.general.poids, 70.0)
