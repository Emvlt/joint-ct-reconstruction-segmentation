import streamlit as st

import pandas as pd

modality_list = [
        '0_1', '0_2', '0_3',
        '0_4', '0_5', '0_6',
        '0_7', '0_8', '0_9',
        '1', 'sequential'
        ]

modality_to_display = {
    '0_1':'C = 0.1',
    '0_2':'C = 0.2',
    '0_3':'C = 0.3',
    '0_4':'C = 0.4',
    '0_5':'C = 0.5',
    '0_6':'C = 0.6',
    '0_7':'C = 0.7',
    '0_8':'C = 0.8',
    '0_9':'C = 0.9',
    '1'  :'C = 1',
    'sequential':'sequential'
}

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

metric = st.sidebar.selectbox(
    'Select Metric',
    ['DICE']
    )

modality = st.sidebar.selectbox(
    'Select modality',
    [modality_to_display[mod] for mod in modality_list[:-1]]
    )

col_0, col_1 = st.columns(2)

with col_0:
    st.header(f'Sparse-View Results')
    st.subheader(f'Distribution of {metric} values for modalitity {modality_to_display[modality]}')
    path_to_data = f'new_processed_results/6_percent_measurements/{metric}_histogram.csv'
    dataframe = pd.read_csv(path_to_data)
    dataframe = dataframe[dataframe['Modality'].isin( [modality,'sequential'])]
    write_histogram(dataframe)

with col_1:
    st.header(f'High Angular Resolution Results')
    st.subheader(f'Distribution of {metric} values for modalitity {modality_to_display[modality]}')
    path_to_data = f'new_processed_results/25_percent_measurements/{metric}_histogram.csv'
    dataframe = pd.read_csv(path_to_data)
    dataframe = dataframe[dataframe['Modality'].isin( [modality,'sequential'])]
    write_histogram(dataframe)