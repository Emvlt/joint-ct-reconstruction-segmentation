# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Project Description",
    )

    st.write("# All-in-One project results page")

    st.sidebar.success("Select results type")

    st.markdown(
        """
        ### Browse pages from the sidebar
        - Averaged Metrics shows the different evaluation metrics averaged on the test dataset
        - Metrics Histograms compares the histogram of metrics values between the sequential approach and a given modality.
        - Per-patient results shows the per-patient insight on each method's performance
        - Visuals shows a per-patient result for slice reconstruction and segmentation
    """
    )


if __name__ == "__main__":
    run()
