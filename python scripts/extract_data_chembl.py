import pandas as pd
from chembl_webresource_client.new_client import new_client

# target = new_client.target
# target_query = target.search('CHEMBL5990')
# targets = pd.DataFrame.from_dict(target_query)


# print(targets)


# selected_target = targets.target_chembl_id[0]
# print(selected_target)




# activity = new_client.activity
# res = activity.filter(target_chembl_id=selected_target).filter(standard_type="Potency")
     

# df = pd.DataFrame.from_dict(res)
     

# print(df.head(3))


     
df = pd.read_csv('/home/u/Desktop/django-drug-discovery/python scripts/Breast cancer type 1 susceptibility protein - Potency.csv', sep=';', on_bad_lines='warn')

    
options = ['Active', 'active']

df = df.loc[df['Comment'].isin(options)]

# print(df)

    
df = df[['Smiles', 'Standard Type', 'Standard Value', 'Standard Units', 'Molecule ChEMBL ID']]

print(df)


df = df.dropna(subset=['Smiles'])

df = df.dropna(subset=['Standard Type'])
df = df.dropna(subset=['Standard Value'])

df = df.dropna(subset=['Standard Units'])
df = df.drop_duplicates(['Smiles'])


options = ['nM']

df = df.loc[df['Standard Units'].isin(options)]


print(df)
df.to_csv("Breast Cancer cleaned data.csv", index=False)

# 2,13

