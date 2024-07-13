import streamlit as st
import pandas as pd
import plotly.express as px

# Load CSV files
patients_df = pd.read_csv('patient_cleaned.csv')
encounters_df = pd.read_csv('encounters_cleaned.csv')
organizations_df = pd.read_csv('organizations_cleaned.csv')
payers_df = pd.read_csv('payers_cleaned.csv')
procedures_df = pd.read_csv('procedures_cleaned.csv')

# Function to get patient info
def get_patient_info(patient_id):
    patient_info = patients_df[patients_df['Id'] == patient_id]
    encounter_info = encounters_df[encounters_df['PATIENT'] == patient_id]
    encounter_info = encounter_info.merge(organizations_df, left_on='ORGANIZATION', right_on='Id', suffixes=('_encounter', '_organization'))
    encounter_info = encounter_info.merge(payers_df, left_on='PAYER', right_on='Id', suffixes=('', '_payer'))
    procedure_info = procedures_df[procedures_df['PATIENT'] == patient_id]
    
    return patient_info, encounter_info, procedure_info

# Streamlit app
st.title('Patient Information Viewer')

# Sidebar for patient selection by ID
st.sidebar.header("Search Patient")
search_query = st.sidebar.text_input("Enter patient name or ID:")

# Filter patients based on search query
if search_query:
    filtered_patients = patients_df[
        patients_df['Id'].str.contains(search_query, case=False) |
        patients_df['FIRST'].str.contains(search_query, case=False) |
        patients_df['LAST'].str.contains(search_query, case=False)
    ]
    patient_selection = st.sidebar.selectbox(
        'Select Patient by ID',
        filtered_patients['Id'] + " - " + filtered_patients['FIRST'] + " " + filtered_patients['LAST']
    )
else:
    patient_selection = st.sidebar.selectbox(
        'Select Patient by ID',
        patients_df['Id'] + " - " + patients_df['FIRST'] + " " + patients_df['LAST']
    )

# Extract selected patient's ID
selected_patient_id = patient_selection.split(" - ")[0]

# Sidebar for patient selection by first name
first_name_selection = st.sidebar.selectbox(
    'Select Patient by First Name',
    patients_df['FIRST'].unique()
)

# Get patient info based on first name
if first_name_selection:
    patient_info_by_name = patients_df[patients_df['FIRST'] == first_name_selection]
    selected_patient_id_by_name = patient_info_by_name.iloc[0]['Id']
    patient_info_by_name, encounter_info_by_name, procedure_info_by_name = get_patient_info(selected_patient_id_by_name)


   
# Get patient info by ID
patient_info, encounter_info, procedure_info = get_patient_info(selected_patient_id)

# Display patient information
st.header('Patient Information')
st.write(patient_info)

st.header('Encounter Information')
st.write(encounter_info)

st.header('Procedure Information')
st.write(procedure_info)

