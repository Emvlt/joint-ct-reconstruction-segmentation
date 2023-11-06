from pathlib import Path

import streamlit as st
import pandas as pd

from constants import modality_list_display, annotations

def write_histogram(data, metric_name):

    chart = {
        "height": 512,
        "mark": "bar",
        "encoding": {
            "x": {
                "field": metric_name,
                "format": ".2f",
                },
            "y": {
                "field": "Count",
                "type": "quantitative"
                },
            "xOffset": {"field": "Modality"},
            "color": {"field": "Modality"}
        }
    }

    st.vega_lite_chart(
            data,
            chart,
            theme="streamlit",
            use_container_width=True
        )

def display_per_modality_results(data):

    chart = {
        "height": 512,
        "mark": "line",
        "encoding": {
            "x": {
                "field": "Modality",
                "type": "nominal",
                "sort":modality_list_display,
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

def load_per_modality_results(setting:str, metric:str) -> pd.DataFrame:
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
        for modality in modality_list_display:

            val = rows[modality].values[0]
            val -= rows['sequential'].values[0]
            if metric in ['Sensitivity', 'DICE']:
                val *= 100
            d['Annotation'].append(annotation)
            d['Modality'].append(modality)
            d['Value'].append(val)
    df = pd.DataFrame.from_dict(d)
    df.to_csv(path_to_plot, index=False)
    return df

def plot_per_slice_results(data, metric):

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
