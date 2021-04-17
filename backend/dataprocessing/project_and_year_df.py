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


project_df = pd.read_excel(current_file_path+"/data_file/clean_project.xlsx", sheet_name=0, engine='openpyxl')
year_df = pd.read_excel(current_file_path+"/data_file/website_year_df.xlsx", sheet_name=0, engine='openpyxl').drop_duplicates("Reference Code")
year_df['year'] = year_df['year'].apply(getFirstYear)

for index, row in project_df.iterrows():
    scores = ast.literal_eval(row['Score'])
    scores = [float(x) for x in scores]
    argmax = np.argmax(scores)
    sent = ast.literal_eval(row['Sent'])[argmax]
    ans = ast.literal_eval(row['Answer'])[argmax]
    if (len(sent)-len(ans) < 5):
        sent = ""
        ans = ""
    project_df.loc[index, "Sentence Output"] = sent
    project_df.loc[index, "Answer"] = ans
    

result  = project_df.merge(year_df, left_on='Reference Code', right_on='Reference Code')
result = result[['Reference Code', 'year', 'Sentence Output', 'Answer']]
result.to_csv(current_file_path+"/data_file/project_and_year_one.csv")  