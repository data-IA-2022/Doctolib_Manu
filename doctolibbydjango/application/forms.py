from django import forms
from .models import Symptome, Form_General, Form_Info_Cardiaque_Tension_Arterielle, Form_Prise_Medoc, Form_Alimentation, Form_Activite_Phisique, Form_Autres_Symptomes, Form_Infos_Medicales

from django import forms

# Cette classe crée un formulaire basé sur le modèle Symptome
# Il utilise tous les champs de ce modèle pour le formulaire.
class evaluation_symptomes_form(forms.ModelForm):
    class Meta:
        model = Symptome
        fields = '__all__'  # Utilise tous les champs du modèle Symptome.

# Cette classe crée un formulaire basé sur le modèle Form_General.
# Il utilise tous les champs de ce modèle pour le formulaire.
class general_form_form(forms.ModelForm):
    class Meta:
        model = Form_General
        fields = '__all__'  # Utilise tous les champs du modèle Form_General.

# Cette classe crée un formulaire basé sur le modèle Form_Info_Cardiaque_Tension_Arterielle.
# Il utilise tous les champs de ce modèle pour le formulaire.
class cardio_form(forms.ModelForm):
    class Meta:
        model = Form_Info_Cardiaque_Tension_Arterielle
        fields = '__all__'  # Utilise tous les champs du modèle Form_Info_Cardiaque_Tension_Arterielle.

# Cette classe crée un formulaire basé sur le modèle Form_Prise_Medoc.
# Il utilise tous les champs de ce modèle pour le formulaire.
class prise_Medoc_form(forms.ModelForm):
    class Meta:
        model = Form_Prise_Medoc
        fields = '__all__'  # Utilise tous les champs du modèle Form_Prise_Medoc.

# Cette classe crée un formulaire basé sur le modèle Form_Alimentation.
# Il utilise tous les champs de ce modèle pour le formulaire.
class Form_Alimentation_form(forms.ModelForm):
    class Meta:
        model = Form_Alimentation
        fields = '__all__'  # Utilise tous les champs du modèle Form_Alimentation.

# Cette classe crée un formulaire basé sur le modèle Form_Activite_Phisique.
# Il utilise tous les champs de ce modèle pour le formulaire.
class Form_Activite_Phisique_form(forms.ModelForm):
    class Meta:
        model = Form_Activite_Phisique
        fields = '__all__'  # Utilise tous les champs du modèle Form_Activite_Phisique.

# Cette classe crée un formulaire basé sur le modèle Form_Autres_Symptomes.
# Il utilise tous les champs de ce modèle pour le formulaire.
class Form_Autres_Symptomes_form(forms.ModelForm):
    class Meta:
        model = Form_Autres_Symptomes
        fields = '__all__'  # Utilise tous les champs du modèle Form_Autres_Symptomes.

# Cette classe crée un formulaire basé sur le modèle Form_Infos_Medicales.
# Il utilise tous les champs de ce modèle pour le formulaire.
class Form_Infos_Medicales_form(forms.ModelForm):
    class Meta:
        model = Form_Infos_Medicales
        fields = '__all__'  # Utilise tous les champs du modèle Form_Infos_Medicales.
