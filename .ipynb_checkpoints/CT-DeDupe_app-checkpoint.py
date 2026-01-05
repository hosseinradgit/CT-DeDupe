
import streamlit as st
import pandas as pd
import numpy as np
import re
from file_convertor import *
from concatenate_files import *
from Import_data import *

st.set_page_config(
    page_title="Clinical Trial Deduplicator",
    page_icon="",
    layout="centered"
)
 
st.title("Clinical Trials Deduplicator")
st.subheader("CT-DeDupe (Beta)")
st.markdown(" ") 

# Tabs for the main content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Data Preview", "Auto-Deduplication", "Manual-Deduplication", "Export Data"])
with tab1:
    st.markdown("""
    ### Overview
    This tool is designed to remove duplicate Clinical Trials records from Cochrane CENTRAL, Embase, ClinicalTrials.gov, WHO ICTRP, and ScanMedicine. After uploading your data to the designated section for each source, you can download clean, de-duplicated data for each source.
    
    ### Using this tool
    
    1. **Upload Data**: Navigate to the "Upload Data" section in the sidebar, and then select the file you want to upload. You can upload multiple data files for each source.
    
    2. **Data Preview**: To view the data, click preview data under each source. The data will appear in the 'Data Preview' tab.

    3. **Auto-Deduplication**: Review the records that were automatically identified as duplicates.

    4. **Manual-Deduplication**: Manually review the records to identify any additional duplicates.
    
    3. **Export Data**: Download the cleaned data in the 'Export Data' tab.

    #### Developer & Contact Information
    
    This tool was developed as part of the project, Global Alliance for Living Evidence on aNxiety, depressiOn and pSychosis (GALENOS) by Hossein Dehdarirad, Research Fellow and Information Scientist at EPPI Center, University College London. For any questions, please contact h.dehdarirad@ucl.ac.uk.
    
    """) 
# Initialize session state for data storage and display control
if 'data_to_display' not in st.session_state:
    st.session_state.data_to_display = None
if 'central_data' not in st.session_state:
    st.session_state.central_data = None
if 'central_non_trials_data' not in st.session_state:
    st.session_state.central_non_trials_data = None
if 'embase_data' not in st.session_state:
    st.session_state.embase_data = None
if 'embase_non_trials_data' not in st.session_state:
    st.session_state.embase_non_trials_data = None
if 'ct_data' not in st.session_state:
    st.session_state.ct_data = None
if 'ictrp_data' not in st.session_state:
    st.session_state.ictrp_data = None
if 'scanmedicine_data' not in st.session_state:
    st.session_state.scanmedicine_data = None

def set_data_to_preview(source_key):
    st.session_state.data_to_display = source_key
    
def clear_preview():
    st.session_state.data_to_display = None


def Cochrane_state():
    st.session_state['Central_IDs'] = []
    st.session_state['Central_df'] =  None
    st.session_state['Central_non_trials_IDs'] = []
    st.session_state['Central_non_trials_df'] =  None

def Embase_state():
    st.session_state['Embase_IDs'] = []
    st.session_state['Embase_df'] =  None
    st.session_state['Embase_non_trials_IDs'] = []
    st.session_state['Embase_non_trials_df'] = None

def ClinicalTirals_state():
    st.session_state['CT_IDs'] = []
    st.session_state['CT_df'] =  None

def WHO_ICTRP_state():
    st.session_state['ICTRP_IDs'] = []
    st.session_state['ICTRP_df'] =  None

def ScanMedicine_state():
    st.session_state['SM_IDs'] = []
    st.session_state['SM_df'] =  None



with st.sidebar:
    st.title("Upload Data")
    # Section 1: Cochrane CENTRAL
    st.subheader("1. Cochrane Central")
    uploaded_central_ris = st.file_uploader(
        "Choose your RIS file...",
        type=["ris"],
        key="ris_uploader1",
        accept_multiple_files=True,
        on_change=Cochrane_state
    )
    if uploaded_central_ris:
        # st.success("Data uploaded successfully!")
        full_central_ris = concatenate_files (uploaded_central_ris, 'ris')
        if full_central_ris:
            # st.write(CENTRAL_Parse(full_central_ris))
            st.session_state.central_data,st.session_state.central_non_trials_data = CENTRAL_Parse(full_central_ris)

            st.button(
                "Preview Central Data", 
                key="central_preview_btn", 
                on_click=set_data_to_preview, 
                args=['central_data'] # Pass the key for the data
            )
            

    st.markdown("---") 
    
    # Section 2: Embase data
    st.subheader("2. Embase")
    uploaded_embase_ris = st.file_uploader(
        "Choose your RIS file...",
        type=["ris"],
        key="ris_uploader2",
        accept_multiple_files=True,
        on_change=Embase_state
    )
    if uploaded_embase_ris:
        # st.success("Data uploaded successfully!")
        full_embase_ris = concatenate_files (uploaded_embase_ris, 'ris')
        if full_embase_ris:
            # st.session_state.embase_data = Embase_Parse(full_embase_ris)
            st.session_state.embase_data,st.session_state.embase_non_trials_data = Embase_Parse(full_embase_ris)
            st.button(
                "Preview Embase Data",
                key="embase_preview_btn", 
                on_click=set_data_to_preview, 
                args=['embase_data']
            )

    st.markdown("---")     
    # ClinicalTrials.gov data
    st.subheader("3. ClinicalTrials.gov")
    ClinicalTrialsGov = st.file_uploader(
        "Choose your CSV file...",
        type=["csv"],
        key="csv_uploader1",
        accept_multiple_files=True,
        on_change=ClinicalTirals_state
    )
    if ClinicalTrialsGov:
        # st.success("Data uploaded successfully!")
        df_ct = concatenate_files (ClinicalTrialsGov, 'csv')
        
        if df_ct.shape[0]:
            st.session_state.ct_data = ClinicalTrialsGov_Parse(df_ct)
            st.button(
                "Preview ClinicalTrials Data",
                key="ct_preview_btn", 
                on_click=set_data_to_preview, 
                args=['ct_data']
            )


    st.markdown("---")     
    # WHO ICTRP data
    st.subheader("4. WHO ICTRP")
    WHO_ICTRP_XML = st.file_uploader(
        "Choose your XML file...",
        type=["xml"],
        key="xml_uploader",
        accept_multiple_files=True,
        on_change=WHO_ICTRP_state
    )
    if WHO_ICTRP_XML:
        # st.success("Data uploaded successfully!")
        df_ictrp = concatenate_files (WHO_ICTRP_XML, 'xml')
        # st.write(f"🎉 Successfully parsed **{(df_ictrp.shape[0])}** records.")
        if df_ictrp.shape[0]:
            st.session_state.ictrp_data = WHO_ICTRP_Parse(df_ictrp)
            st.button(
                "Preview WHO ICTRP Data",
                key="ictrp_preview_btn", 
                on_click=set_data_to_preview, 
                args=['ictrp_data']
            )
    

    
    st.markdown("---")     
    # ScanMedicine data
    st.subheader("5. ScanMedicine")
    ScanMedicine_csv = st.file_uploader(
        "Choose your CSV file...",
        type=["csv"], 
        key="csv_uploader2",
        accept_multiple_files=True,
        on_change=ScanMedicine_state
    )
    if ScanMedicine_csv:
        # st.success(f"Data uploaded successfully!")
        df_scanmedicine = concatenate_files (ScanMedicine_csv, 'csv')
        
        if df_scanmedicine.shape[0]:
            st.session_state.scanmedicine_data = ScanMedicine_Parse(df_scanmedicine)
            st.button(
                "Preview ScanMedicine Data",
                key="scanmedicine_preview_btn", 
                on_click=set_data_to_preview, 
                args=['scanmedicine_data']
            )


    
    with tab3:
        # Central data and ids
        if 'Central_IDs' in st.session_state:
            central_ids = st.session_state['Central_IDs']
        else: 
            central_ids = []
        if 'Central_df' in st.session_state:
            central = st.session_state['Central_df']
        else: 
            central = None
        if 'Central_non_trials_IDs' in st.session_state:
            central_non_trials_ids = st.session_state['Central_non_trials_IDs']
        else:
            central_non_trials_ids = []
        if 'Central_non_trials_df' in st.session_state:
            central_non_trials_df = st.session_state['Central_non_trials_df']
        else: 
            central_non_trials_df = None
        ## embase data and ids
        if 'Embase_IDs' in st.session_state:
            embase_ids = st.session_state['Embase_IDs']
        else: 
            embase_ids = []
        if 'Embase_df' in st.session_state:
            embase = st.session_state['Embase_df']
        else: 
            embase = None

        if 'Embase_non_trials_IDs' in st.session_state:
            embase_non_trials_ids = st.session_state['Embase_non_trials_IDs']
        else:
            embase_non_trials_ids = []

        if 'Embase_non_trials_df' in st.session_state:
            embase_non_trials_df = st.session_state['Embase_non_trials_df']

        else:
            embase_non_trials_df = None
        
        ## ClinicalTirals.gov data and ids
        if 'CT_IDs' in st.session_state: 
            ct_ids_final = st.session_state['CT_IDs']
        else:
            ct_ids_final = []
        if 'CT_df' in st.session_state:
            ct = st.session_state['CT_df']
        else: 
            ct = None
            
        ## WHO ICTRP data and ids
        if 'ICTRP_IDs' in st.session_state:
            ictrp_ids_final = st.session_state['ICTRP_IDs']
        else: 
            ictrp_ids_final = []
        if 'ICTRP_df' in st.session_state:
            ictrp = st.session_state['ICTRP_df']
        else: 
            ictrp = None
        
        ## ScanMedidince data and ids
        if 'SM_IDs' in st.session_state:
            scanmedicine_ids_final = st.session_state['SM_IDs']
        else: 
            scanmedicine_ids_final = []
        if 'SM_df' in st.session_state:
            scanmedicine = st.session_state['SM_df']
        else: 
            scanmedicine = None
        dfs = []
        if isinstance(central, pd.DataFrame):
            central_subset = central[['Author', 'Title', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number', 'Source','Volume','Issue']]
            # central_subset = central_subset.rename(columns={'Author': 'Trial_ID'})
            central_subset['Trial_ID'] = central['Author'].str.strip()
            central_subset['Database'] = 'CENTRAL'
            central_subset['Source_Code'] = 1
            new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue', 'Database','Source_Code']
            central_subset = central_subset[new_order]
            dfs.append (central_subset)           
        
        if isinstance(ct, pd.DataFrame):
            ct['NCT Number'] = ct['NCT Number'].str.strip()
            ct_subset = ct[['NCT Number']]
            ct_subset['Author'] = ct_subset['NCT Number']
            targeted_tags = ['Study Title', 'First Posted', 'Study URL', "Brief Summary", "Primary Outcome Measures","Secondary Outcome Measures", "Study Status"]
            for tag in targeted_tags:
                if tag in ct.columns:
                    ct_subset[tag] = ct[tag]
                else:
                    ct_subset[tag] = ""
            ct_subset['Note'] = "Study Status: " + ct_subset["Study Status"].fillna('').astype(str) + " " + "OUTCOMS: "+ ct_subset["Primary Outcome Measures"].fillna('').astype(str) + " " + ct_subset["Secondary Outcome Measures"].fillna('').astype(str)
            ct_subset['Acession_Number'] = ct_subset['NCT Number']
            ct_subset['Keywords'] = ""
            ct_subset = ct_subset.rename(columns={'NCT Number': 'Trial_ID', 'Study Title': 'Title', "Brief Summary":'Abstract','First Posted':'Year', 'Study URL':'URL'})
            ct_subset['Year'] = ct_subset['Year'].str.extract(r'(^[0-9]{4})')
            ct_subset['Database'] = 'ClinicalTrialsGov'
            ct_subset['Source_Code'] = 2
            ct_subset['Source'] = "ClinicalTrials.gov"
            ct_subset['Volume'] = ""
            ct_subset['Issue'] = ""
            new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue', 'Database','Source_Code']
            ct_subset = ct_subset[new_order]
            # st.write(ct_subset)
            dfs.append (ct_subset)

        if isinstance(embase, pd.DataFrame):
            embase_subset = embase[['Author', 'Title', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number', 'Source','Volume','Issue']]
            # embase_subset = embase_subset.rename(columns={'Acession_Number': 'Trial_ID'})
            embase_subset['Trial_ID'] = embase['Acession_Number'].str.strip()
            embase_subset['Database'] = 'EMBASE'
            embase_subset['Source_Code'] = 3
            new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue', 'Database','Source_Code']
            embase_subset = embase_subset[new_order]
            # st.write(embase_subset)
            dfs.append (embase_subset)

        
        if isinstance(ictrp, pd.DataFrame):
            ictrp['TrialID'] = ictrp['TrialID'].str.strip()
            ictrp_subset = ictrp[['TrialID']]
            ictrp_subset['Author'] = ictrp_subset['TrialID'].str.strip()
            targeted_tags = ['Public_title', 'Date_registration', 'web_address', "Recruitment_Status", "Condition", "Intervention", "Primary_outcome", "Secondary_outcome", "Inclusion_Criteria", "Countries", "Scientific_title", "Internal_Number"]
            for tag in targeted_tags:
                if tag in ictrp.columns:
                    ictrp_subset[tag] = ictrp[tag]
                else:
                    ictrp_subset[tag] = ""
            ictrp_subset['Abstract'] = 'INTERVENTION: '+ ictrp_subset['Intervention'].fillna('').astype(str) + ' CONDITION: ' + ictrp_subset['Condition'].fillna('').astype(str) + " PRIMARY OUTCOME: " + ictrp_subset['Primary_outcome'].fillna('').astype(str) + " SECONDARY OUTCOME: " + ictrp_subset['Secondary_outcome'].fillna('').astype(str) + " INCLUSION CRITERIA: " + ictrp_subset['Inclusion_Criteria'].fillna('').astype(str)
            ictrp_subset['Note'] = "Scientific title: " + ictrp_subset["Scientific_title"].fillna('').astype(str) + " Recruitment_Status:" +  ictrp_subset["Recruitment_Status"].fillna('').astype(str) + " Country: " + ictrp_subset["Countries"].fillna('').astype(str)
            ictrp_subset['Keywords'] = ""
            ictrp_subset['Acession_Number'] = ictrp_subset['Internal_Number']
            ictrp_subset = ictrp_subset.rename(columns={'TrialID': 'Trial_ID', 'Public_title': 'Title', 'Date_registration':'Year', 'web_address':'URL'})
            ictrp_subset['Year'] = ictrp_subset['Year'].str.extract(r'([0-9]{4})')
            ictrp_subset['Database'] = 'WHO_ICTRP'
            ictrp_subset['Source'] = "WHO ICTRP"
            ictrp_subset['Volume'] = ""
            ictrp_subset['Issue'] = ""
            ictrp_subset['Source_Code'] = 4
            new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number', 'Volume','Issue', 'Database','Source_Code']
            ictrp_subset = ictrp_subset[new_order]
            dfs.append (ictrp_subset)

        
        if isinstance(scanmedicine, pd.DataFrame):
            scanmedicine['MainID'] = scanmedicine['MainID'].str.strip()
            scanmedicine_subset = scanmedicine[['MainID']]
            scanmedicine_subset['Author'] = scanmedicine_subset['MainID'].str.strip()
            targeted_tags = ['PublicTitle', 'DateOfRegistration', 'DocURL', "TrialStatus", "HealthConditionOrProblemStudied", "Interventions", "PrimaryOutcomes", "InclusionCriteria", "SecondaryOutcomes", "CountriesOfRecruitment", "ScientificTitle"]
            for tag in targeted_tags:
                if tag in scanmedicine.columns:
                    scanmedicine_subset[tag] = scanmedicine[tag]
                else:
                    scanmedicine_subset[tag] = ""

            scanmedicine_subset['Abstract'] = 'INTERVENTION: '+ scanmedicine_subset['Interventions'].fillna('').astype(str) + ' CONDITION: ' + scanmedicine_subset['HealthConditionOrProblemStudied'].fillna('').astype(str) + " PRIMARY OUTCOME: " + scanmedicine_subset['PrimaryOutcomes'].fillna('').astype(str) + " SECONDARY OUTCOME: " + scanmedicine_subset['SecondaryOutcomes'].fillna('').astype(str) + " INCLUSION CRITERIA: " + scanmedicine_subset['InclusionCriteria'].fillna('').astype(str)
            scanmedicine_subset['Note'] = "Scientific title: " + scanmedicine_subset["ScientificTitle"].fillna('').astype(str) + " TrialStatus:" +  scanmedicine_subset["TrialStatus"].fillna('').astype(str) + " Country: " + scanmedicine_subset["CountriesOfRecruitment"].fillna('').astype(str)
            scanmedicine_subset['Keywords'] = ""
            scanmedicine_subset['Acession_Number'] = scanmedicine_subset['MainID']
            scanmedicine_subset = scanmedicine_subset.rename(columns={'MainID': 'Trial_ID', 'PublicTitle': 'Title', 'DateOfRegistration':'Year', 'DocURL':'URL'})
            scanmedicine_subset['Year'] = scanmedicine_subset['Year'].str.extract(r'(^[0-9]{4})')
            scanmedicine_subset['Database'] = 'ScanMedicine'
            scanmedicine_subset['Source'] = 'ScanMedicine'
            scanmedicine_subset['Volume'] = ""
            scanmedicine_subset['Issue'] = ""
            scanmedicine_subset['Source_Code'] = 5
            new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue', 'Database','Source_Code']
            scanmedicine_subset = scanmedicine_subset[new_order]
            dfs.append(scanmedicine_subset)

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            # st.write(combined_df)
            sorted_df = combined_df.sort_values(by=['Trial_ID', 'Source_Code'],ascending=[True, True]).reset_index(drop=True)
            sorted_df['Status'] = np.where(sorted_df.groupby('Trial_ID').cumcount() == 0,  'Primary', 'Duplicate')
            def color_priority(row):
                if row['Status'] == 'Primary':
                    # Apply a light green background to the entire row
                    return ['background-color: #e6ffe6'] * len(row)
                elif row['Status'] == 'Duplicate':
                    # Apply a light red background to the entire row
                    return ['background-color: #ffe6e6'] * len(row)
                return [''] * len(row)
            sliced_df = sorted_df.iloc[:100]
            styled_df = sliced_df.style.apply(color_priority, axis=1)
            st.write(styled_df)
            st.session_state['sorted_df'] = sorted_df
            def convert_df_to_csv(df):
                return df.to_csv(index=False).encode('utf-8')
            dfs_to_download = convert_df_to_csv(sorted_df)
            st.download_button(
                label="Download Data",
                data=dfs_to_download,
                file_name='Duplicate Records.csv',
                mime='text/csv')


    with tab4:
        if 'sorted_df' in st.session_state:
            sorted_df = st.session_state['sorted_df']
        else: 
            sorted_df = []
    
        if isinstance(sorted_df, pd.DataFrame):
            primary_ids = sorted_df[sorted_df['Status'] == 'Primary']['Trial_ID'].unique()
            primary_records_df = sorted_df[sorted_df['Status'] == 'Primary']
            primary_records_df['Title'] = primary_records_df['Title'].str.strip()
            primary_records_df['Title'] = primary_records_df['Title'].str.lower()
            primary_records_df['Year'] = primary_records_df['Year'].str.strip()
            duplicate_mask_ = primary_records_df.duplicated(subset=['Title', 'Year'], keep=False)
            duplicate_mask_df = primary_records_df[duplicate_mask_].copy()
            duplicate_mask_df = duplicate_mask_df.sort_values(by=['Title', 'Year'], ascending=True)
            duplicate_mask_df.insert(0, 'Delete?', False, allow_duplicates=False)
            edited_df = st.data_editor(
                    duplicate_mask_df,
                    column_config={"Delete?": st.column_config.CheckboxColumn(required=True)},
                    hide_index=True)
            if st.button("Remove Checked Records"):
                rows_to_remove = edited_df[edited_df['Delete?'] == True]
                unwanted_values = list (rows_to_remove['Trial_ID'])
                rows_to_drop = primary_records_df['Trial_ID'].isin(unwanted_values)
                primary_records_df = primary_records_df[~rows_to_drop]
                st.session_state['primary_ids'] = primary_ids
                st.session_state['primary_records_df'] = primary_records_df
                st.warning (f"⚠️ {len(rows_to_remove)} record(s) removed from the dataset and Export Data tab updated.")

    with tab5:
        if 'primary_ids' in st.session_state and 'primary_records_df' in st.session_state:
            primary_ids = st.session_state['primary_ids']
            primary_records_df = st.session_state['primary_records_df']
            st.subheader("Data Summary")
            summary_table = pd.pivot_table(primary_records_df, 
                                         index='Database',
                                         columns='Status', 
                                         values='Trial_ID',
                                         aggfunc='count', 
                                         fill_value=0 )
            st.write(summary_table
            )
            st.markdown("---")  
            st.subheader("Export Data")
            
            for database in summary_table.index:
                st.write(database)
                data_to_export = primary_records_df[primary_records_df['Database'] == database]               
                col1, col2 = st.columns(2)
                if database == 'CENTRAL':
                    if isinstance(central_non_trials_df, pd.DataFrame):
                        central_non_trials_df_subset = central_non_trials_df[['Author', 'Title', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue','Source']]
                        central_non_trials_df_subset['Trial_ID'] = ''
                        central_non_trials_df_subset['Database'] = 'CENTRAL'
                        central_non_trials_df_subset['Source_Code'] = 1
                        new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue','Database','Source_Code']
                        central_non_trials_df_subset = central_non_trials_df_subset[new_order]
                        data_to_export_central = pd.concat([data_to_export, central_non_trials_df_subset], ignore_index=True)
                        csv_data = convert_df_to_csv(data_to_export_central)
                        ris_data = convert_df_to_ris(data_to_export) + convert_non_trial_df_to_ris (central_non_trials_df_subset)
                    else:
                        csv_data = convert_df_to_csv(data_to_export)
                        ris_data = convert_df_to_ris(data_to_export)

                elif database == 'EMBASE':
                    if isinstance(embase_non_trials_df, pd.DataFrame):
                        embase_non_trials_df_subset = embase_non_trials_df[['Author', 'Title', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue','Source']]
                        embase_non_trials_df_subset['Trial_ID'] = ''
                        embase_non_trials_df_subset['Database'] = 'EMBASE'
                        embase_non_trials_df_subset['Source_Code'] = 3
                        new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue','Database','Source_Code']
                        embase_non_trials_df_subset = embase_non_trials_df_subset[new_order]
                        data_to_export_embase = pd.concat([data_to_export, embase_non_trials_df_subset], ignore_index=True)
                        csv_data = convert_df_to_csv(data_to_export_embase)
                        ris_data = convert_df_to_ris(data_to_export) + convert_non_trial_df_to_ris (embase_non_trials_df_subset)
                    else:
                        csv_data = convert_df_to_csv(data_to_export)
                        ris_data = convert_df_to_ris(data_to_export)
                else:
                    csv_data = convert_df_to_csv(data_to_export)
                    ris_data = convert_df_to_ris(data_to_export)
                with col1:
                    st.download_button(
                        label="Export as CSV",
                        data=csv_data,
                        file_name=f'{database}.csv',
                        mime='text/csv',
                        key=f'csv_download_{database}'
                    )
                # # RIS Download Button
                # ris_data = convert_df_to_ris(data_to_export)
                
                with col2:
                    st.download_button(
                        label="Export as RIS",
                        data=ris_data,
                        file_name=f'{database}.ris',
                        mime='text/RIS',
                        key=f'ris_download_{database}'
                    )
            
        else: 
            if isinstance(sorted_df, pd.DataFrame):
                st.subheader("Data Summary")
                summary_table = pd.pivot_table(sorted_df, 
                                             index='Database',
                                             columns='Status', 
                                             values='Trial_ID',
                                             aggfunc='count', 
                                             fill_value=0 )
                st.write(summary_table)
                st.markdown("---") 
                
                st.subheader("Export Data")
                primary_ids = sorted_df[sorted_df['Status'] == 'Primary']['Trial_ID'].unique()
                primary_records_df = sorted_df[sorted_df['Status'] == 'Primary']
                
                for database in summary_table.index:
                    data_to_export = primary_records_df[primary_records_df['Database'] == database]
                    st.markdown(f"**{database}**")
                    
                    col1, col2 = st.columns(2)

                    if database == 'CENTRAL':
                        if isinstance(central_non_trials_df, pd.DataFrame):
                            central_non_trials_df_subset = central_non_trials_df[['Author', 'Title', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue', 'Source']]
                            central_non_trials_df_subset['Trial_ID'] = ''
                            central_non_trials_df_subset['Database'] = 'CENTRAL'
                            central_non_trials_df_subset['Source_Code'] = 1
                            new_order = ['Trial_ID','Author', 'Title', 'Source','Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue','Database','Source_Code']
                            central_non_trials_df_subset = central_non_trials_df_subset[new_order]
                            data_to_export_central = pd.concat([data_to_export, central_non_trials_df_subset], ignore_index=True)
                            csv_data = convert_df_to_csv(data_to_export_central)
                            ris_data = convert_df_to_ris(data_to_export) + convert_non_trial_df_to_ris (central_non_trials_df_subset)
                        else:
                            csv_data = convert_df_to_csv(data_to_export)
                            ris_data = convert_df_to_ris(data_to_export)
                    elif database == 'EMBASE':
                        if isinstance(embase_non_trials_df, pd.DataFrame):
                            embase_non_trials_df_subset = embase_non_trials_df[['Author', 'Title', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue','Source']]
                            embase_non_trials_df_subset['Trial_ID'] = ''
                            embase_non_trials_df_subset['Database'] = 'EMBASE'
                            embase_non_trials_df_subset['Source_Code'] = 3
                            new_order = ['Trial_ID','Author', 'Title', 'Source', 'Year', 'URL', 'Abstract','Keywords', 'Note', 'Acession_Number','Volume','Issue','Database','Source_Code']
                            embase_non_trials_df_subset = embase_non_trials_df_subset[new_order]
                            data_to_export_embase = pd.concat([data_to_export, embase_non_trials_df_subset], ignore_index=True)
                            csv_data = convert_df_to_csv(data_to_export_embase)
                            ris_data = convert_df_to_ris(data_to_export) + convert_non_trial_df_to_ris (embase_non_trials_df_subset)
                        else:
                            csv_data = convert_df_to_csv(data_to_export)
                            ris_data = convert_df_to_ris(data_to_export)
                    else:
                        csv_data = convert_df_to_csv(data_to_export)
                        ris_data = convert_df_to_ris(data_to_export)
                    with col1:
                        st.download_button(
                            label="Export as CSV",
                            data=csv_data,
                            file_name=f'{database}.csv',
                            mime='text/csv',
                            key=f'csv_download_{database}'
                        )
                    # RIS Download Button
                    # ris_data = convert_df_to_ris(data_to_export)
                    with col2:
                        st.download_button(
                            label="Export as RIS",
                            data=ris_data,
                            file_name=f'{database}.ris',
                            mime='text/RIS',
                            key=f'ris_download_{database}'
                        )
            

with tab2:
    
    
    source_key = st.session_state.data_to_display
    
    if source_key is not None and st.session_state.get(source_key) is not None:
        data_source_name = ""
        if source_key == 'central_data':
            data_source_name = "Cochrane Central"
        elif source_key == 'embase_data':
            data_source_name = "Embase"
        elif source_key == 'ct_data':
            data_source_name = "ClinicalTrials.gov"
        elif source_key == 'ictrp_data':
            data_source_name = "WHO ICTRP"
        elif source_key == 'scanmedicine_data':
            data_source_name = "ScanMedicine"
    
        st.header(f"Previewing Data from: **{data_source_name}**")
        data_to_show = st.session_state[source_key]
        st.write(data_to_show.iloc[:100])
        
        
        st.button("Clear Preview", on_click=clear_preview, key="hide_preview_btn")
    elif source_key is not None and st.session_state.get(source_key) is None:
        st.warning("No parsed data available to preview for the selected source.")
        
        st.session_state.data_to_display = None
    else:
        st.info("Upload your data in the sidebar and click a 'Preview Data' button to see the data here.")


