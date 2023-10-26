import streamlit as st
import pandas as pd

modality_list = [
        '0_1', '0_2', '0_3',
        '0_4', '0_5', '0_6',
        '0_7', '0_8', '0_9',
        '1', 'sequential'
        ]

C_dict = {
            '0_1': 0.1,
            '0_2': 0.2,
            '0_3': 0.3,
            '0_4': 0.4,
            '0_5': 0.5,
            '0_6': 0.6,
            '0_7': 0.7,
            '0_8': 0.8,
            '0_9': 0.9,
            '1':1,
            'sequential':'sequential'
        }

def write_per_slice_results(data, metric):

    chart = {
        "height": 512,
        "mark": "line",
        "encoding": {
            "x": {
                "field": "slice_index",
                "type": "quantitative",
            }
        },
        "layer": [
        {
            "mark": {
                "type": "line",
                "interpolate": "monotone"
                },
            "encoding":
                {
                    "y": {
                    "field": str(metric),
                    "type": "quantitative",

                    },
                    "color": {"field": "C", "type": "nominal"}

                }
        },
        {
            "mark": {
                "type": "point"
                },
            "encoding":
                {
                    "y": {
                    "field": "annotation_size_mean",
                    "type": "quantitative"
                    },
                    "color":{
                        "condition":{"test":"datum['annotation_size_mean'] < 256", "value":"red"},
                        "value":"green"
                    }

                }
        },

    ],
    "resolve": {"scale": {"y": "independent"}}
    }

    st.vega_lite_chart(
            data,
            chart,
            theme="streamlit",
            use_container_width=True
        )

### Make full width
st.set_page_config(layout="wide")

### CSS
st.sidebar.title('Per-Patient Results')

experiment_folder_names = ['6_percent_measurements', '25_percent_measurements']

experiment_folder_name = st.sidebar.selectbox(
    'Select Experiment Type',
    experiment_folder_names
    )

metric = st.sidebar.selectbox(
    'Select Metric',
    ['BCE_loss', 'PSNR_loss', 'TP', 'FP', 'TN', 'FN', 'Specificity', 'Sensitivity', 'DICE']
    )

result_patients_data = pd.concat([pd.read_csv(f'./new_processed_results/{experiment_folder_name}/lpd_unet_{c}.csv') for c in modality_list])
unique_patients_ids = result_patients_data['patient_index'].unique()

patient_id = st.sidebar.selectbox(
    'Select Patient Focus',
    unique_patients_ids
    )

col_2, col_3 = st.columns(2)
result_patient_data = result_patients_data[result_patients_data['patient_index'] == patient_id]
rows_with_annotation = result_patient_data[~result_patient_data["n_annotations"].isna()]
slices_with_annotation = rows_with_annotation["slice_index"].unique()

with col_2:
    write_per_slice_results(result_patient_data, metric)

with col_3:
    st.subheader(f'Slices with annotations: ')
    st.text(f'{slices_with_annotation}')
    st.subheader(f'Average {metric} on slices with annotation')
    for c_value in modality_list:
        st.text(f'C = {c_value} : {rows_with_annotation[rows_with_annotation["C"] == C_dict[c_value]][metric].mean()}')