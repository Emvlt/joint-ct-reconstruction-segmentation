import math

from pathlib import Path

import streamlit as st
import pandas as pd

metrics = ['BCE_loss', 'PSNR_loss', 'TP', 'FP', 'TN', 'FN', 'Sensitivity', 'DICE']

annotations = ['small', 'large', 'with', 'without']

modality_list = [
    'sequential',
    '0.1', '0.2', '0.3',
    '0.4', '0.5', '0.6',
    '0.7', '0.8', '0.9',
    'end-to-end',
        ]

def plot_format(setting:str, metric:str) -> pd.DataFrame:
    path_to_plot = Path(f'new_processed_results/{setting}/{metric}_results_plot.csv')
    if path_to_plot.is_file():
        return pd.read_csv(path_to_plot)

    d = {
        'Annotation':[],
        'Modality':[],
        'Value':[]
    }
    path_to_df = Path(f'new_processed_results/{setting}/{metric}_results.csv')
    old_df = pd.read_csv(path_to_df)
    for annotation in annotations:
        rows = old_df[old_df['Annotation'] == annotation]
        for modality in modality_list:

            val = rows[modality].values[0]
            if metric == 'TN':
                val -= rows['sequential'].values[0]
            elif metric == 'Specificity':
                val = math.log(val)
            d['Annotation'].append(annotation)
            d['Modality'].append(modality)
            d['Value'].append(val)
    df = pd.DataFrame.from_dict(d)
    df.to_csv(path_to_plot, index=False)
    return df

def write_per_slice_results(data):

    chart = {
        "height": 512,
        "mark": "line",
        "encoding": {
            "x": {
                "field": "Modality",
                "type": "nominal",
                "sort":modality_list,
                "axis":{
                    "labelAngle":0
                }

            }
        },
        "layer": [
        {
            "mark":
                {"type": "line"}
                ,
            "encoding":
                {
                    "y": {
                    "field": "Value",
                    "type": "quantitative"

                    },
                    "color": {"field": "Annotation", "type": "nominal"}

                }
        },
        {
            "mark":
                {"type": "point"}
                ,
            "encoding":
                {
                    "y": {
                        "field": "Value",
                        "type": "quantitative",
                        "format": ".2f"
                    },
                    "color": {
                        "field": "Annotation", "type": "nominal"}

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

st.set_page_config(layout="wide")

st.sidebar.title('Averaged Results')

metric = st.sidebar.selectbox(
    'Select Metric',
    metrics
    )

col_0, col_1 = st.columns(2)

with col_0:
    low_res_data = plot_format('6_percent_measurements', metric)
    write_per_slice_results(low_res_data)

with col_1:
    high_res_data = plot_format('25_percent_measurements', metric)
    write_per_slice_results(high_res_data)

