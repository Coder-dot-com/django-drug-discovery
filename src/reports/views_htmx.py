from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Report
from generate_molecules.models import GeneratedMolecule, GenerationRequest


@login_required
def create_report_htmx(request):
    
    
    report = Report.objects.create(user=request.user,
                                   report_name = request.POST['report_name'],
                                   
                                   
                                   
                                   )
    
    context = {'report': report}
    
    return  render(request, 'view_report_htmx.html', context=context)


@login_required
def create_report_molecules_display_htmx(request):
    
    
    report = Report.objects.create(user=request.user,
                                   report_name = request.POST['report_name'],
                                   
                                   
                                   
                                   )
    
    context = {'report': report}
    
    return  render(request, 'view_report_htmx.html', context=context)


@login_required
def get_modal_add_to_report_htmx(request, molecule_uuid):
    
    reports = Report.objects.filter(user=request.user).order_by('datetime_created').reverse()
    
    context = {
        'reports': reports,
        'molecule_uuid': molecule_uuid,
        
    }
    
    return render(request, 'add_report_modal_form.html', context=context)


@login_required
def add_molecule_to_report_htmx(request, molecule_uuid):
    
    molecule = GeneratedMolecule.objects.get(generation_request__user=request.user, uuid=molecule_uuid)
    
    report_uuid = request.POST['report_uuid']
    report = Report.objects.get(user=request.user, uuid=report_uuid)
    
    report.molecules.add(molecule)
    report.save()
    #check molecule belongs to user via request
    #check report belongs to user
    
    
    return HttpResponse("Added")


@login_required
def remove_molecule_from_report_htmx(request, molecule_uuid, report_uuid):
    
    molecule = GeneratedMolecule.objects.get(generation_request__user=request.user, uuid=molecule_uuid)
    
    report = Report.objects.get(user=request.user, uuid=report_uuid)
    
    report.molecules.remove(molecule)
    report.save()

    
    molecules = report.molecules.all()
    molecule_count = molecules.count()
    
    

    context = {
        'report': report,
        'molecules': molecules,
        'molecule_count': molecule_count,
        
    }
    
    return render(request, 'view_report_htmx.html', context=context)
    


@login_required
def add_all_molecules_to_report_htmx(request):
    
    
    molecule_uuids = request.POST['molecules'].split(',')
    report_uuid = request.POST['report_uuid']
    report = Report.objects.get(user=request.user, uuid=report_uuid)
    
    molecules_added = len(molecule_uuids)
    
    for molecule_uuid in molecule_uuids:
        molecule = GeneratedMolecule.objects.get(generation_request__user=request.user, uuid=molecule_uuid)    
        report.molecules.add(molecule)
    report.save()
    #check molecule belongs to user via request
    #check report belongs to user
    
    
    return HttpResponse(f"""
                        <div class='display-6 text-center'>Added {molecules_added} molecules to your report</div>
                        <div class='text-muted text-center'> Note: Molecules added already were not added again but are included in the above count</div>
                    
                        """)