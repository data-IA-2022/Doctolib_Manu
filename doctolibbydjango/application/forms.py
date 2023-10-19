from django import forms
from .models import Symptome, Form_General, Form_Info_Cardiaque_Tension_Arterielle


class evaluation_symptomes_form(forms.ModelForm):
    class Meta:
        model = Symptome
        fields = ['irratibilite',
                    'sentiment_depressif', 
                    'bouche_gorge_seche', 
                    'actions_gestes_impulsif', 
                    'grincement_dents', 
                    'difficulte_a_rester_assis', 
                    'cauchemars', 
                    'diarrhee', 
                    'attaques_verbales_envers_qq1', 
                    'haut_bas_emotifs', 
                    'grande_envie_pleurer',
                    ]

class general_form_form(forms.ModelForm):
    class Meta:
        model = Form_General
        fields = ['poids' ,
                    'tour_2_taille',
                    ]
        
class cardio_form(forms.ModelForm):
    class Meta:
        model = Form_Info_Cardiaque_Tension_Arterielle
        fields = ['frquence_cardiaque' ,
                    'tension_systolique_matin' ,
                    'tension_systolique_soir' ,
                    'tension_diastolique_matin' ,
                    'tension_diastolique_soir' ,
                    'description' ,
                ]

        





