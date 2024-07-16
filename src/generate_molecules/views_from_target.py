from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import GenerationRequest, Target, Organism,Disease
import pandas as pd
from drug_discovery.settings import BASE_DIR
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required



import boto3
s3 = boto3.client('s3')
from drug_discovery.settings import AWS_STORAGE_BUCKET_NAME


@login_required
def render_targets_organism(request, generation_request_id):
    generation_request =  GenerationRequest.objects.get(id=generation_request_id)
    
    organisms = Organism.objects.all()
    
    
    context = {'generation_request': generation_request,
               'organisms': organisms,
               }

    return render(request, "generation_flow/from_target_organism.html", context=context)


@login_required
def handle_target_organism_post(request, uuid):
    
    generation_request =  GenerationRequest.objects.get(uuid=uuid)
    
    organism = get_object_or_404(Organism, id=(request.POST['organism']))
    
    generation_request.organism = organism
    generation_request.save()
    
    return render_diseases_and_any_targets(request, uuid)

        

@login_required
def render_diseases_and_any_targets(request, uuid):
    generation_request =  GenerationRequest.objects.get(uuid=uuid)
    organism = generation_request.organism
    
    
    #if diease only include first target with the disease
    targets_for_organism = Target.objects.filter(organism=organism)
    
    #first get targets with null disease
    targets_with_no_disease = (targets_for_organism.filter(disease__isnull=True))
    
    
    
    #get targets and call unique 
    target_diseases = (targets_for_organism.exclude(id__in=targets_with_no_disease).order_by('disease').distinct('disease'))
    
    #combine the two queries
    
    targets = targets_with_no_disease.union(target_diseases)
    
    
    context = {'generation_request': generation_request,
               'targets': targets,
               } 
    
    return render(request, "generation_flow/select_disease_or_target.html", context=context)
    

@login_required
def handle_disease_target_post(request, uuid):
    generation_request =  GenerationRequest.objects.get(uuid=uuid)

    #target id in request.post
    
    #if target has disease then different pathway
    #if no disease then continue to selct cutoffs
    target = Target.objects.get(id=request.POST['target'])
    context = {'generation_request': generation_request,}
    if target.disease:
        generation_request.disease = target.disease
        generation_request.save()
        
        targets = Target.objects.filter(organism=target.organism, disease=target.disease, receptor__isnull=False)
        
        context['targets'] = targets
        
        return render(request, "generation_flow/render_all_disease_targets.html", context=context)
    
    
    generation_request.target = target
    generation_request.save()
    return render_cutoffs(request, generation_request.uuid)

@login_required
def handle_target_post(request, uuid):
    generation_request =  GenerationRequest.objects.get(uuid=uuid)

    target = Target.objects.get(id=request.POST['target'])
    generation_request.target = target
    generation_request.save()
    
    
    return render_cutoffs(request, uuid)


@login_required
def render_cutoffs(request, uuid):
    generation_request =  GenerationRequest.objects.get(uuid=uuid)
    target = generation_request.target

    type_of_request = target.default_comparator
    cutoff = float(target.default_standard_value_cutoff)

    file_path = f'{BASE_DIR}/tmp/{target.training_data}'

    try:
        df = pd.read_csv(file_path)   
    except FileNotFoundError:
        s3.download_file(AWS_STORAGE_BUCKET_NAME, str(target.training_data), file_path)
        df = pd.read_csv(file_path)   
        
        
    if type_of_request == "less_than":
        df = df.loc[(df['Standard Value'] < cutoff)]
        molecule_count = df.count()[0]
        
    elif type_of_request == "greater_than":
        df = df.loc[(df['Standard Value'] > cutoff)]
        molecule_count = df.count()[0]    
    
    elif type_of_request == "less_than_or_equal_to":
        df = df.loc[(df['Standard Value'] <= cutoff)]
        molecule_count = df.count()[0]    
    elif type_of_request == "greater_than_or_equal_to":
        df = df.loc[(df['Standard Value'] >= cutoff)]
        molecule_count = df.count()[0]       


    context = {'generation_request': generation_request,
               'molecule_count': molecule_count,
               'type_of_request': type_of_request,
               'cutoff': cutoff,
               }
        
    return render(request, "generation_flow/render_cutoffs.html", context=context)



@login_required
def molecule_count(request, uuid):
    
    generation_request =  GenerationRequest.objects.get(uuid=uuid)
    
    target = generation_request.target
    
    try:
        submitted = request.POST['submitted']
    except MultiValueDictKeyError:
        submitted = False
    
    type_of_request = request.POST['type_of_request']
    cutoff = float(request.POST['cutoff'])

    file_path = f'{BASE_DIR}/tmp/{target.training_data}'

    try:
        df = pd.read_csv(file_path)   
    except FileNotFoundError:
        s3.download_file(AWS_STORAGE_BUCKET_NAME, str(target.training_data), file_path)
        df = pd.read_csv(file_path)   
        
    
    if type_of_request == "less_than":
        df = df.loc[(df['Standard Value'] < cutoff)]
        molecule_count = df.count()[0]
        
    elif type_of_request == "greater_than":
        df = df.loc[(df['Standard Value'] > cutoff)]
        molecule_count = df.count()[0]    
    
    elif type_of_request == "less_than_or_equal_to":
        df = df.loc[(df['Standard Value'] <= cutoff)]
        molecule_count = df.count()[0]    
    elif type_of_request == "greater_than_or_equal_to":
        df = df.loc[(df['Standard Value'] >= cutoff)]
        molecule_count = df.count()[0]   
           
    if not submitted:  

        context = {'generation_request': generation_request,
                'molecule_count': molecule_count,
                'type_of_request': type_of_request,
                'cutoff': cutoff,
                
                }
    
        return render(request, "generation_flow/render_cutoffs.html", context=context)

    else:
        generation_request.comparator = type_of_request
        generation_request.standard_value_cutoff = cutoff
        generation_request.molecules_ai_trained_on = molecule_count
        
        # generation_request.molecules_plain_text
        try:
            df.columns = df.columns.str.lower()
            smiles = df['smiles'].values.tolist()
        except KeyError:
            smiles = df.iloc[:, 0]
            
                
        smiles = "\n".join(smiles)
        
        generation_request.molecules_plain_text = smiles
        generation_request.save()
        
        context = {'generation_request': generation_request,
          
                }
        return render(request, "generation_flow/request_summary.html", context=context)


