# app/tables.py
import django_tables2 as tables
from .models import Symptome

class VotreModelTable(tables.Table):
    class Meta:
        model = Symptome
        template_name = 'django_tables2/bootstrap.html'  # si vous utilisez Bootstrap
