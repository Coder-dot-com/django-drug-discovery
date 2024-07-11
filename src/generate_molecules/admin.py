from django.contrib import admin
from .models import GenerationRequest, GeneratedMolecule, Target, Disease, Organism
# Register your models here.


class GeneratedMoleculeInline(admin.TabularInline):
    model = GeneratedMolecule
    
# class FromMoleculeInline(admin.TabularInline):
#     model = FromMolecules
class GenerationRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'datetime_created', 'uuid', 'complete', 'type_of_request', 'organism', 'disease', 'target', 'molecules_plain_text']
    inlines = [GeneratedMoleculeInline]

admin.site.register(GenerationRequest, GenerationRequestAdmin)
admin.site.register(GeneratedMolecule)


admin.site.register(Organism)
admin.site.register(Disease)
admin.site.register(Target)