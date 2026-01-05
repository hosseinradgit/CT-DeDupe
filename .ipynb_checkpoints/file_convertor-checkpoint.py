
import pandas as pd
import re

def convert_df_to_csv(df):
                return df.to_csv(index=False).encode('utf-8')


def convert_df_to_ris(df):
    ris_content = ""
    for index, row in df.iterrows():
        ris_content += "TY  - JOUR\n"
        mapping = {
            "DB": "Database",
            "AN": "Acession_Number",
            "A1": "Author",
            "T1": "Title",
            "JA": "URL",
            "PY": "Year",
            "N2": "Abstract",
            "KW": "Keywords",
            "UR": "URL",
            "N1": "Note"
        }
        
        for tag, col in mapping.items():
            value = row.get(col)
            if pd.notna(value) and str(value).lower() != 'nan':
                ris_content += f"{tag}  - {value}\n"
        ris_content += "ER  - \n\n" 
    return ris_content.encode('utf-8')


def convert_non_trial_df_to_ris(df):
    ris_content = ""
    mapping = {
        "DB": "Database",
        "AN": "Acession_Number",
        "A1": "Author",
        "T1": "Title",
        "JA": "Source",
        "PY": "Year",
        "VL": "Volume",
        "IS": "Issue",
        "N2": "Abstract",
        "KW": "Keywords",
        "UR": "URL",
        "N1": "Note"
    }

    for index, row in df.iterrows():
        ris_content += "TY  - JOUR\n"
        for tag, column in mapping.items():
            value = row.get(column)
            if tag == "PY" and "/" in str(value):
                value = str(value).strip("/")
            if tag == "JA" and len(str(value).split(";")) >1:
                value = str(value).split(";")[0]                           
            if pd.notna(value) and str(value).strip().lower() != 'nan' and str(value).strip() != '':
                ris_content += f"{tag}  - {value}\n"
        ris_content += "ER  - \n\n"
    return ris_content.encode('utf-8')

