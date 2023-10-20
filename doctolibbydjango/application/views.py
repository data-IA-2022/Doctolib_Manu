from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from authentification.models import Utilisateur, medecinPatient
from .models import (
    Symptome, Form_General, Form_Info_Cardiaque_Tension_Arterielle,
    Form_Prise_Medoc, Form_Alimentation, Form_Activite_Phisique, Form_Autres_Symptomes, Form_Infos_Medicales,
)
from .forms import (evaluation_symptomes_form, general_form_form, cardio_form, prise_Medoc_form, Form_Alimentation_form, 
                    Form_Activite_Phisique_form, Form_Autres_Symptomes_form, Form_Infos_Medicales_form
)

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
            request.session['evaluation_symptomes'] = form.cleaned_data 
            return redirect('/form-general/')
    else:
        form = evaluation_symptomes_form()
    return render(request, 'evaluation_symptomes.html', {'form': form})

@login_required
def form_general_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = general_form_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['form_general_view'] = form.cleaned_data
            return redirect('/cardio_')    
    else:
        form = general_form_form(initial=personne_data)
    return render(request, 'form_general.html', {'form': form})

@login_required
def caldio_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = cardio_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['caldio_view'] = form.cleaned_data
            return redirect('/prs_medoc')
    else:
        form = cardio_form(initial=personne_data)
    return render(request, 'cardio.html', {'form': form})

@login_required
def prise_Medoc_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = prise_Medoc_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['prise_Medoc_view'] = form.cleaned_data
            return redirect('alimentation') 
    else:
        form = prise_Medoc_form(initial=personne_data)
    return render(request, 'prs_medoc.html', {'form': form})

@login_required
def alimentation_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = Form_Alimentation_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['alimentation_view'] = form.cleaned_data
            return redirect('activite_physique') 
    else:
        form = Form_Alimentation_form(initial=personne_data)
    return render(request, 'alimentation.html', {'form': form})

@login_required
def activite_physique_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = Form_Activite_Phisique_form(request.POST, initial=personne_data)
        if form.is_valid():
            request.session['activite_physique_view'] = form.cleaned_data
            return redirect('autres_symptomes')
    else:
        form = Form_Activite_Phisique_form(initial=personne_data)
    return render(request, 'activite_physique.html', {'form': form})

@login_required
def autres_symptomes_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = Form_Autres_Symptomes_form(request.POST, initial=personne_data)
        if form.is_valid():

            converted_dict = {key: value for key, value in request.POST.items()}
            converted_dict = dict(list(converted_dict.items())[1:])
            request.session['autres_symptomes_view'] = converted_dict
            return redirect('info_medicales') 
    else:
        form = Form_Autres_Symptomes_form(initial=personne_data)
    return render(request, 'autres_symptomes.html', {'form': form})

@login_required
def info_medicales_view(request):
    personne_data = request.session.get('personne_data', {})
    if request.method == 'POST':
        form = Form_Infos_Medicales_form(request.POST, initial=personne_data)
        if form.is_valid():

            save_formulaire(request, Symptome, 'evaluation_symptomes')
            save_formulaire(request, Form_General, 'form_general_view')
            save_formulaire(request, Form_Info_Cardiaque_Tension_Arterielle,'caldio_view')
            save_formulaire(request, Form_Prise_Medoc,'prise_Medoc_view')
            save_formulaire(request, Form_Alimentation,'alimentation_view')
            save_formulaire(request, Form_Activite_Phisique,'activite_physique_view')
            save_formulaire(request, Form_Autres_Symptomes,'autres_symptomes_view')
            form.save()
            
            # save_formulaire(request,'form_general_view')
    
            return redirect('accueil')  # changez 'success_url' par votre URL de réussite.
    else:
        form = Form_Infos_Medicales_form(initial=personne_data)
    return render(request, 'info_medicales.html', {'form': form})

def save_formulaire(request, instance ,name):
    # Récupération des données des formulaires précédents
    form1_data = request.session.get(name)
    # Créez des instances de vos modèles sans les sauvegarder immédiatement
    instance1 = instance(**form1_data)
    # Validez le dernier formulaire et sauvegardez toutes les données
    instance1.save()
    # N'oubliez pas de nettoyer les données de la session une fois que vous avez terminé
    del request.session[name]

