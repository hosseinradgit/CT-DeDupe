import streamlit as st
import pandas as pd
import re

def RIS_To_DataFrame (ris_data):
    tag_map = {
    'TY': 'Reference_Type',
    'TI': 'Title', 'T1': 'Title',
    'AN': 'Acession_Number', 'U2': 'Acession_Number',
    'AB': 'Abstract', 'N2': 'Abstract',
    'AU': 'Author', 'A1': 'Author',
    'JA': 'Source', 'SO': 'Source', 'JF':'Source',
    'PY': 'Year', 'Y1': 'Year', 'YR':'Year',
    'DO': 'DOI', 'DI': 'DOI',
    'C3': 'Trial Source',
    'M3': 'Note', 'CY': 'Note',
    'KW':'Keywords',
    'UR': 'URL',
    'DB': 'Database',
    'PT': 'Publication_Type',
    'VL':'Volume',
    'IS':'Issue'}
    standard_columns = set(tag_map.values())
    record_splitter = r'ER\s{2}-\s*'
    line_parser = r'^([A-Z0-9]{2})\s{2}-\s+(.*)'
    
    parsed_records = []
    ris_records = re.split(record_splitter, ris_data.strip())
    for record_str in ris_records:
        if not record_str.strip():
            continue
        record_dict = {}
        current_standard_tag = None 
        
        for line in record_str.strip().split('\n'):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            match = re.search(line_parser, line_stripped)
            if match:
                ris_tag = match.group(1).strip()
                ris_value = match.group(2).strip()
                current_standard_tag = tag_map.get(ris_tag)
    
                if current_standard_tag:
                    if current_standard_tag in record_dict:
                        record_dict[current_standard_tag] += f"; {ris_value}"
                    else:
                        record_dict[current_standard_tag] = ris_value
            else:
                if current_standard_tag:
                    record_dict[current_standard_tag] += f" {line_stripped}"
        
        parsed_records.append(record_dict)
    df = pd.DataFrame(parsed_records, columns=sorted(list(standard_columns)))
    object_cols = df.select_dtypes(include=['object']).columns
    df[object_cols] = df[object_cols].where(pd.notna, None)
    df['Author'] = df['Author'].astype(str).str.rstrip(',')
    
    return df




def CENTRAL_Parse (data):
    filtered_CENTRAL_Dataframe = None
    filtered_CENTRAL_non_trials_Dataframe = None
    
    m3_pattern = re.compile(r'M3\s+-\s+Trial registry record', re.MULTILINE)
    a1_pattern = re.compile(r'A1\s+-\s+(.*)', re.MULTILINE)
    try:
        central = data.split("ER  -")[:-1]
        st.write(f"🎉 Successfully parsed **{len(central)}** records.")               
        CENTRAL_Dataframe = RIS_To_DataFrame (data)
        CENTRAL_Dataframe['Note'] = CENTRAL_Dataframe['Note'].str.strip()
        CENTRAL_Dataframe['Note'] = CENTRAL_Dataframe['Note'].str.lower()
        central_ids = []
        central_non_trials = []
        for idx,record in enumerate(CENTRAL_Dataframe['Note']):
            if record == "trial registry record":
                central_ids.append (CENTRAL_Dataframe['Author'][idx].strip())
            else:
                central_non_trials.append(CENTRAL_Dataframe['Acession_Number'][idx].strip())
        if central_ids:
            central_ids = list (set(central_ids))
            filtered_CENTRAL_Dataframe = CENTRAL_Dataframe[CENTRAL_Dataframe['Author'].isin(central_ids)]
            st.session_state['Central_IDs'] = central_ids
            st.session_state['Central_df'] =  filtered_CENTRAL_Dataframe
            st.write(f"🎉 Successfully identified **{len(central_ids)}** unique trial records.")
            # return filtered_CENTRAL_Dataframe
            
        else:
            st.warning("No trial records were identified. Please double check the uploaded data.")
        if central_non_trials:
            central_non_trials = list (set(central_non_trials))
            filtered_CENTRAL_non_trials_Dataframe = CENTRAL_Dataframe[CENTRAL_Dataframe['Acession_Number'].isin(central_non_trials)]
            st.session_state['Central_non_trials_IDs'] = central_non_trials
            st.session_state['Central_non_trials_df'] =  filtered_CENTRAL_non_trials_Dataframe

        return filtered_CENTRAL_Dataframe,filtered_CENTRAL_non_trials_Dataframe
            # uploaded_ris_file1.seek(0) 
    except Exception as e:
        st.error(f"Error reading RIS file. Please check the uploaded data.")


def Embase_Parse (data):
    filtered_EMBASE_Dataframe = None
    filtered_EMBASE_non_trials_Dataframe = None
    db_pattern = re.compile(r'DB\s+-\s+Embase Clinical Trials',re.MULTILINE)
    jf_pattern = re.compile(r'JF\s+-\s+clinicaltrials.gov',re.MULTILINE)
    an_pattern = re.compile(r'AN\s+-\s+(.*)', re.MULTILINE)
    id_pattern = re.compile(r'U2  - L(.*)', re.MULTILINE)
    # create embase ids list
    try:
        embase = data.split("ER  -")[:-1]
        st.write(f"🎉 Successfully parsed **{len(embase)}** records.")
        EMBASE_Dataframe = RIS_To_DataFrame (data)
        
        EMBASE_Dataframe['Database'] = EMBASE_Dataframe['Database'].astype(str).str.strip()
        EMBASE_Dataframe['Database'] = EMBASE_Dataframe['Database'].astype(str).str.lower()
        
        embase_ids = []
        embase_non_trials = []
        for record in EMBASE_Dataframe.itertuples():
            idx = record.index
            if record.Database == "embase clinical trials":
                embase_ids.append (record.Acession_Number)
            elif record.Note == 'Clinical Trial': 
                embase_ids.append (record.Acession_Number)
            else:
                embase_non_trials.append(record.Acession_Number)      
        if embase_ids:
            embase_ids = list (set(embase_ids))
            filtered_EMBASE_Dataframe = EMBASE_Dataframe[EMBASE_Dataframe['Acession_Number'].isin(embase_ids)].reset_index(drop=True)
            embase_urls = []
            year_cleaned = []
            for idx in range(len(filtered_EMBASE_Dataframe)):
                url_splited = filtered_EMBASE_Dataframe['URL'][idx].split("; ")
                if len (url_splited)>= 1:
                    embase_urls.append (url_splited[0])
                else: 
                    embase_urls.append (url_splited)
            filtered_EMBASE_Dataframe['URL'] = embase_urls 
            filtered_EMBASE_Dataframe['Year'] = filtered_EMBASE_Dataframe['Year'].str.rstrip('//')
            filtered_EMBASE_Dataframe['Acession_Number'] = filtered_EMBASE_Dataframe['Acession_Number'].str.replace(r'^L', '', regex=True)
            st.session_state['Embase_IDs'] = embase_ids
            st.session_state['Embase_df'] =  filtered_EMBASE_Dataframe
            st.write(f"🎉 Successfully identified **{len(embase_ids)}** unique trial records.")
            # return filtered_EMBASE_Dataframe
        else:
            st.warning("No trial records were identified. Please check the uploaded data.")

        if embase_non_trials:
            embase_non_trials = list (set(embase_non_trials))
            filtered_EMBASE_non_trials_Dataframe = EMBASE_Dataframe[EMBASE_Dataframe['Acession_Number'].isin(embase_non_trials)]
            st.session_state['Embase_non_trials_IDs'] = embase_non_trials
            st.session_state['Embase_non_trials_df'] =  filtered_EMBASE_non_trials_Dataframe
        return filtered_EMBASE_Dataframe,filtered_EMBASE_non_trials_Dataframe
    except Exception as e:
        st.error(f"Error reading RIS file. Please check the uploaded data.")

    

def ClinicalTrialsGov_Parse (data):
    try:
        df_ct = data
        ct_ids = []
        for i in df_ct['NCT Number']:
            ct_ids.append(str(i).strip())
        ct_ids_final = list(set(ct_ids))
        if ct_ids_final:
            st.session_state['CT_IDs'] = ct_ids_final
            st.session_state['CT_df'] =  df_ct
            st.write(f"🎉 Successfully parsed **{(df_ct.shape[0])}** records.")
            st.write(f"🎉 Successfully identified **{len(ct_ids_final)}** unique trial records.")
            
            return df_ct
            
        else:
            st.warning("No trial records were identified from ClinicalTrials.gov.")
    except Exception as e:
        st.error(f"Error reading CSV file. Please check the uploaded data.")

def WHO_ICTRP_Parse (data):
    try:
        df_ictrp = data
        df_ictrp['TrialID'] = df_ictrp['TrialID'].str.strip()
        # create ictrp ids list
        ictrp_ids = []
        for i in df_ictrp['TrialID']:
            ictrp_ids.append(str(i).strip())
        ictrp_ids_final = list(set(ictrp_ids))
        if ictrp_ids_final:
            st.session_state['ICTRP_IDs'] = ictrp_ids_final
            st.session_state['ICTRP_df'] =  df_ictrp
            st.write(f"🎉 Successfully parsed **{(df_ictrp.shape[0])}** records.")
            st.write(f"🎉 Successfully identified **{len(ictrp_ids_final)}** unique trial records.")
            return df_ictrp
        else:
            st.warning("No trial records were identified from WHO ICTRP.")
            
    except Exception as e:
        st.error(f"Error reading XML file. Please check the uploaded data.")


def ScanMedicine_Parse (data):
    try:
        df_scanmedicine = data
        # create scanmedicine ids list
        scanmedicine_ids = []
        for i in df_scanmedicine['MainID']:
            scanmedicine_ids.append(str(i).strip())
        scanmedicine_ids_final = list(set(scanmedicine_ids))
        if scanmedicine_ids_final:
            st.session_state['SM_IDs'] = scanmedicine_ids_final
            st.session_state['SM_df'] =  df_scanmedicine
            st.write(f"🎉 Successfully parsed **{(df_scanmedicine.shape[0])}** records.")
            st.write(f"🎉 Successfully identified **{len(scanmedicine_ids_final)}** unique trial records.")
            return df_scanmedicine
            
        else:
            st.warning("No trial records were identified from ScanMedicine.")
    except Exception as e:
        st.error(f"Error reading CSV file. Please check the uploaded data.")  
        
    