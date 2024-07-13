import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski

     

    

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


df = pd.read_csv('/home/u/Desktop/django-drug-discovery/python scripts/Breast Cancer cleaned data.csv', sep=',', on_bad_lines='skip')


# df_lipinski = lipinski(df['Smiles'])

# df.index = df_lipinski.index

# df_combined = pd.concat([df,df_lipinski], axis=1)

# df_combined.to_csv("test.csv")

# selection = ['Smiles','Molecule ChEMBL ID']
# df3_selection = df[selection]
# df3_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)

import subprocess
import os


# os.chdir("PaDEL/")
# subprocess.check_call(['./padel.sh', './test'])


df_X = pd.read_csv('/home/u/Desktop/django-drug-discovery/PaDEL/test/descriptors_output.csv')
df_X = df_X.drop(columns=['Name'])

df_Y = df['Standard Value']

dataset = pd.concat([df_X,df_Y], axis=1)

# print(df_Y)
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import VarianceThreshold
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
import lazypredict
from lazypredict.Supervised import LazyRegressor

selection = VarianceThreshold(threshold=(0.1))    
X = selection.fit_transform(df_X)

X_train, X_test, Y_train, Y_test = train_test_split(X, df_Y, test_size=0.2, random_state=17)

clf = LazyRegressor(verbose=0,ignore_warnings=True, custom_metric=None)
models_train, predictions_train = clf.fit(X_train, X_train, Y_train, Y_train)
models_test, predictions_test = clf.fit(X_train, X_test, Y_train, Y_test)

# print(predictions_train)

print(predictions_test)