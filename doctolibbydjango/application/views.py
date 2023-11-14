# Importation des modules nécessaires de Django
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from authentification.models import Utilisateur, medecinPatient
from .tables import VotreModelTable, RapportTable, Rapport_PatientTable, Rapport_PatientTable
from .filters import VotreModelFilter, SymptomeFilter, RapportFilter, Rapport_PatientFilter
# Importation des modèles spécifiques à votre application
from .models import (
    Symptome, Form_General, Form_Info_Cardiaque_Tension_Arterielle,
    Form_Prise_Medoc, Form_Alimentation, Form_Activite_Phisique, Form_Autres_Symptomes, Formulaire, Rapport, Rapport_Patient
)
# Importation des formulaires spécifiques à votre application
from .forms import (evaluation_symptomes_form, general_form_form, cardio_form, prise_Medoc_form, Form_Alimentation_form, 
                    Form_Activite_Phisique_form, Form_Autres_Symptomes_form, Form_Infos_Medicales_form
)
from datetime import datetime

@login_required  # Décorateur pour s'assurer que seul un utilisateur connecté puisse accéder à cette vue
def accueil(request):
    prenom = request.user.username  # Récupération du prénom de l'utilisateur
    # Rendu du template avec le contexte
    return render(request,"accueil.html",
                  context={"prenom": prenom})

@login_required  # Décorateur pour s'assurer que seul un utilisateur connecté puisse accéder à cette vue
def comptes(request):
    regexMDP = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-]).{8,}$"  # Expression régulière pour la validation du mot de passe
    message = ""
    if request.method == "POST":  # Si la requête est de type POST
        # Récupération des données du formulaire
        ancienMDP = request.POST["ancienMDP"]
        nouveauMDP1 = request.POST["nouveauMDP1"]
        nouveauMDP2 = request.POST["nouveauMDP2"]
        
        # Vérification de l'authenticité de l'utilisateur
        verification = authenticate(username = request.user.username,
                                    password = ancienMDP)
        if verification != None:
            if nouveauMDP1 == nouveauMDP2:  # Vérification de la correspondance des mots de passe
                utilisateur = Utilisateur.objects.get(username = request.user.username)
                utilisateur.set_password(request.POST.get("nouveauMDP1"))  # Mise à jour du mot de passe
                utilisateur.save()
                return redirect("accueil")  # Redirection vers la page d'accueil
            else:
                message = "⚠️ Les deux mot de passe ne concordent pas ⚠️"
        else:
            message = "L'ancien mot de passe n'est pas bon. T'es qui toi ? 😡"
    # Rendu du template avec le contexte
    return render(request,
                  "comptes.html",
                  {"regexMDP" : regexMDP, "message" : message})

@login_required
def edaia(request):
    # Vérifiez si l'utilisateur est un médecin, sinon redirigez-le vers une URL spécifique
    if request.user.role != "medecin":
        return redirect("https://media.tenor.com/2euSOQYdz8oAAAAj/this-was-technically-illegal-maclen-stanley.gif")
    else:
        # Rendu de la page 'edaia.html' si l'utilisateur est un médecin

        qs = Symptome.objects.all()
        filtered = VotreModelFilter(request.GET, queryset=qs)
        table = VotreModelTable(filtered.qs)
        return render(request, 'edaia.html', {'table': table, 'filter': filtered})

        # return render(request, "edaia.html")
    

# @login_required
# def histo(request):

#     # Obtenez la queryset de Rapport avec les objets liés
#     rapports = Rapport.objects.select_related('symptome', 'formulaire').all()

#     # Appliquez le filtre
#     filtered = RapportFilter(request.GET, queryset=rapports)

#     # Créez la table avec la queryset filtrée
#     table = RapportTable(filtered.qs)

#     return render(request, 'histo.html', {'table': table, 'filter': filtered})


@login_required
def histo(request):
    username = request.user.username
    user_role = request.user.role

    # Commencez avec une queryset de base de Rapport_Patient
    rapports = Rapport_Patient.objects.select_related('medecin_patient', 'rapport')

    # Appliquez le filtre en passant le username et le rôle
    filtered = Rapport_PatientFilter(request.GET, queryset=rapports, username=username, user_role=user_role)

    # Créez la table avec la queryset filtrée en passant aussi le username et le rôle
    table = Rapport_PatientTable(filtered.qs, username=username, user_role=user_role)

    return render(request, 'histo.html', {'table': table, 'filter': filtered})



@login_required
def associationMedecinPatient(request):
    # Étapes pour associer des médecins à des patients
    # 1- Récupération de la liste des médecins et des patients
    medecins = [medecin for medecin in Utilisateur.objects.filter(role="medecin")]
    patients = [patient for patient in Utilisateur.objects.filter(role="patient")]
    
    # 2- Filtrage des patients qui ne sont pas déjà associés à des médecins
    listePatientsAssocies = [ligne.idPatient for ligne in medecinPatient.objects.all()]
    listePatientsNonAssocies = [patient for patient in patients if patient not in listePatientsAssocies]
    
    # 3- Création d'un template avec une liste déroulante pour l'association médecin-patient
    tableAssociationMedecinPatient = medecinPatient.objects.all()
    
    if request.method == "POST":
        # Récupération des données du formulaire pour l'association médecin-patient
        medecin = request.POST["medecin"]
        patient = request.POST["patient"]
        
        # Enregistrement de l'association médecin-patient dans la base de données
        medecinPatient(idMedecin = Utilisateur.objects.filter(username=medecin)[0], 
                       idPatient = Utilisateur.objects.filter(username=patient)[0]).save()
        return redirect("associationMedecinPatient")
    
    return render(request, "associationMedecinPatient.html",
                  {"listePatientsNonAssocies" : listePatientsNonAssocies,
                   "medecins" : medecins,
                   "tableAssociationMedecinPatient" : tableAssociationMedecinPatient})

# Les fonctions suivantes sont structurées de manière à gérer différents formulaires (tunel de formulaires)
#region

# Les fonctions suivantes sont structurées de manière similaire pour gérer différents formulaires
# Chaque fonction gère un formulaire spécifique, enregistre les données du formulaire dans la session si elles sont valides,
# et redirige l'utilisateur vers la page suivante ou précédente en fonction de l'action sélectionnée.
#region

@login_required
def evaluation_symptomes(request):
    if request.method == 'POST':  # Vérification si la requête est de type POST
        personne_data={}  # Initialisation d'un dictionnaire vide pour les données initiales du formulaire
        form = evaluation_symptomes_form(request.POST, initial=personne_data)  # Création d'une instance du formulaire avec les données POST et les données initiales
        if form.is_valid():  # Validation du formulaire
            request.session['evaluation_symptomes'] = form.cleaned_data  # Stockage des données validées dans la session
            action = request.POST.get('action')  # Récupération de l'action souhaitée depuis les données POST
            if action == 'suivant':  # Vérification si l'action est 'suivant'
                return redirect('/form-general/')  # Redirection vers la vue suivante
            elif action == 'precedent':  # Vérification si l'action est 'precedent'
                return redirect('accueil')  # Redirection vers la vue d'accueil
    else:  # Si la requête n'est pas de type POST (i.e., GET)
        personne_data = request.session.get('evaluation_symptomes', {})  # Récupération des données précédemment stockées dans la session, ou un dictionnaire vide si aucune donnée n'est trouvée
        form = evaluation_symptomes_form(initial=personne_data)  # Création d'une instance du formulaire avec les données initiales
    return render(request, 'evaluation_symptomes.html', {'form': form})  # Rendu du formulaire dans le template HTML


@login_required
def form_general_view(request):
    personne_data = request.session.get('evaluation_symptomes', {})
    if request.method == 'POST':
        form = general_form_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['form_general_view'] = form.cleaned_data    
            action = request.POST.get('action')
            if action == 'suivant':
                return redirect('/cardio_')  
            elif action == 'precedent':
                return redirect('evaluation_symptomes') 
    else:
        personne_data = request.session.get('form_general_view', {})
        form = general_form_form(initial=personne_data)
    return render(request, 'form_general.html', {'form': form})

@login_required
def caldio_view(request):
    personne_data = request.session.get('form_general', {})
    if request.method == 'POST':
        form = cardio_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['caldio_view'] = form.cleaned_data
            action = request.POST.get('action')
            if action == 'suivant':
                return redirect('/prs_medoc')
            elif action == 'precedent':
                return redirect('form-general/')
    else:
        personne_data = request.session.get('caldio_view', {})
        form = cardio_form(initial=personne_data)
    return render(request, 'cardio.html', {'form': form})

@login_required
def prise_Medoc_view(request):
    personne_data = request.session.get('cardio', {})
    if request.method == 'POST':
        form = prise_Medoc_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['prise_Medoc_view'] = form.cleaned_data    
            action = request.POST.get('action')
            if action == 'suivant':
                return redirect('alimentation') 
            elif action == 'precedent':
                return redirect('cardio')
    else:
        personne_data = request.session.get('prise_Medoc_view', {})
        form = prise_Medoc_form(initial=personne_data)
    return render(request, 'prs_medoc.html', {'form': form})

@login_required
def alimentation_view(request):
    personne_data = request.session.get('prs_medoc', {})
    if request.method == 'POST':
        form = Form_Alimentation_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['alimentation_view'] = form.cleaned_data         
            action = request.POST.get('action')
            if action == 'suivant':
                return redirect('activite_physique')
            elif action == 'precedent':
                return redirect('prise_medoc')
    else:
        personne_data = request.session.get('alimentation_view', {})
        form = Form_Alimentation_form(initial=personne_data)
    return render(request, 'alimentation.html', {'form': form})

@login_required
def activite_physique_view(request):
    personne_data = request.session.get('alimentation', {})
    if request.method == 'POST':
        form = Form_Activite_Phisique_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['activite_physique_view'] = form.cleaned_data
            action = request.POST.get('action')
            if action == 'suivant':
                return redirect('autres_symptomes')
            elif action == 'precedent':
                return redirect('alimentation')
            
    else:
        personne_data = request.session.get('activite_physique_view', {})
        form = Form_Activite_Phisique_form(initial=personne_data)
    return render(request, 'activite_physique.html', {'form': form})

#endregion

@login_required
def autres_symptomes_view(request):
    # Récupération des données précédemment sauvegardées dans la session, si elles existent
    personne_data = request.session.get('activite_physique', {})
    
    # Vérification si la requête est une requête POST
    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données POST et les données initiales récupérées de la session
        form = Form_Autres_Symptomes_form(request.POST, initial=personne_data)
        
        # Vérification de la validité du formulaire
        if form.is_valid():
            # Récupération de l'action souhaitée (suivant ou précédent) depuis les données POST
            action = request.POST.get('action')
            
            # Traitement en fonction de l'action souhaitée
            if action == 'suivant':
                # Conversion des données POST en dictionnaire, en excluant le premier élément et l'élément 'action'
                converted_dict = {key: value for key, value in request.POST.items()}
                converted_dict = dict(list(converted_dict.items())[1:])
                del converted_dict['action']
                # Sauvegarde du dictionnaire converti dans la session
                request.session['autres_symptomes_view'] = converted_dict
                # Redirection vers la vue suivante
                return redirect('info_medicales') 
            elif action == 'precedent':
                # Redirection vers la vue précédente
                return redirect('activite_physique')
    else:
        personne_data = request.session.get('autres_symptomes_view', {})
        # Création d'une instance du formulaire avec les données initiales récupérées de la session (pour une requête GET)
        form = Form_Autres_Symptomes_form(initial=personne_data)
    
    # Rendu du template avec le formulaire
    return render(request, 'autres_symptomes.html', {'form': form})

@login_required
def info_medicales_view(request):
    # Récupération des données précédemment sauvegardées dans la session, si elles existent
    personne_data = request.session.get('autres_symptomes', {})
    
    # Vérification si la requête est une requête POST
    if request.method == 'POST':
        # Création d'une instance du formulaire avec les données POST et les données initiales récupérées de la session
        form = Form_Infos_Medicales_form(request.POST, initial=personne_data)
        
        # Vérification de la validité du formulaire
        if form.is_valid():
            # Récupération de l'action souhaitée (suivant ou précédent) depuis les données POST
            action = request.POST.get('action')
            
            # Traitement en fonction de l'action souhaitée
            if action == 'suivant':
                # Appel des fonctions save_formulaire et save_formulaire_atres_symptomes pour sauvegarder les données des formulaires dans la base de données
                symtomes = save_formulaire(request, Symptome, 'evaluation_symptomes')
                general = save_formulaire(request, Form_General, 'form_general_view')
                cardio = save_formulaire(request, Form_Info_Cardiaque_Tension_Arterielle,'caldio_view')
                medoc = save_formulaire(request, Form_Prise_Medoc,'prise_Medoc_view')
                alimentation = save_formulaire(request, Form_Alimentation,'alimentation_view')
                physique = save_formulaire(request, Form_Activite_Phisique,'activite_physique_view')
                autres_symptomes = save_formulaire_atres_symptomes(request)
                # Sauvegarde des données du formulaire actuel dans la base de données
                info_medic = form.save()
                
                # Appel de la fonction save_hub_formulaire pour créer une instance du modèle Formulaire et la sauvegarder dans la base de données
                formulaire = save_hub_formulaire(general, cardio, medoc, alimentation, physique, autres_symptomes, info_medic)
                
                # Appel de la fonction save_rapport pour créer une instance du modèle Rapport et la sauvegarder dans la base de données
                rapport = save_rapport(formulaire, symtomes, datetime.now())
                
                # Récupération de l'association médecin-patient correspondante
                association = medecinPatient.objects.get(idMedecin_id = Utilisateur.objects.get(username = "No"), 
                                                        idPatient_id =  Utilisateur.objects.get(username = request.user.username))
                
                # Appel de la fonction save_patient_rapport pour créer une instance du modèle Patient et la sauvegarder dans la base de données
                save_patient_rapport(rapport, association)

                # Efface toutes les données de la session
                for key in ['evaluation_symptomes', 'form_general_view', 'caldio_view']:
                    request.session.pop(key, None)
                
                # Redirection vers la vue accueil
                return redirect('accueil')
            
            elif action == 'precedent':
                # Redirection vers la vue précédente
                return redirect('autres_symptomes')
    else:
        # Création d'une instance du formulaire avec les données initiales récupérées de la session (pour une requête GET)
        form = Form_Infos_Medicales_form(initial=personne_data)
    
    # Rendu du template avec le formulaire
    return render(request, 'info_medicales.html', {'form': form})

#endregion

# Sauvegarde des données vers la base de données
#region
def save_patient_rapport(rapport, medecin_patient):
    # Création d'une nouvelle instance de la classe Patient
    instance1 = Rapport_Patient()

    # Assignation des arguments rapport et medecin_patient aux attributs correspondants de l'instance
    instance1.medecin_patient = medecin_patient
    instance1.rapport = rapport

    # Sauvegarde de l'instance dans la base de données
    instance1.save()

    # Retour de l'instance créée
    return instance1

def save_rapport(formulaire, symptome, date=datetime.now()):
    # Création d'une nouvelle instance de la classe Rapport
    instance1 = Rapport()

    # Assignation des arguments formulaire, symptome et date aux attributs correspondants de l'instance
    instance1.formulaire = formulaire
    instance1.symptome = symptome
    instance1.date_saisie = date

    # Sauvegarde de l'instance dans la base de données
    instance1.save()

    # Retour de l'instance créée
    return instance1

def save_hub_formulaire(general, cardio, medoc, alimentation, physique, autres_symptomes, info_medic):
    # Création d'une nouvelle instance de la classe Formulaire
    instance1 = Formulaire()

    # Assignation des arguments aux attributs correspondants de l'instance
    instance1.general = general
    instance1.info_cardiaque = cardio
    instance1.prise_medoc = medoc
    instance1.alimentation = alimentation
    instance1.activite_phisique = physique
    instance1.autres_symptomes = autres_symptomes
    instance1.infos_medicales = info_medic

    # Sauvegarde de l'instance dans la base de données
    instance1.save()

    # Retour de l'instance créée
    return instance1

def save_formulaire(request, instance, name):
    # Récupération des données du formulaire précédent à partir de la session
    form1_data = request.session.get(name)

    # Création d'une nouvelle instance du modèle spécifié avec les données récupérées
    instance1 = instance(**form1_data)

    # Sauvegarde de l'instance dans la base de données
    instance1.save()

    # Suppression des données du formulaire de la session pour nettoyer
    del request.session[name]

    # Retour de l'instance créée
    return instance1

def save_formulaire_atres_symptomes(request):
    from datetime import time, timedelta
    
    # Récupération des données du formulaire précédent à partir de la session
    form1_data = request.session.get('autres_symptomes_view')

    # Création d'une nouvelle instance du modèle Form_Autres_Symptomes avec les données récupérées
    instance1 = Form_Autres_Symptomes(**form1_data)
    
    # Conversion des chaînes de caractères en objets time et timedelta pour les champs de temps spécifiés
    instance1.heure_debut_palpitations = time(
        int(request.session.get('autres_symptomes_view')['heure_debut_palpitations'].split(':')[0]),
        int(request.session.get('autres_symptomes_view')['heure_debut_palpitations'].split(':')[1]),
        0)
    
    instance1.duree_total_palpitations = timedelta(
        days=0, minutes=int(request.session.get('autres_symptomes_view')['duree_total_palpitations']))

    instance1.heure_debut_douleurs_thoracique = time(
        int(request.session.get('autres_symptomes_view')['heure_debut_douleurs_thoracique'].split(':')[0]),
        int(request.session.get('autres_symptomes_view')['heure_debut_douleurs_thoracique'].split(':')[1]),
        0)

    instance1.duree_total_douleurs_thoracique = timedelta(
        days=0, minutes=int(request.session.get('autres_symptomes_view')['duree_total_douleurs_thoracique']))

    instance1.heure_debut_malaises = time(
        int(request.session.get('autres_symptomes_view')['heure_debut_malaises'].split(':')[0]),
        int(request.session.get('autres_symptomes_view')['heure_debut_malaises'].split(':')[1]),
        0)

    instance1.duree_total_malaises = timedelta(
        days=0, minutes=int(request.session.get('autres_symptomes_view')['duree_total_malaises']))

    # Sauvegarde de l'instance dans la base de données
    instance1.save()

    # Suppression des données du formulaire de la session pour nettoyer
    del request.session['autres_symptomes_view']

    # Retour de l'instance créée
    return instance1

#endregion
