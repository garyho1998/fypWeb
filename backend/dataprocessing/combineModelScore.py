import pandas as pd
import os.path

list_business_df = pd.read_excel("list_business_needs.xlsx", sheet_name=0, engine='openpyxl')
result = pd.DataFrame()
for index, row in list_business_df.iterrows():
    filename = "modelScore/ITSolList_{}_xlnet-large-stsb_100000sl_BiEncoder.csv".format(row["Reference Code"]) 
    if not os.path.isfile(filename):
        continue
    score_df = pd.read_csv(filename)
    ref_code_column = pd.DataFrame({'Business Reference Code': [row["Reference Code"]]*len(score_df)})
    score_df = score_df.join(ref_code_column)
    result = result.append(score_df, ignore_index = True)

result.to_csv("business_need_with_match.csv")  