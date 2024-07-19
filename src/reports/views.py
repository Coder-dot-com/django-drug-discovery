from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Report
from django.shortcuts import render, HttpResponse, get_object_or_404
import csv

# Create your views here.
@login_required
def list_of_reports(request):
    
    reports = Report.objects.filter(user=request.user).order_by('datetime_created').reverse()
    
    context = {
        'reports': reports,
    }
    
    return render(request, "list_of_reports.html", context=context)


@login_required
def view_report(request, uuid):
    report = get_object_or_404(Report, user=request.user, uuid=uuid)
    
    molecules = report.molecules.all()
    molecule_count = molecules.count()
    
    

    context = {
        'report': report,
        'molecules': molecules,
        'molecule_count': molecule_count,
        
    }
    
    return render(request, 'view_report.html', context=context)


def export_report_molecules_csv(request, uuid):
    report = get_object_or_404(Report, user=request.user, uuid=uuid)
    
    molecules = report.molecules.all()
    molecule_count = molecules.count()

 
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="Report: {report.report_name}.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["SMILES", "molecular_formula", "molecular_weight", "H_bond_acceptors", "H_bond_donors", "heavy_atoms", "rotatable_bonds", "logp", "lipinskis_violations", "synthetic_accessibility_score"])
    
    for molecule in molecules:
        writer.writerow([f"{molecule.smile_identifier}", f"{molecule.molecular_formula}", f"{molecule.molecular_weight}", f"{molecule.H_bond_acceptors}", f"{molecule.H_bond_donors}", f"{molecule.heavy_atoms}", f"{molecule.rotatable_bonds}", f"{molecule.logp}", f"{molecule.lipinskis_violations}", f"{molecule.synthetic_accessibility_score}" ])

    return response   
    


