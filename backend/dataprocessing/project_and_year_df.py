import pandas as pd
import os.path
import ast
import numpy as np
import pathlib
import ast

current_file_path = str(pathlib.Path(__file__).parent.absolute())

def getFirstYear(years):
    yearlist = ast.literal_eval(years)
    if not yearlist: return ""
    return yearlist[0]


project_df = pd.read_excel(current_file_path+"/clean_project.xlsx", sheet_name=0, engine='openpyxl')
year_df = pd.read_excel(current_file_path+"/website_year_df.xlsx", sheet_name=0, engine='openpyxl').drop_duplicates("Reference Code")
year_df['year'] = year_df['year'].apply(getFirstYear)

for index, row in project_df.iterrows():
    scores = ast.literal_eval(row['Score'])
    scores = [float(x) for x in scores]
    argmax = np.argmax(scores)
    project_df.loc[index, "Sentence Output"] = ast.literal_eval(row['Sent'])[argmax]
    project_df.loc[index, "Answer"] = ast.literal_eval(row['Answer'])[argmax]
    

result  = project_df.merge(year_df, left_on='Reference Code', right_on='Reference Code')
result = result[['Reference Code', 'year', 'Sentence Output', 'Answer']]
result.to_csv(current_file_path+"/project_and_year_one.csv")  