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


df = pd.read_csv('/home/u/Desktop/django-drug-discovery/python scripts/Hepatocyte Growth Factor Cleaned data.csv', sep=',', on_bad_lines='skip')


# # df_lipinski = lipinski(df['Smiles'])

# # df.index = df_lipinski.index

# # df_combined = pd.concat([df,df_lipinski], axis=1)

# # df_combined.to_csv("test.csv")

# # selection = ['Smiles','Molecule ChEMBL ID']
# # df_selection = df[selection]
# # df_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)


# selection = ['Smiles','Molecule ChEMBL ID']
# df_selection = df[selection]
# # df_selection.to_csv('molecule.smi', sep='\t', index=False, header=False)


from rdkit import Chem
from mordred import Calculator, descriptors

smiles = []

for i in df['Smiles'].tolist():
  cpd = str(i).split('.')
  cpd_longest = max(cpd, key = len)
  smiles.append(cpd_longest)

df = df.drop(columns="Smiles", axis=1)

smiles = pd.Series(smiles, name = 'Smiles')
df = pd.concat([df,smiles], axis=1)


calc = Calculator(descriptors, ignore_3D=True)

smiles = df['Smiles']

mols = [Chem.MolFromSmiles(smi) for smi in smiles]
df_X = calc.pandas(mols)


i = 0
for column in df_X.columns:
    # print(str(df_X[column].dtypes))
    if str(df_X[column].dtypes) != "float64" and str(df_X[column].dtypes) != "int64":
        print("dropping column", column)
        
        df_X = df_X.drop(columns=[column], axis=1)
    # print(i)
    i+=1


df_X.to_csv("mordredhgf.csv", index=False)
import numpy as np



df_Y = df['Standard Value']

df_X = pd.read_csv('mordredhgf.csv')


import matplotlib.pyplot as plt

plt.hist(df_Y)

# plt.show()


from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import VarianceThreshold
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
import lazypredict
from lazypredict.Supervised import LazyRegressor
from sklearn.preprocessing import Normalizer


# norm = Normalizer().fit(df_X)

# norm_X_train = norm.transform(df_X)
# print(list(norm_X_train.var(axis=0)))


# selector = VarianceThreshold(threshold = 1e-7)
# selected_features = selector.fit_transform(norm_X_train)

# X_train, X_test, Y_train, Y_test = train_test_split(selected_features, df_Y, test_size=0.2)



# clf = LazyRegressor(verbose=0,ignore_warnings=True, custom_metric=None)
# models_test, predictions_test = clf.fit(X_train, X_test, Y_train, Y_test)


# print(models_test.drop(columns="Time Taken", axis=1))
# print(predictions_test)





#teaoot