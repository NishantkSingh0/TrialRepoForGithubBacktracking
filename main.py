import streamlit as st


# Building sample Streamlit Layout for taking Github URL
if "url" not in st.session_state:
    st.session_state.url=""

st.set_page_config(layout="wide")  
st.session_state.url = st.text_input("Git URL", "")

run_analysis = st.button("🚀 Analyze")