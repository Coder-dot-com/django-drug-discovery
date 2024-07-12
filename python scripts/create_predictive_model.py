import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

     
# df = pd.read_csv('/home/u/Desktop/django-drug-discovery/python scripts/Breast Cancer cleaned data.csv', sep=',', on_bad_lines='skip')

    

# df = df.dropna(subset=['Smiles'])

# df = df.dropna(subset=['Standard Type'])
# df = df.dropna(subset=['Standard Value'])

# df = df.dropna(subset=['Standard Units'])
# df = df.drop_duplicates(['Smiles'])


# def lipinski(smiles, verbose=False):

#     moldata= []
#     for elem in smiles:
#         mol=Chem.MolFromSmiles(elem) 
#         moldata.append(mol)
       
#     i=0
#     rows = []
#     for mol in moldata:        
       
#         desc_MolWt = Descriptors.MolWt(mol)
#         desc_MolLogP = Descriptors.MolLogP(mol)
#         desc_NumHDonors = Lipinski.NumHDonors(mol)
#         desc_NumHAcceptors = Lipinski.NumHAcceptors(mol)

           
#         row = np.array([desc_MolWt,
#                         desc_MolLogP,
#                         desc_NumHDonors,
#                         desc_NumHAcceptors])   

#         rows.append(row)
  
    
#     columnNames=["MW","LogP","NumHDonors","NumHAcceptors"]   
#     descriptors = pd.DataFrame(data=rows,columns=columnNames)
    
#     return descriptors




# df_lipinski = lipinski(df['Smiles'])

# df.index = df_lipinski.index

# df_combined = pd.concat([df,df_lipinski], axis=1)

# df_combined.to_csv("test.csv")

# selection = ['Smiles','Molecule ChEMBL ID']
# df3_selection = df[selection]
# df3_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

import subprocess
import os

print(os.listdir())

os.chdir("PaDEL/")
subprocess.check_call(['./padel.sh', './test'])