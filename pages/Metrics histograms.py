import streamlit as st

import pandas as pd

from constants import metrics, modality_list, modalities_to_display, displays_to_modality
from utils import write_histogram

### Make full width
st.set_page_config(layout="wide")

### CSS
st.sidebar.title('Histograms')

metric_name = st.sidebar.selectbox(
    'Select Metric',
    metrics
    )

modality = st.sidebar.selectbox(
    'Select modality',
    [modalities_to_display[mod] for mod in modality_list[:-1]]
    )

col_0, col_1 = st.columns(2)

with col_0:
    st.header(f'Sparse-View Results')
    st.subheader(f'Distribution of {metric_name} values for modalitity {modality}')
    path_to_data = f'new_processed_results/6_percent_measurements/{metric_name}_histogram.csv'
    dataframe = pd.read_csv(path_to_data)
    dataframe = dataframe[dataframe['Modality'].isin( [displays_to_modality[modality],'lpd_unet_sequential'])]
    write_histogram(dataframe, metric_name)

with col_1:
    st.header(f'High Angular Resolution Results')
    st.subheader(f'Distribution of {metric_name} values for modalitity {modality}')
    path_to_data = f'new_processed_results/25_percent_measurements/{metric_name}_histogram.csv'
    dataframe = pd.read_csv(path_to_data)
    dataframe = dataframe[dataframe['Modality'].isin([displays_to_modality[modality],'lpd_unet_sequential'])]
    write_histogram(dataframe, metric_name)

