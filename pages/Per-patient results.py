import streamlit as st
import pandas as pd

modality_list = [
        '0_1', '0_2', '0_3',
        '0_4', '0_5', '0_6',
        '0_7', '0_8', '0_9',
        '1', 'sequential'
        ]

modality_df_to_display = {
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

modality_display_to_df = {value:key for key, value in modality_df_to_display.items()}

setting_folder_names_df_to_display = {
    '6_percent_measurements':'Sparse-View',
    '25_percent_measurements':'High-Resolution'
    }

setting_folder_display_to_df = {
    'Sparse-View':'6_percent_measurements',
    'High-Resolution':'25_percent_measurements'
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

setting_folder_name_display = st.sidebar.selectbox(
    'Select Setting',
    list(setting_folder_display_to_df.keys())
    )

metric = st.sidebar.selectbox(
    'Select Metric',
    ['BCE_loss', 'PSNR_loss', 'TP', 'FP', 'TN', 'FN', 'Sensitivity', 'DICE']
    )

modality_display = st.sidebar.selectbox(
    'Select Joint Modality, C = ',
    modality_display_to_df
    )

setting_name_df = setting_folder_display_to_df[setting_folder_name_display]


sequential_patient_data = pd.read_csv(f'./new_processed_results/{setting_name_df}/lpd_unet_sequential.csv')
unique_patients_ids = sequential_patient_data['patient_index'].unique()

patient_id = st.sidebar.selectbox(
    'Select Patient Focus',
    unique_patients_ids
    )

modality_patient_data = pd.read_csv(f'./new_processed_results/{setting_name_df}/lpd_unet_{modality_display_to_df[modality_display]}.csv')

complete_patient_data = pd.concat([sequential_patient_data, modality_patient_data])

complete_patient_data = complete_patient_data[complete_patient_data['patient_index'] == patient_id]
rows_with_annotation = complete_patient_data[~complete_patient_data["n_annotations"].isna()]
slices_with_annotation = rows_with_annotation["slice_index"].unique()

write_per_slice_results(complete_patient_data, metric)

