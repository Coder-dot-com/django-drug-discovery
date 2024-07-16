from django.db import models
from generate_molecules.models import GeneratedMolecule
from django.contrib.auth import get_user_model
from uuid import uuid4

User = get_user_model()

# Create your models here.
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid4)

    datetime_created = models.DateTimeField(auto_now_add=True, editable=True)
    report_name = models.CharField(max_length=1000)
    molecules = models.ManyToManyField(GeneratedMolecule, null=True, blank=True)
    
    
    # include_smile_identifier = models.BooleanField(default=True)
    # include_molecular_structure = models.BooleanField(default=True)
    
    # #Physicochemical properties
    # include_molecular_formula = models.BooleanField(default=True)
    # include_molecular_weight  = models.BooleanField(default=True)
    # include_H_bond_acceptors = models.BooleanField(default=True)
    # include_H_bond_donors = models.BooleanField(default=True)
    # include_heavy_atoms = models.BooleanField(default=True)
    # include_rotatable_bonds  = models.BooleanField(default=True)


    # ##druglikeness seperate out for each score
    
    # #lipinski's score
    
    # # logp =  models.FloatField(default=0)
    # include_lipinskis_violations = models.BooleanField(default=True)
    
    
    # #Synthesisability
    
    # include_synthetic_accessibility_score = models.BooleanField(default=True)