import streamlit as st
import pandas as pd

from utils import plot_per_slice_results
from constants import displays_to_modality

setting_folder_names_df_to_display = {
    '6_percent_measurements':'Sparse-View',
    '25_percent_measurements':'High-Resolution'
    }

setting_folder_display_to_df = {
    'Sparse-View':'6_percent_measurements',
    'High-Resolution':'25_percent_measurements'
    }


### Make full width
st.set_page_config(layout="wide")

### CSS
st.sidebar.title('Refine Selection')

setting_folder_name_display = st.sidebar.selectbox(
    'Select Setting',
    list(setting_folder_display_to_df.keys())
    )

metric = st.sidebar.selectbox(
    'Select Metric',
    ['BCE_loss', 'PSNR_loss', 'TP', 'FP', 'TN', 'FN', 'Sensitivity', 'DICE']
    )

display_mod = st.sidebar.selectbox(
    'Select Joint Modality',
    displays_to_modality
    )

setting_name_df = setting_folder_display_to_df[setting_folder_name_display]

sequential_patient_data = pd.read_csv(f'./new_processed_results/{setting_name_df}/lpd_unet_sequential.csv')
unique_patients_ids = sequential_patient_data['patient_index'].unique()

patient_id = st.sidebar.selectbox(
    'Select Patient Focus',
    unique_patients_ids
    )

st.title(f'Patient {patient_id} Per-Slice Results')

modality_patient_data = pd.read_csv(f'./new_processed_results/{setting_name_df}/{displays_to_modality[display_mod]}.csv')

complete_patient_data = pd.concat([sequential_patient_data, modality_patient_data])

complete_patient_data = complete_patient_data[complete_patient_data['patient_index'] == patient_id]
rows_with_annotation = complete_patient_data[~complete_patient_data["n_annotations"].isna()]
slices_with_annotation = rows_with_annotation["slice_index"].unique()

plot_per_slice_results(complete_patient_data, metric)

