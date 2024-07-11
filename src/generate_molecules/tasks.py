from drug_discovery.celery import app
from .models import GenerationRequest, GeneratedMolecule
import shutil
import pandas as pd
from io import BytesIO
from django.core.files import File



from rdkit.Contrib.SA_Score import sascorer

import subprocess
import os
from datetime import datetime



@app.task
def generate_molecule(generation_request):
    

    generation_request = GenerationRequest.objects.get(id=224)
    generation_request.time_started_creating = datetime.now()
    generation_request.save()

    #run transfer learning
    from_molecules = generation_request.molecules_plain_text
    from_molecules = from_molecules.split('\n')
    
    uuid = str(generation_request.uuid)
    
    os.chdir("transfer_learning_models")
    
    os.mkdir(uuid)
    
    os.chdir(uuid)
    
    
    df = pd.DataFrame(from_molecules, columns=['SMILES'])
    
    df = df.drop_duplicates(subset=['SMILES'])
    
    TL_train_filename = f"{uuid}_train.smi"
    TL_validation_filename = f"{uuid}_validation.smi"

    data = df.sample(frac=1)
    n_head = len(data) // 5
    n_tail = len(df) - n_head
    
    
    train, validation = data.head(n_head), data.tail(n_tail)

    train.to_csv(TL_train_filename, sep="\t", index=False, header=False)
    validation.to_csv(TL_validation_filename, sep="\t", index=False, header=False)

    TL_parameters = f"""
    run_type = "transfer_learning"
    use_cuda = false  # run on the GPU if true, on the CPU if false


    [parameters]

    num_epochs = 30  #can change this based on user input
    save_every_n_epochs = 2
    batch_size = 100
    sample_batch_size = 2000

    input_model_file = "../../stage1.chkpt"
    output_model_file = "TL_reinvent.model"
    smiles_file = "{TL_train_filename}"
    validation_smiles_file = "{TL_validation_filename}"
    standardize_smiles = true
    randomize_smiles = true
    randomize_all_smiles = false
    internal_diversity = true
    """
    
    TL_config_filename = f"transfer_learning.toml"

    with open(TL_config_filename, "w") as tf:
        tf.write(TL_parameters)
        
    

    subprocess.run(["reinvent", "-l", "transfer_learning.log", TL_config_filename]) 







    sampling_parameters=f"""
run_type = "sampling"
use_cuda = false  # run on the GPU if true, on the CPU if false


[parameters]
## Mol2Mol: find molecules similar to the provided molecules
model_file = "TL_reinvent.model.30.chkpt" #  trained model after transfer learning can change 20 to user based input
sample_strategy = "multinomial"  # multinomial or beamsearch (deterministic)
temperature = 1.0 # temperature in multinomial sampling

output_file = 'sampling.csv'  # sampled SMILES and NLL in CSV format

num_smiles = 50  # number of SMILES to be sampled, 1 per input SMILES
unique_molecules = true  # if true remove all duplicatesd canonicalize smiles
randomize_smiles = false # if true shuffle atoms in SMILES randomly
    """
    
    config_filename = f"{uuid}.toml"

    with open(config_filename, "w") as tf:
        tf.write(sampling_parameters)
    
    
    subprocess.run(["reinvent", "-l", "sampling.log", config_filename]) 
    
    
    #load csv into pandas and genrate images from smiles using rdkit
    df = pd.read_csv(f"sampling.csv")
    
    smiles = df['SMILES']
    from rdkit import Chem
    from rdkit.Chem import Draw
    for i in range(0,len(smiles)):
        
        smile = smiles[i]
        m = Chem.MolFromSmiles(smile)
        img = Draw.MolToImage(m, size=(1000,1000))
        
        
        s = sascorer.calculateScore(m)
    
        img_io = BytesIO()
        img.save(img_io, 'png')          
        GeneratedMolecule.objects.create(generation_request=generation_request,smile_identifier=smile, 
                                         molecular_structure=File(img_io, name=f"{generation_request.uuid}_{i}.png"),
                                         synthetic_accessibility_score=s
                                         )

    generation_request.time_completed_creating = datetime.now()
    generation_request.complete = True
    generation_request.save()
            
    os.chdir('..')
    os.chdir('..')

