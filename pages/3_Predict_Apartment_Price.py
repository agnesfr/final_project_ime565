"""AI Disclosure Template
Tool: ChatGPT-5
Purpose: Debug matching varible name to training data; Http color coding
"""


import streamlit as st
import pandas as pd
import pickle
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title = "Sold Apartment Prices", 
                   page_icon = "🏢",)

# Page title
st.markdown(
    """
    <h2 style="text-align: center;">Apartment Prices Predictor - Results 🌟</h2>
    """,
    unsafe_allow_html=True,
)

# Subtitle with a descriptive message
st.markdown(
    """
    <h3 style="text-align: center;">Discover the Apartment Prices in Stockholm</h3>
    <p style="text-align: center; font-size: 1.1rem;">
    Based on the apartment details you provided, this is the estimated price prediction
    </p>
    <hr style="border: 1px solid #ccc;">
    """,
    unsafe_allow_html=True,
)

# # Ensure session state keys are initialized
if 'form_submitted' not in st.session_state:
    st.session_state['form_submitted'] = False

# Check if the form has been submitted
if st.session_state['form_submitted'] == False:
    st.warning("Please fill out the form on the 'User Input' page before viewing predictions.")
    st.stop()

# Load models
@st.cache_resource
def load_model(path="apartment_models.pickle"):  
    with open(path, "rb") as f:
        return pickle.load(f)

model = load_model() 

model_choice = st.sidebar.radio(
    "Choose model for prediction", 
    ("Random Forest", "Decision Tree", "AdaBoost", "Soft Voting")
)

# Save model choice to session state
st.session_state['model_choice'] = model_choice

# Predict without button click
if model_choice == "Random Forest":
    selected_model = model['Random Forest']
elif model_choice == "Decision Tree":
    selected_model = model['Decision Tree']
elif model_choice == "AdaBoost":
    selected_model = model['AdaBoost']
else:
    selected_model = model['Soft Voting']

#match the data in pickle file
default_df = pd.read_csv('apartments_sweden.csv')
default_df['rent'] = default_df['rent'].str.replace(',', '').astype(float)
default_df = default_df[default_df['floor'] <= 10]
default_df.dropna(inplace = True)
#drop longitude latitude and sold price from default df
encode_df = default_df.copy().drop(columns=['sold_price', 'latitude', 'longitude', 'adress'])

# Prepare user input data
user_data = {
    'location_area': st.session_state['location_area'],
    'number_of_rooms': (st.session_state['number_of_rooms']),
    'area': st.session_state['area'],
    'rent': st.session_state['rent'],
    'floor': st.session_state['floor'],  # Convert to str to match training data
    'has_elevator': st.session_state['has_elevator'],
    'has_fireplace': st.session_state['has_fireplace'],
    'has_outside': st.session_state['has_outside']
}
user_df = pd.DataFrame([user_data])

# Ensure the order of columns in user data is in the same order as that of original data
user_df = user_df[encode_df.columns]

# Concatenate two dataframes together along rows (axis = 0)
encode_df = pd.concat([encode_df,user_df], axis = 0)

# Define which columns should be one-hot encoded
cat_cols = ['location_area', 'number_of_rooms', 'floor', 
            'has_elevator', 'has_fireplace', 'has_outside']

encode_dummy_df = pd.get_dummies(encode_df, columns=cat_cols, dtype=int).tail(1)


alpha = st.slider(
    "Select alpha value",  
    min_value=0.1,         
    max_value=0.9,         
    value=0.5,             
    step=0.01,
    help="Alpha defines the uncertainty level for the prediction intervals. Higher alpha means larger uncertainty."
)

prediction, intervals = selected_model.predict(encode_dummy_df, alpha=alpha)
pred_value = int(prediction[0])
lower_limit = int(max(0, intervals[:, 0][0][0]) )
upper_limit = int(max(0, intervals[:, 1][0][0]))


st.markdown(
    f"""
    <div style="
        background-color:#e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 8px;">
        <h4 style="color:#2e7d32; margin-bottom:5px;">✅ Predicted Price Using {model_choice}</h4>
        <h2 style="color:#1b5e20;">{pred_value:,.0f} SEK</h2>
        <p style="color:#2e7d32;">With a <b>{(1 - alpha):.0%}</b> confidence level:</p>
        <p style="color:#2e7d32;"><b>Prediction Interval:</b> 
        [{int(lower_limit):,} — {int(upper_limit):,}] SEK</p>
    </div>
    """,
    unsafe_allow_html=True
)

