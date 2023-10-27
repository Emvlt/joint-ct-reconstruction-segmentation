import streamlit as st

import pandas as pd

modality_list = [
        '0_1', '0_2', '0_3',
        '0_4', '0_5', '0_6',
        '0_7', '0_8', '0_9',
        '1', 'sequential'
        ]

settings = [
    '6_percent_measurements',
    '25_percent_measurements'
    ]

def write_histogram(data):

    chart = {
        "height": 512,
        "mark": "bar",
        "encoding": {
            "x": {
                "field": "DICE",
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

### Make full width
st.set_page_config(layout="wide")

### CSS
st.sidebar.title('Histograms')

setting = st.sidebar.selectbox(
    'Select Experiment Type',
    settings
    )

metric = st.sidebar.selectbox(
    'Select Metric',
    ['DICE']
    )

modality = st.sidebar.selectbox(
    'Select Metric',
    modality_list[:-1]
    )

col_0, col_1 = st.columns(2)

with col_0:
    path_to_data = f'new_processed_results/6_percent_measurements/{metric}_histogram.csv'
    dataframe = pd.read_csv(path_to_data)
    dataframe = dataframe[dataframe['Modality'].isin( [modality,'sequential'])]
    print(dataframe)
    write_histogram(dataframe)

with col_1:
    path_to_data = f'new_processed_results/25_percent_measurements/{metric}_histogram.csv'
    dataframe = pd.read_csv(path_to_data)
    dataframe = dataframe[dataframe['Modality'].isin( [modality,'sequential'])]
    write_histogram(dataframe)