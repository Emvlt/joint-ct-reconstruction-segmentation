from pathlib import Path

import streamlit as st
import pandas as pd

modality_list = [
        '0_1', '0_2', '0_3',
        '0_4', '0_5', '0_6',
        '0_7', '0_8', '0_9',
        'end_to_end', 'sequential'
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
            'end_to_end':1,
            'sequential':'sequential'
        }

def load_avg_patient_result(setting:str, metric = 'PSNR_loss'):
    path_to_patient_result = Path(f'new_processed_results/{setting}/per_patient_all_annotations_{metric}.csv')
    if not path_to_patient_result.is_file():
        path_to_all_annotations_results = Path(f'new_processed_results/{setting}/all_annotations_{metric}.csv')
        all_annotations_results = pd.read_csv(path_to_all_annotations_results)
        result_dict = {
            'patient_id':[],
            metric:[],
            'C':[]
        }
        patient_ids = all_annotations_results['patient_id'].unique()
        for patient_id in patient_ids:
            patient_result = all_annotations_results[all_annotations_results["patient_id"] == patient_id]
            for modality in modality_list:
                result_dict['patient_id'].append(patient_id)
                result_dict[metric].append(patient_result[modality].values[0])
                result_dict['C'].append(modality)

        result_df = pd.DataFrame.from_dict(result_dict)
        result_df.to_csv(path_to_patient_result, index=False)

    return pd.read_csv(path_to_patient_result)

def plot_per_patient_average(data):
    chart = {
        "height": 512,
        "mark": "line",
        "encoding": {
            "x": {
                "field": "patient_id",
                "type": "nominal",
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
                    "field": "PSNR_loss",
                    "type": "quantitative",

                    },
                    "color": {"field": "C", "type": "nominal"}

                }
        }
        ],
    }

    st.vega_lite_chart(
            data,
            chart,
            theme="streamlit",
            use_container_width=True
        )

### Make full width
st.set_page_config(layout="wide")

path_to_reconstruction_results = Path(f'new_processed_results/reconstruction/reconstruction_results.csv')

results_df = pd.read_csv(path_to_reconstruction_results)

n_patients = len(results_df['patient_id'].unique())

st.subheader(f'Averaged per-patient for the sequential approach')
st.dataframe(results_df)


st.subheader(f'Averaged results for the two settings')
low_avg  = results_df["low_res"].mean()
high_avg = results_df["high_res"].mean()
st.markdown(
f"""
Comments:
- There are 69 patients
- On average, the low resolution setting achieves {low_avg:.2f} dB PSNR.
- On average, the high resolution setting achieves {high_avg:.2f} dB PSNR.
- Increasing by four the number of projections (64 -> 256) yields a {high_avg-low_avg:.2f} dB PSNR improvement.
"""
)

