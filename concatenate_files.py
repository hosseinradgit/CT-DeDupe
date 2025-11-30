import pandas as pd
import streamlit as st

def concatenate_files(uploaded_files, data_type): #data type could be csv or xml or ris
        """Reads and concatenates a list of uploaded CSV or XML  or RIS files."""
        if not uploaded_files:
            return None
        all_dfs = []
        full_ris_text = ""    
        for file in uploaded_files:
            try:
                if data_type == 'csv':
                    df = pd.read_csv(file)
                    all_dfs.append(df)
                elif data_type == 'xml':
                    df = pd.read_xml(file,parser='etree')
                    all_dfs.append(df)
                elif data_type == 'ris':
                    # Read the content of the file
                    ris_content = file.read().decode("utf-8")
                    # Concatenate the content using the + operator
                    full_ris_text += ris_content + "\n"
            except Exception as e:
                st.error(f"Error reading {file.name}: {e}")
                return None

        if data_type == 'ris':
            return full_ris_text
        try:
            concatenated_df = pd.concat(all_dfs, ignore_index=True)
            return concatenated_df
        except Exception as e:
            st.error(f"Error concatenating files: {e}")
            return None



        

