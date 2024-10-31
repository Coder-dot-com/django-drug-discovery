from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import GenerationRequest

from .tasks import generate_molecule
import pandas as pd
import magic
from rdkit.Chem import MolFromSmiles, Draw

from .views_from_target import render_targets_organism
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from reports.models import Report

@login_required
def molecules_or_target(request):
    context = {'hide_restart_button': True}
    return render(request, 'generation_flow/molecules_or_target.html', context=context)



@login_required
def molecules_or_target_post(request):
    type_of_request = request.POST['type_of_request']
    print(type_of_request)
    
    
    generation_request = GenerationRequest.objects.create(user=request.user,type_of_request=type_of_request)
    
    context = {'generation_request': generation_request}
    
    if type_of_request == "from_molecules":
        return render(request, "generation_flow/from_molecules.html", context=context)
    
    elif type_of_request == "from_target":
        return render_targets_organism(request, generation_request_id=generation_request.uuid)

@login_required
def from_molecules_post(request, uuid):  
    
    generation_request = get_object_or_404(GenerationRequest, user=request.user,uuid=uuid)
    
    
    #read first bytes of csv file
    try:
        csv = request.FILES.get('moleculecsvfile')
        
        header = csv.read(512)
        csv.seek(0)
    
        type_of_file = (magic.from_buffer(header, mime=True)) 
        
        if type_of_file == "text/csv" or type_of_file == "text/plain":
            #upload file and call generation request
            generation_request
            df = pd.read_csv(csv)
            
            try:
                df.columns = df.columns.str.lower()
                smiles = df['smiles'].values.tolist()
            except KeyError:
                smiles = df.iloc[:, 0]
            
            list_of_smiles = smiles
                
            smiles = "\n".join(smiles)
            
            for i in range(0, len(list_of_smiles)):
                smile = list_of_smiles[i]
            
                mol = MolFromSmiles(smile)
                if not mol:
                    return HttpResponse(f"Please check the molecules provided are correct, specifically {list_of_smiles[i]}")
            


            
            #create and save to database
        else:
            
            return HttpResponse(f" Incorrect file type, file type should be csv not {type_of_file}. Reload the page to try again")
    except AttributeError: #means no file uploaded check for copy and pasted text
        
        smiles = (request.POST['SMILES'])
        if not smiles:
            return HttpResponse("Please ensure you upload a csv or enter smiles. Reload the page to try again") 
        else:
            #validate smiles #split on /n
            list_of_smiles = smiles.split('\n')
            
            for i in range(0, len(list_of_smiles)):
                smile = list_of_smiles[i]
            
                mol = MolFromSmiles(smile)
                if not mol:
                    return HttpResponse(f"Please check the molecules provided are correct, specifically {list_of_smiles[i]}")
            


    
    generation_request.molecules_plain_text = smiles
    generation_request.molecules_ai_trained_on = len(list_of_smiles)
    generation_request.save()
    
    #Here render summary
    
    context = {'generation_request': generation_request,     
            }
    return render(request, "generation_flow/request_summary.html", context=context)



        


@login_required
def create_molecule(request, uuid):
    
    generation_request = get_object_or_404(GenerationRequest, user=request.user,uuid=uuid)
    
    generation_request.submitted = True
    generation_request.save()
    
    transaction.on_commit(lambda: generate_molecule.delay(generation_request.id))
    
    context = {'generation_request' : generation_request}
    
    return render(request, 'render_molecules_htmx.html', context=context)


@login_required
def poll_for_request_completion(request, uuid):
    
    generation_request = get_object_or_404(GenerationRequest, user=request.user,uuid=uuid, complete=True)
    
    molecules = generation_request.get_molecules()
    molecule_count = molecules.count()
    reports = Report.objects.filter(user=request.user).order_by('datetime_created').reverse()

    if generation_request:
        context = {'generation_request' : generation_request,
                   'molecules': molecules,
                   'molecule_count': molecule_count,
                   'reports': reports,
                   
                   }        
        rendered_page =render(request, 'render_molecules_htmx.html', context=context)
        url_to_push =  request.build_absolute_uri(reverse('render_molecules', kwargs={
                "uuid": uuid,}
                            ))
        rendered_page.headers['Hx-Push-URL'] = url_to_push
        return rendered_page
    
@login_required
def restart_creation_flow(request):
    return molecules_or_target(request)