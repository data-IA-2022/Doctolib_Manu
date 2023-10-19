from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from authentification.models import Utilisateur, medecinPatient
from application.models import Symptome, Form_General
from .forms import evaluation_symptomes_form, general_form_form, cardio_form, prise_Medoc_form, Form_Alimentation_form, Form_Activite_Phisique_form

@login_required
def accueil(request):
    prenom = request.user.username
    return render(request,"accueil.html",
                  context={"prenom": prenom})


@login_required
def comptes(request):
    regexMDP = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-]).{8,}$"
    message = ""
    if request.method == "POST":
        ancienMDP = request.POST["ancienMDP"]
        nouveauMDP1 = request.POST["nouveauMDP1"]
        nouveauMDP2 = request.POST["nouveauMDP2"]
        
        verification = authenticate(username = request.user.username,
                                    password = ancienMDP)
        if verification != None:
            if nouveauMDP1 == nouveauMDP2:
                utilisateur = Utilisateur.objects.get(username = request.user.username)
                #utilisateur = Utilisateur.objects.get(id=request.user.id)
                utilisateur.set_password(request.POST.get("nouveauMDP1"))
                utilisateur.save()
                return redirect("accueil")
            else:
                message = "⚠️ Les deux mot de passe ne concordent pas ⚠️"
        else:
            message = "L'ancien mot de passe n'est pas bon. T'es qui toi ? 😡"
    return render(request,
                  "comptes.html",
                  {"regexMDP" : regexMDP, "message" : message})

@login_required
def edaia(request):
    if request.user.role != "medecin":
        return redirect("https://media.tenor.com/2euSOQYdz8oAAAAj/this-was-technically-illegal-maclen-stanley.gif")
    else:
        return render(request, "edaia.html")

@login_required
def associationMedecinPatient(request):
    # 1- Récupérer la liste des id des médecins et des patients
    # 2- Ensuite on ne garde que les patients qui ne sont pas dans la table medecinPatient
    # 3- On créé ensuite un template qui contiendra une liste déroulante
    # 4- Dans cette liste déroulante on va afficher d'un côté les médecins
    # et de l'autre les patients filtrés (voir étapge 2)
    # https://developer.mozilla.org/fr/docs/Web/HTML/Element/select
    
    medecins = [medecin for medecin in Utilisateur.objects.filter(role="medecin")]
    patients = [patient for patient in Utilisateur.objects.filter(role="patient")]
    listePatientsAssocies = [ligne.idPatient for ligne in medecinPatient.objects.all()]
    print("listePatientsAssocies :", listePatientsAssocies)
    listePatientsNonAssocies = [patient for patient in patients if patient not in listePatientsAssocies]
    tableAssociationMedecinPatient = medecinPatient.objects.all()
    
    if request.method == "POST":
        medecin = request.POST["medecin"]
        patient = request.POST["patient"]
        print("medecin", type(medecin), medecin)
        medecinPatient(idMedecin = Utilisateur.objects.filter(username=medecin)[0], 
                       idPatient = Utilisateur.objects.filter(username=patient)[0]).save()
        return redirect("associationMedecinPatient")
    return render(request, "associationMedecinPatient.html",
                  {"listePatientsNonAssocies" : listePatientsNonAssocies,
                   "medecins" : medecins,
                   "tableAssociationMedecinPatient" : tableAssociationMedecinPatient})

@login_required
def evaluation_symptomes(request):

    if request.method == 'POST':
        form = evaluation_symptomes_form(request.POST)
        if form.is_valid():
            # Ici, plutôt que de sauvegarder directement, nous pourrions stocker les données dans la session.
            request.session['personne_data'] = {'symptomes': form.cleaned_data}
            return redirect('/form-general/')
    else:
        form = evaluation_symptomes_form()
    return render(request, 'evaluation_symptomes.html', {'form': form})

def form_general_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = general_form_form(request.POST, initial=personne_data)
        if form.is_valid():

             # Fusionnez les deux dictionnaires
            merged_data = {**personne_data, **{'general': form.cleaned_data}}

             # Si vous souhaitez mettre à jour les données de la session avec les nouvelles données
            request.session['personne_data'] = merged_data

            # Sauvegarder les données dans la base de données
            # form.save()
            return redirect('/cardio_')  # changez 'success_url' par votre URL de réussite.
    else:
        form = general_form_form(initial=personne_data)
    return render(request, 'form_general.html', {'form': form})

def caldio_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = cardio_form(request.POST, initial=personne_data)
        if form.is_valid():

             # Fusionnez les deux dictionnaires
            merged_data = {**personne_data, **{'cardio': form.cleaned_data}}

             # Si vous souhaitez mettre à jour les données de la session avec les nouvelles données
            request.session['personne_data'] = merged_data
            
            # Sauvegarder les données dans la base de données
            # form.save()
            return redirect('/prs_medoc')  # changez 'success_url' par votre URL de réussite.
    else:
        form = cardio_form(initial=personne_data)
    return render(request, 'cardio.html', {'form': form})

def prise_Medoc_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = prise_Medoc_form(request.POST, initial=personne_data)
        if form.is_valid():

             # Fusionnez les deux dictionnaires
            merged_data = {**personne_data, **{'prise_medoc': form.cleaned_data}}

             # Si vous souhaitez mettre à jour les données de la session avec les nouvelles données
            request.session['personne_data'] = merged_data

            print("reponce ", merged_data)
            
            # Sauvegarder les données dans la base de données
            # form.save()
            return redirect('alimentation')  # changez 'success_url' par votre URL de réussite.
    else:
        form = prise_Medoc_form(initial=personne_data)
    return render(request, 'prs_medoc.html', {'form': form})

def alimentation_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = Form_Alimentation_form(request.POST, initial=personne_data)
        if form.is_valid():

             # Fusionnez les deux dictionnaires
            merged_data = {**personne_data, **{'alimentation': form.cleaned_data}}

             # Si vous souhaitez mettre à jour les données de la session avec les nouvelles données
            request.session['personne_data'] = merged_data

            print("reponce ", merged_data)
            
            # Sauvegarder les données dans la base de données
            # form.save()
            return redirect('activite_physique')  # changez 'success_url' par votre URL de réussite.
    else:
        form = Form_Alimentation_form(initial=personne_data)
    return render(request, 'alimentation.html', {'form': form})

def activite_physique_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = Form_Activite_Phisique_form(request.POST, initial=personne_data)
        if form.is_valid():

             # Fusionnez les deux dictionnaires
            merged_data = {**personne_data, **{'activité_physique': form.cleaned_data}}

             # Si vous souhaitez mettre à jour les données de la session avec les nouvelles données
            request.session['personne_data'] = merged_data

            print("reponce ", merged_data)
            
            # Sauvegarder les données dans la base de données
            # form.save()
            return redirect('accueil')  # changez 'success_url' par votre URL de réussite.
    else:
        form = Form_Activite_Phisique_form(initial=personne_data)
    return render(request, 'activite_physique.html', {'form': form})



