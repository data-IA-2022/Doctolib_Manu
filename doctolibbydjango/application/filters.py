# app/filters.py
import django_filters
from .models import Symptome

class VotreModelFilter(django_filters.FilterSet):
    class Meta:
        model = Symptome
        fields = '__all__'#['champ1', 'champ2']''  # Spécifiez les champs que vous souhaitez filtrer.
