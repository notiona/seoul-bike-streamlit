"""Seoul Bike Introduction streamlit page"""
# pylint:disable=invalid-name, non-ascii-file-name
from pathlib import Path

import streamlit as st

from seoul_bike_streamlit.paths import IMAGE_PATH

st.write("#### What is Seoul Bike (따릉이)?")
st.image(str(Path(IMAGE_PATH) / "seoul-bike.png"),
         caption="https://www.bikeseoul.com/main.do#bike_info",
         output_format="PNG")
st.markdown("Seoul Bike (따릉이) is a public bike rental service "
            "owned by the city of Seoul, that has started in April 2015.\n\n"
            "The city provides bicycle rental services for citizens, with "
            "hundreds of rental stations all around Seoul.\n\n"
            "For more information, visit the "
            "[Seoul Bike official website](https://www.bikeseoul.com/main.do).")
