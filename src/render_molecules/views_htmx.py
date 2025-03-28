from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from generate_molecules.models import GenerationRequest
from django.urls import reverse
from reports.models import Report

# Create your views here.

@login_required
def filter_molecules_htmx(request, uuid):
    
    generation_request = get_object_or_404(GenerationRequest, user=request.user,uuid=uuid)
    molecules = generation_request.get_molecules()
    reports = Report.objects.filter(user=request.user).order_by('datetime_created').reverse()

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
        
        
    H_bond_donors_from = request.GET['H_bond_donors_from']
    if H_bond_donors_from:
        molecules = molecules.filter(H_bond_donors__gte=H_bond_donors_from)   
        
    H_bond_donors_to = request.GET['H_bond_donors_to']
    if H_bond_donors_to:
        molecules = molecules.filter(H_bond_donors__lte=H_bond_donors_to)       
        

    heavy_atoms_from = request.GET['heavy_atoms_from']
    if heavy_atoms_from:
        molecules = molecules.filter(heavy_atoms__gte=heavy_atoms_from)   
        
    heavy_atoms_to = request.GET['heavy_atoms_to']
    if heavy_atoms_to:
        molecules = molecules.filter(heavy_atoms__lte=heavy_atoms_to)        
        
    
    #druglikeness
        
    lipinskis_violations_from = request.GET['lipinskis_violations_from']
    if lipinskis_violations_from:
        molecules = molecules.filter(lipinskis_violations__gte=lipinskis_violations_from)   
        
    lipinskis_violations_to = request.GET['lipinskis_violations_to']
    if lipinskis_violations_to:
        molecules = molecules.filter(lipinskis_violations__lte=lipinskis_violations_to)    
        
        
    #synthesizability
    
    synthetic_accessibility_score_from = request.GET['synthetic_accessibility_score_from']
    if synthetic_accessibility_score_from:
        molecules = molecules.filter(synthetic_accessibility_score__gte=synthetic_accessibility_score_from)   
        
    synthetic_accessibility_score_to = request.GET['synthetic_accessibility_score_to']
    if synthetic_accessibility_score_to:
        molecules = molecules.filter(synthetic_accessibility_score__lte=synthetic_accessibility_score_to)        
        
    
    molecule_count = molecules.count()

    
    context = {
        'generation_request': generation_request,
        'molecules': molecules,
        'molecule_count': molecule_count,
        'reports': reports,
        
        #physicochemical properties
        'molecular_mass_from': molecular_mass_from,
        'molecular_mass_to': molecular_mass_to,
        'H_bond_acceptors_from': H_bond_acceptors_from,
        'H_bond_acceptors_to': H_bond_acceptors_to,
        'H_bond_donors_from': H_bond_donors_from,
        'H_bond_donors_to': H_bond_donors_to,
        'heavy_atoms_from': heavy_atoms_from,
        'heavy_atoms_to': heavy_atoms_to,
        
        #Druglikeness
        
        'lipinskis_violations_from': lipinskis_violations_from,
        'lipinskis_violations_to': lipinskis_violations_to,
        
        #Syhnthesizability
        'synthetic_accessibility_score_from': synthetic_accessibility_score_from,
        'synthetic_accessibility_score_to': synthetic_accessibility_score_to,
        
        
    }
    
    
    
    rendered_page =  render(request, 'render_molecules_htmx.html', context=context)
    
    #to do push page filtered url
    
    url_to_push =  request.build_absolute_uri(reverse('filter_molecules', kwargs={
                "uuid": uuid,}
                            ))
    
    url_to_push = str(url_to_push) + "?" + str(request.META['QUERY_STRING'])

    
    rendered_page.headers['Hx-Push-URL'] = url_to_push
    return rendered_page

@login_required
def load_reports_list_htmx(request):
    reports = Report.objects.filter(user=request.user).order_by('datetime_created').reverse()
    
    context ={
        'reports': reports
    }

    return render(request, "includes/reports_list.html", context=context)