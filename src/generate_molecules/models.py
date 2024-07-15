from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Organism(models.Model):
    organism = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.organism


class Disease(models.Model):
    disease = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        return self.disease

class Target(models.Model):
    organism = models.ForeignKey(Organism, on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, null=True, blank=True, on_delete=models.SET_NULL)
    receptor = models.CharField(max_length=1000, null=True, blank=True)
    chembl_id = models.CharField(max_length=1000)
    training_data = models.FileField(upload_to="target_data/training_data/", null=True, blank=True)
    standard_type = models.CharField(max_length=1000, null=True, blank=True)
    standard_units = models.CharField(max_length=1000, null=True, blank=True)
 
    
    comparator_choices = (
        ("less_than", 'less_than'),
        ("greater_than", 'greater_than'),
        ("less_than_or_equal_to", 'less_than_or_equal_to'),
        ('greater_than_or_equal_to', 'greater_than_or_equal_to')
    )
    
    default_comparator = models.CharField(max_length=1000, choices=comparator_choices, default="less_than_or_equal_to")
    
    default_standard_value_cutoff = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self) -> str:
        if self.receptor:
            return str(self.receptor)
        elif self.disease:
            return str(self.disease)
        else:
            return str(self.organism)
    #to do later
    # effect_prediction_model =  models.FileField...
    #predicted_effect units = models.Charfield..

class GenerationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    
    datetime_created = models.DateTimeField(auto_now_add=True, editable=True)
    uuid = models.UUIDField(default=uuid4)
    complete = models.BooleanField(default=False)
    choices = [
        ("from_target", "from_target"),
        ("from_molecules", "from_molecules"),
    ]
    type_of_request = models.CharField(choices=choices, max_length=100)
    
    #from_molecules
    molecules_plain_text = models.TextField(max_length=1000000, null=True, blank=True)

    organism = models.ForeignKey(Organism, null=True, blank=True, on_delete=models.SET_NULL)
    disease = models.ForeignKey(Disease, null=True, blank=True, on_delete=models.SET_NULL)

    target = models.ForeignKey(Target, null=True, blank=True, on_delete=models.SET_NULL)

    comparator_choices = (
        ("less_than", 'less_than'),
        ("greater_than", 'greater_than'),
        ("less_than_or_equal_to", 'less_than_or_equal_to'),
        ('greater_than_or_equal_to', 'greater_than_or_equal_to')
    )
    
    comparator = models.CharField(max_length=1000, choices=comparator_choices, null=True, blank=True)
    standard_value_cutoff = models.FloatField(max_length=1000, null=True, blank=True)
    molecules_ai_trained_on = models.IntegerField(null=True, blank=True)
    

    time_started_creating = models.DateTimeField(null=True, blank=True)
    time_completed_creating = models.DateTimeField(null=True, blank=True)

    
    def get_molecules(self):
        return GeneratedMolecule.objects.filter(generation_request=self).order_by('datetime_created').reverse()

class GeneratedMolecule(models.Model):
    generation_request = models.ForeignKey(GenerationRequest, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True, editable=True)

    smile_identifier = models.CharField(max_length=1000)
    molecular_structure = models.ImageField(upload_to="molecular_structures/")
    
    
    #Physicochemical properties
    molecular_formula = models.CharField(max_length=1000, default="error")
    molecular_weight  = models.FloatField(default=0)
    H_bond_acceptors = models.IntegerField(default=0)
    H_bond_donors = models.IntegerField(default=0)
    heavy_atoms = models.IntegerField(default=0)
    rotatable_bonds  = models.IntegerField(default=0)        


    ##druglikeness seperate out for each score
    
    #lipinski's score
    
    logp =  models.FloatField(default=0)
    lipinski_violations = models.IntegerField(default=0)
    
    
    #molecular weigt num of h donors and acceptors already calculated
    
    
    #Synthesisability
    
    synthetic_accessibility_score = models.DecimalField(decimal_places=3,max_digits=100)
    
    

