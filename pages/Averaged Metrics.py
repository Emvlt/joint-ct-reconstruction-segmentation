import streamlit as st

from utils import display_per_modality_results, load_per_modality_results
from constants import display_to_metrics

st.set_page_config(layout="wide")

st.sidebar.title('Refine Selection')

metric_display = st.sidebar.selectbox(
    'Select Metric',
    display_to_metrics
    )

st.title(f'Per-Modality Averaged {metric_display}, compared to the Sequential Approach')

col_0, col_1 = st.columns(2)

metric = display_to_metrics[metric_display]

text = {
    '6_percent_measurements':{
        'BCE_loss':
            """
            - Excepting C =1, there is a negative impact of the joint training on the Binary Cross-Entropy.
            """,
        'TP':
            """
            - There is a positive impact of the joint approach against the sequential approach.
            - Up to 46 TP are gained for large annotations.
            - Up to 8 TP are gained for small annotations
            """,
        'FP':
            """
            - There is no trend in the relation between the number of FP and the training modality.
            - For instance, for C=0.3, there are 70 less FP but for C = 0.8 there are 66 more.
            """,
        'TN':
            """
            - There is no trend in the relation between the number of TN and the training modality.
            - For instance, for C=0.3, there are 58 more TP but for C = 0.8 there are 76 less.
            """,
        'FN':
            """
            - There seems to be a positive impact of the joint approach against the sequential approach.
            - The only value of C that increases the number of FN is C = 0.2.
            """,
        'Sensitivity':
            """
            - There is a positive impact of the joint approach against the sequential approach.
            - The sensitivity increases by up to 12 percentage points.
            - No values of C decrease the sensitivity.
            """,
        'DICE':
            """
            - There is a positive impact of the joint approach against the sequential approach.
            - The sensitivity increases by up to 9 percentage points.
            - No values of C decrease the Dice score.
            """
    },
    '25_percent_measurements':{
        'BCE_loss':
            """
            - There is a negative impact of the joint training on the Binary Cross-Entropy.
            """,
        'TP':
            """
            - There is no trend in the relation between the number of TP and the training modality.
            - For C = 0.1, 15 TP are gained
            - For C = 0.8, 32 TP are lost
            """,
        'FP':
            """
            - There is a positive impact of the joint training on the number of FP.
            - For any value of C, the joint training reduces the number of FP.
            - Up to 150 FP are lost.
            """,
        'TN':
            """
            - There is a positive impact of the joint training on the number of TN.
            - For any value of C, the joint training increases the number of TN.
            - Up to 150 TP are gained.
            """,
        'FN':
            """
            - There is no trend between the training modality and the impact on FN.
            - For C = 0.1, 12 FP are lost
            - For C = 0.5, 20 FP are gained
            """,
        'Sensitivity':
            """
            - Joint training has a negative impact on the sensitivity
            """,
        'DICE':
            """
            - There is a positive impact of the joint approach against the sequential approach for the Dice score.
            - Excepting C = 0.8, training with the joint approach yields improvement of up to 6 percentage points.
            """
    }
}

with col_0:
    st.header(f'Sparse-View Results')
    low_res_data = load_per_modality_results('6_percent_measurements', metric)
    display_per_modality_results(low_res_data)
    st.markdown(text['6_percent_measurements'][metric])

with col_1:
    st.header(f'High-Resolution Results')
    high_res_data = load_per_modality_results('25_percent_measurements', metric)
    display_per_modality_results(high_res_data)
    st.markdown(text['25_percent_measurements'][metric])

