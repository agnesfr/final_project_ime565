"""AI Disclosure Template
Tool: ChatGPT-5
Purpose: Implement weighted feature importance calculation and plotting for Soft Voting Classifier; 
color code predicted classes in Streamlit app; display prediction probabilities with one decimal place"""

# Import necessary libraries
import streamlit as st
import pickle
import pandas as pd

# Suppress warnings
import warnings
warnings.filterwarnings("ignore")   

st.title("Apartment Prices Prediction")
st.write("Predict apartment prices using machine learning.")

# Image
st.image("apartments_image.jpg", use_container_width=True)
st.caption("Image Source: Svensk Fastighetsförmedling")

# Add app description section
st.write("Utilize our advanced machine learning application to predict apartment prices")

# What can you do in this app?
with st.expander("What can you do in this app?"):
    st.write("""
    - Input apartment features to get price predictions.
    - View map over apartment locations.
    - Understand which feature of the apartment affects the price the most.
    """)

st.sidebar.subheader("Navigate this app")
st.sidebar.write("""
- *Home*: Overview of the app.
- *Understanding Models*: Information about diffrent models that is used.
- *User Input*: Upload your apartment features.
- *Predict Apartment Price*: Get price predictions.
- *Map*: View apartment locations on a map.
- *Additional Information*: More information about model preformance.
""")

# Initilize session state keys for user input
if 'latitude' not in st.session_state:
    st.session_state['latitude'] = 59.30962174
if 'longitude' not in st.session_state:
    st.session_state['longitude'] = 18.07417091
if 'adress' not in st.session_state:
    st.session_state['adress'] = 'No adress'
if 'location_area' not in st.session_state:
    st.session_state['location_area'] = 'Södermalm'
if 'number_of_rooms' not in st.session_state:
    st.session_state['number_of_rooms'] = 2
if 'area' not in st.session_state:
    st.session_state['area'] = 40
if 'rent' not in st.session_state:
    st.session_state['rent'] = 1500
if 'floor' not in st.session_state:
    st.session_state['floor'] = 3
if 'has_elevator' not in st.session_state:
    st.session_state['has_elevator'] = 'Yes'
if 'has_fireplace' not in st.session_state:
    st.session_state['has_fireplace'] = 'No'
if 'has_outside' not in st.session_state:
    st.session_state['has_outside'] = 'No'
if "form_submitted" not in st.session_state:
    st.session_state["form_submitted"] = False
if 'model_choice' not in st.session_state:
    st.session_state['model_choice'] = 'Decision Tree'  # Default to Decision Tree
if "area_range_slider" not in st.session_state:
    st.session_state["area_range_slider"] = (30.0, 50.0)
if "max_rent_slider" not in st.session_state:
    st.session_state["max_rent_slider"] = 15000.0
if "location_scope" not in st.session_state:
    st.session_state["location_scope"] = "Only my chosen area"

