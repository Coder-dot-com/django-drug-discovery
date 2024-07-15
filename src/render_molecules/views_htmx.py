from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from generate_molecules.models import GenerationRequest

# Create your views here.

@login_required
def filter_molecules(request, uuid):
    print(request.get_full_path())
    print(request.META['QUERY_STRING'])
    
    generation_request = get_object_or_404(GenerationRequest, user=request.user,uuid=uuid)
    molecules = generation_request.get_molecules()

    #physicochemical filters
    molecular_mass_from = request.GET['molecular_mass_from']
    if molecular_mass_from:
        molecules = molecules.filter(molecular_weight__gte=molecular_mass_from)
    
    
    molecular_mass_to = request.GET['molecular_mass_to']
    if molecular_mass_to:
        molecules = molecules.filter(molecular_weight__lte=molecular_mass_to)
    
    
    H_bond_acceptors_from = request.GET['H_bond_acceptors_from']
    if H_bond_acceptors_from:
        molecules = molecules.filter(H_bond_acceptors__gte=H_bond_acceptors_from)   
        
    H_bond_acceptors_to = request.GET['H_bond_acceptors_to']
    if H_bond_acceptors_to:
        molecules = molecules.filter(H_bond_acceptors__lte=H_bond_acceptors_to)
    
    molecule_count = molecules.count()

    
    context = {
        'generation_request': generation_request,
        'molecules': molecules,
        'molecule_count': molecule_count,
        
        #physicochemical properties
        'molecular_mass_from': molecular_mass_from,
        'molecular_mass_to': molecular_mass_to,
        'H_bond_acceptors_from': H_bond_acceptors_from,
        'H_bond_acceptors_to': H_bond_acceptors_to,
        
        
        
    }
    
    return render(request, 'render_molecules_htmx.html', context=context)

