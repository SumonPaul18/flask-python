import streamlit as st
import requests

st.set_page_config(page_title="My Streamlit App")

st.write("Enter some data to process:")

with st.form(key='my_form'):
    input_data = st.text_input(label='Enter data')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    response = requests.post('http://localhost:5000/process', json={'input_data': input_data})
    if response.status_code == 200:
        st.write('Processed data:', response.json()['processed_data'])
    else:
        st.write('Error:', response.status_code)
