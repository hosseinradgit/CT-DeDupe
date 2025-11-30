
# Import necessary packages
import pandas as pd
import re


# ClinicalTrials.gov CSV file to RIS
def CT_RIS (ct_csv):
    RIS_list_dicts = []
    for index, row in ct_csv.iterrows():
        RIS_mapper = {} 
        year_raw = row['First Posted']
        year_pattern = r'^[0-9]{4}'
        year_detect = re.findall (year_pattern, year_raw)
        if year_detect:
            year = year_detect[0]
        else:
            year = ''
        
        RIS_mapper = {
            'TY  -  ': 'JOUR',
            'AN  -  ': row['NCT Number'],
            'A1  -  ': row['NCT Number'],
            'T1  -  ': row['Study Title'],
            'JA  -  ': row['Study URL'],
            'PY  -  ': year,
            'N2  -  ': row['Brief Summary'],
            'UR  -  ': row['Study URL'],
            'N1  -  ': 'Study Status: '+ str(row['Study Status']) + "\n" + ' Primary Outcome Measures: ' + str(row['Primary Outcome Measures'])  + "\n" +' Secondary Outcome Measures: ' + str(row['Secondary Outcome Measures']),
            'ER  -  ': " " + "\n"
        }
        RIS_list_dicts.append(RIS_mapper)

    RIS_list = []
    for record in RIS_list_dicts:
        ris_txt = ""
        for key, value in record.items():
            ris_txt = ris_txt + str(key) + str(value) + "\n"
        RIS_list.append (ris_txt)

    return ''.join (item for item in RIS_list)


# ScanMedicine CSV file to RIS
def SM_RIS (SM_csv):
    RIS_list_dicts = []
    for index, row in SM_csv.iterrows():
        RIS_mapper = {} 
        year_raw = row['DateOfRegistration']
        year_pattern = r'^[0-9]{4}'
        year_detect = re.findall (year_pattern, year_raw)
        if year_detect:
            year = year_detect[0]
        else:
            year = ''
        
        RIS_mapper = {
            'TY  -  ': 'JOUR',
            'AN  -  ': row['MainID'],
            'A1  -  ': row['MainID'],
            'T1  -  ': row['PublicTitle'],
            'JA  -  ': row['DocURL'],
            'PY  -  ': year,
            'N2  -  ': 'INTERVENTION: '+ str(row['Interventions']) + ' CONDITION: ' + str(row['HealthConditionOrProblemStudied']) + " PRIMARY OUTCOME: " + str(row['PrimaryOutcomes']) + " SECONDARY OUTCOME: " + str(row['SecondaryOutcomes']) + " INCLUSION CRITERIA: " + str(row['InclusionCriteria']),
            'UR  -  ': row['DocURL'],
            'N1  -  ': row['TrialStatus'],
            'ER  -  ': " " + "\n"
        }
        RIS_list_dicts.append(RIS_mapper)

    RIS_list = []
    for record in RIS_list_dicts:
        ris_txt = ""
        for key, value in record.items():
            ris_txt = ris_txt + str(key) + str(value) + "\n"
        RIS_list.append (ris_txt)

    return ''.join (item for item in RIS_list)


# WHO ICTRP file to RIS
def ICTRP_RIS (ICTRP_csv):
    RIS_list_dicts = []
    for index, row in ICTRP_csv.iterrows():
        RIS_mapper = {} 
        year_raw = str(row['Date_registration3'])
        year_pattern = r'^[0-9]{4}'
        year_detect = re.findall (year_pattern, year_raw)
        if year_detect:
            year = year_detect[0]
        else:
            year = ''
        abstract = 'INTERVENTION: '+ str(row['Intervention']) + ' CONDITION: ' + str(row['Condition']) + " PRIMARY OUTCOME: " + str(row['Primary_outcome']) + " SECONDARY OUTCOME: " + str(row['Secondary_outcome']) + " INCLUSION CRITERIA: " + str(row['Inclusion_Criteria'])
        clean_abstract = re.sub(r"<br\s*/?>", "", abstract)
        RIS_mapper = {
            'TY  -  ': 'JOUR',
            'AN  -  ': row['TrialID'],
            'A1  -  ': row['TrialID'],
            'T1  -  ': row['Public_title'],
            'JA  -  ': row['web_address'],
            'PY  -  ': year,
            'N2  -  ': clean_abstract,
            'UR  -  ': row['web_address'],
            'N1  -  ': '',
            'ER  -  ': " " + "\n"
        }
        RIS_list_dicts.append(RIS_mapper)

    RIS_list = []
    for record in RIS_list_dicts:
        ris_txt = ""
        for key, value in record.items():
            ris_txt = ris_txt + str(key) + str(value) + "\n"
        RIS_list.append (ris_txt)

    return ''.join (item for item in RIS_list)

