from pathlib import Path
from PIL import Image
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")


st.sidebar.title('Results')

patient_id = st.sidebar.selectbox(
    'Select Patient Id',
    ['LIDC-IDRI-0936']
    )

result_patients_data = pd.read_csv(f'new_processed_results/25_percent_measurements/lpd_unet_sequential.csv')
result_patient_data = result_patients_data[result_patients_data['patient_index'] == patient_id]
rows_with_annotation = result_patient_data[~result_patient_data["n_annotations"].isna()]
slices_with_annotation = rows_with_annotation["slice_index"].unique()

### Image viewer
path_to_image_folder = Path(f'visuels/sequential/{patient_id}')

st.text(f'Slices with annotations: {list(slices_with_annotation)}')

slice_index = st.select_slider(
        'Select a slice to display',
        options=[i for i in range(int(len(list(path_to_image_folder.glob('*')))/4))])

col_0, col_1, col_2 = st.columns(3)

with col_0:
    st.subheader('Reference Images')
    image = Image.open(Path(f'visuels/sequential/{patient_id}/slice_{slice_index}_input.jpg')) #type:ignore
    st.image(image)
    image = Image.open(Path(f'visuels/sequential/{patient_id}/slice_{slice_index}_mask.jpg')) #type:ignore
    st.image(image)

with col_1:
    st.subheader('Joint Approach Results (C=1)')
    image = Image.open(Path(f'visuels/joint/{patient_id}/slice_{slice_index}_reconstruction.jpg')) #type:ignore
    st.image(image)
    image = Image.open(Path(f'visuels/joint/{patient_id}/slice_{slice_index}_segmentation.jpg')) #type:ignore
    st.image(image)

with col_2:
    st.subheader('Sequential Approach Results')
    image = Image.open(Path(f'visuels/sequential/{patient_id}/slice_{slice_index}_reconstruction.jpg')) #type:ignore
    st.image(image)
    image = Image.open(Path(f'visuels/sequential/{patient_id}/slice_{slice_index}_segmentation.jpg')) #type:ignore
    st.image(image)

