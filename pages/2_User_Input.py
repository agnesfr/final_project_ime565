import streamlit as st
import pandas as pd

st.set_page_config(page_title = "Form User Input")

st.markdown(
    """
    <style>
      .block-container {max-width: 900px;}
      .app-title { 
        font-size: 50px; 
        font-weight: 800; 
        line-height: 1.1; 
        margin: 8px 0 10px 0; 
        text-align: center;
      }
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="app-title">Fill out a survey</div>', unsafe_allow_html=True)

st.image("sthlm.png", width="stretch", caption = "Stockholm Apartments, picture taken from tours-tickets.se")

# Create a form for user inputs
with st.form("user_inputs_form"):
  st.write("Please fill out the following survey about your apartment preferences:")

  location_area = st.selectbox(
    "Preferred Location Area:",
    ["Östermalm", 
     "Gärdet", 
     "Vasastan", 
     "Norrmalm", 
     "Skeppsholmen", 
     "Djurgården", 
     "Norra Djurgården", 
     "Hjorthagen", 
     "Kungsholmen", 
     "Kristineberg", 
     "Fredhäll", 
     "Marieberg", 
     "Stadshagen", 
     "Lilla Essingen", 
     "Stora Essingen", 
     "Södermalm", 
     "Gamla Stan", 
     "Långholmen", 
     "Reimersholme", 
     "Riddarholmen", 
     "Hammarby sjöstad"]
  , index=15,
  help="Select the neighborhood/area in Stockholm where you'd like to live")

  number_of_rooms = st.selectbox("Number of Rooms:", [1, 1.5, 2, 2.5, 3],
                   help="Choose the number of rooms (2 = 1 bedroom + 1 living room)")

  area = st.number_input("Apartment Area (in square meters):", min_value=10, max_value=200, value=33,
              help="Enter the desired apartment size in square meters")

  rent = st.number_input("Max Rent (in SEK):", min_value=500, max_value=5000, value=2500,
              help="Enter the maximum monthly rent you're willing to pay in Swedish Kronor")

  floor = st.number_input("Floor Level:", -2, 10, 3,
               help="Enter the desired floor level (negative numbers = basement)")

  has_elevator = st.selectbox("Elevator", ["yes", "no"], index=0,
                 help="Does the building have an elevator?")

  has_fireplace = st.selectbox("Fireplace", ["yes", "no"], index=1,
                help="Does the apartment have a fireplace?")

  has_outside = st.selectbox("Outside space (balcony/patio)?", ["yes", "no"], index=1,
                help="Does the apartment have a balcony, patio, or outdoor space?")

  submitted = st.form_submit_button("Save")

  if submitted:
    # Store inputs in session state
    st.session_state['location_area'] = location_area
    st.session_state['number_of_rooms'] = number_of_rooms
    st.session_state['area'] = area
    st.session_state['rent'] = rent
    st.session_state['floor'] = floor
    st.session_state['has_elevator'] = has_elevator
    st.session_state['has_fireplace'] = has_fireplace
    st.session_state['has_outside'] = has_outside
    st.session_state['form_submitted'] = True

    st.success("You can now proceed to the Prediction page to see the estimated apartment price.")
