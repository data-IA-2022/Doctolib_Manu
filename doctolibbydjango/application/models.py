from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from authentification.models import Utilisateur
# import datetime

# Create your models here.
# La classe Person représente une personne avec un nom.
class Person(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

# La classe Group représente un groupe avec un nom et une liste de membres.
class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through="Membership")

    def __str__(self):
        return self.name

# La classe Membership représente l'appartenance d'une personne à un groupe
# avec la date à laquelle elle a rejoint le groupe et une raison d'invitation.
class Membership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
    test = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)  # Note : Utilisateur doit être défini ailleurs dans le code.

# La classe Medecin représente un médecin avec une référence à un utilisateur.
class Medecin(models.Model): 
    user_id = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)  # Note : Utilisateur doit être défini ailleurs dans le code.

# La classe Symptome représente un symptôme avec une description et une valeur.
class Symptome(models.Model):
    
    choises_evaluation = [(0, 'Ce symptôme n’est pas apparu au cours des deux dernières semaines'),
                                        (1, 'Ce symptôme est apparu une ou deux fois seulement au cours des deux dernières semaines'),
                                        (5, 'Ce symptôme est apparu plusieurs fois au cours des deux dernières semaines'),
                                        (10, 'Ce symptôme est apparu presque continuellement au cours des deux dernières semaines')]
    
    irratibilite = models.IntegerField(choices=choises_evaluation, default = 0) 
    sentiment_depressif = models.IntegerField(choices=choises_evaluation, default = 0)
    bouche_gorge_seche = models.IntegerField(choices=choises_evaluation, default = 0)
    actions_gestes_impulsif = models.IntegerField(choices=choises_evaluation, default = 0)
    grincement_dents = models.IntegerField(choices=choises_evaluation, default = 0)
    difficulte_a_rester_assis = models.IntegerField(choices=choises_evaluation, default = 0)
    cauchemars = models.IntegerField(choices=choises_evaluation, default = 0)
    diarrhee = models.IntegerField(choices=choises_evaluation, default = 0)
    attaques_verbales_envers_qq1 = models.IntegerField(choices=choises_evaluation, default = 0)
    haut_bas_emotifs = models.IntegerField(choices=choises_evaluation, default = 0)
    grande_envie_pleurer = models.IntegerField(choices=choises_evaluation, default = 0)
    

# Cette classe représente le modèle pour les données générales du formulaire.
class Form_General(models.Model):
    poids = models.FloatField( default=70.0,  validators=[MinValueValidator(20.0), MaxValueValidator(300.0)])
    tour_2_taille = models.FloatField( default=80.0,  validators=[MinValueValidator(40.0), MaxValueValidator(300.0)])

class Form_Info_Cardiaque_Tension_Arterielle(models.Model):
    frquence_cardiaque = models.FloatField( default=60.0,  validators=[MinValueValidator(20.0), MaxValueValidator(120.0)])
    tension_systolique_matin = models.FloatField( default=120.0,  validators=[MinValueValidator(100.0), MaxValueValidator(250.0)])
    tension_systolique_soir = models.FloatField( default=120.0,  validators=[MinValueValidator(100.0), MaxValueValidator(250.0)])
    tension_diastolique_matin = models.FloatField( default=60.0,  validators=[MinValueValidator(40.0), MaxValueValidator(100.0)])
    tension_diastolique_soir = models.FloatField( default=60.0,  validators=[MinValueValidator(40.0), MaxValueValidator(100.0)])
    description = models.CharField(blank=True, null=True, default = '', max_length=500)

# Cette classe représente le modèle pour les données concernant la prise de médicaments du formulaire.
class Form_Prise_Medoc(models.Model):
    nombre_medoc_pris_jr = models.IntegerField( default=0)
    oublie_prise_medoc_matin = models.BooleanField( default="False")
    oublie_prise_medoc_soir = models.BooleanField( default="False")
    effet_secondaires_remarques = models.BooleanField( default="False")
    symptomes_particuliers_remarques = models.BooleanField( default="False")
    description = models.CharField(default = None, max_length=500)

# Cette classe représente le modèle pour les données concernant l'alimentation du formulaire.
class Form_Alimentation(models.Model):
    conso_alcool =  models.BooleanField( default="False")
    grignotage_sucre = models.BooleanField( default="False")
    grignotage_sale = models.BooleanField( default="False")
    nombre_repas_durant_jr = models.IntegerField( default=2)
    quantite_eau_bu = models.FloatField( default=0.0,  validators=[MinValueValidator(0.0)])
    quantite_alcool_bu = models.FloatField( default=0.0,  validators=[MinValueValidator(0.0)])

# Cette classe représente le modèle pour les données concernant l'activité physique du formulaire.
class Form_Activite_Phisique(models.Model):
    a_eu_activite_physique =  models.BooleanField( default="False")
    duree_activite_physique = models.DurationField()
    description = models.CharField(default = None, max_length=500)

# Cette classe représente le modèle pour les données concernant d'autres symptômes du formulaire.
class Form_Autres_Symptomes(models.Model):
    presence_dyspnee =  models.BooleanField( default="False")
    presence_oedeme = models.BooleanField( default="False")
    presence_episode_intectieux = models.BooleanField( default="False")
    presence_fievre =  models.BooleanField( default="False")
    presence_palpitation = models.BooleanField( default="False")
    presence_douleur_thoracique = models.BooleanField( default="False")
    presence_malaise =  models.BooleanField( default="False")
   
    heure_debut_palpitations = models.TimeField( default=None)
    duree_total_palpitations = models.DurationField( default=None)

    heure_debut_douleurs_thoracique = models.TimeField( default=None)
    duree_total_douleurs_thoracique = models.DurationField(default=None)

    heure_debut_malaises = models.TimeField( default=None)
    duree_total_malaises = models.DurationField(default=None)

# Cette classe représente le modèle pour les informations médicales du formulaire.
class Form_Infos_Medicales(models.Model):
    valeur_natremie = models.FloatField( default= 140.0,  validators=[MinValueValidator(0.0)])
    valeur_potatium = models.FloatField( default= 4.0,  validators=[MinValueValidator(0.0)])
    valeur_creatinine = models.FloatField( default= 90.0,  validators=[MinValueValidator(0.0)])
    valeur_clairance_creatinine = models.FloatField( default=90.0,  validators=[MinValueValidator(0.0)])
    taux_nt_probnp = models.FloatField( default=100.0,  validators=[MinValueValidator(0.0)]) 
    taux_fer_serique = models.FloatField( default=60.0,  validators=[MinValueValidator(0.0)])
    taux_hemoglobine = models.FloatField( default=14.0,  validators=[MinValueValidator(0.0)])
    valeur_vitesse_sedimentation = models.FloatField( default=15.0,  validators=[MinValueValidator(0.0)])
    taux_proteine_c = models.FloatField( default=100.0,  validators=[MinValueValidator(0.0)])
    taux_troponine = models.FloatField( default=20.0,  validators=[MinValueValidator(0.0)])
    taux_vitamine_d = models.FloatField( default=60.0,  validators=[MinValueValidator(0.0)])
    taux_acide_urique = models.FloatField( default=5.0,  validators=[MinValueValidator(0.0)])
    taux_inr = models.FloatField( default=2.5,  validators=[MinValueValidator(0.0)])
   
# Cette classe représente le modèle principal du formulaire, qui relie les autres modèles par des clés étrangères.
class Formulaire(models.Model):
    general = models.ForeignKey(Form_General, on_delete=models.CASCADE, default=None)
    info_cardiaque = models.ForeignKey(Form_Info_Cardiaque_Tension_Arterielle, on_delete=models.CASCADE, default=None)
    prise_medoc = models.ForeignKey(Form_Prise_Medoc, on_delete=models.CASCADE, default=None)
    alimentation = models.ForeignKey(Form_Alimentation, on_delete=models.CASCADE, default=None)
    activite_phisique = models.ForeignKey(Form_Activite_Phisique, on_delete=models.CASCADE, default=None)
    autres_symptomes = models.ForeignKey(Form_Autres_Symptomes, on_delete=models.CASCADE, default=None)
    infos_medicales = models.ForeignKey(Form_Infos_Medicales, on_delete=models.CASCADE, default=None)


# La classe Rapport représente un rapport avec une référence à un symptôme et un formulaire.
class Rapport(models.Model):
    symptome = models.ForeignKey(Symptome, on_delete=models.CASCADE)
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE)
    date_saisie = models.DateTimeField(null=True)

# La classe Patient représente un patient avec une référence à un utilisateur,
# un rapport par défaut, et une liste de médecins associés.
class Patient(models.Model): 
    user_id = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)  # Note : Utilisateur doit être défini ailleurs dans le code.
    rapport = models.ForeignKey(Rapport, on_delete=models.CASCADE, default=None)
    medicin = models.ManyToManyField(Medecin)