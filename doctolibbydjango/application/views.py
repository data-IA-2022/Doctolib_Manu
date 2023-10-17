from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from authentification.models import Utilisateur, medecinPatient
from application.models import Symptome, Form_General

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
  
    # Liste des noms des champs
    noms_des_champs = [
        "Irritabilité",
        "Sentiments dépressifs",
        "Bouche sèche ou gorge sèche",
        "Actions ou gestes impulsifs",
        "Grincement des dents",
        "Difficulté à rester assis",
        "Cauchemars",
        "Diarrhée",
        "Attaques verbales envers quelqu’un",
        "Hauts et bas émotifs",
        "Grande envie de pleurer"
    ]

    print("------------------------------------------------------ ")

    if request.method == 'POST':
     
        symptome_instance = Symptome()

        symptome_instance.irratibilite = request.POST.get("Irritabilité")
        symptome_instance.sentiment_depressif = request.POST.get("Sentiments dépressifs")
        symptome_instance.bouche_gorge_seche = request.POST.get("Bouche sèche ou gorge sèche")
        symptome_instance.actions_gestes_impulsif = request.POST.get("Actions ou gestes impulsifs")
        symptome_instance.grincement_dents = request.POST.get("Grincement des dents")
        symptome_instance.difficulte_a_rester_assis = request.POST.get("Difficulté à rester assis")
        symptome_instance.cauchemars = request.POST.get("Cauchemars")
        symptome_instance.diarrhee = request.POST.get("Diarrhée")
        symptome_instance.attaques_verbales_envers_qq1 = request.POST.get("Attaques verbales envers quelqu’un")
        symptome_instance.haut_bas_emotifs = request.POST.get("Hauts et bas émotifs")
        symptome_instance.grande_envie_pleurer = request.POST.get("Grande envie de pleurer")

        symptome_instance.save()

        return redirect('/form-general/')

    context = {
        'choix_evaluation': Symptome.choises_evaluation,
        'noms_des_champs': noms_des_champs
    }
    return render(request, 'evaluation_symptomes.html', context)


def form_general_view(request):
    if request.method == "POST":
        instance = Form_General()


        print(request.POST)
        # form = FormGeneralForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     # Add some action here if needed (e.g., redirect to a success page)

        instance.save()

    # else:
    #     form = FormGeneralForm()
        pass

    context = {
        'choix_evaluation': Symptome.choises_evaluation,
    }

    return render(request, 'form_general.html', context)




