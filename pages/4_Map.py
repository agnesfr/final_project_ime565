"""AI Disclosure Template
Tool: ChatGPT-5
Purpose: Http color coding; display apartment locations on the map; prise treshold colors; apartment markers on map
"""


import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Apartment Map", page_icon="🗺️")

# Page title
st.markdown(
    """
    <h2 style="text-align: center">Stockholm Apartment Map 🗺️</h2>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <p style="text-align: center; font-size: 1.1rem;">
    Explore apartments that match your criteria. Click on markers to see details!
    </p>
    <hr style="border: 1px solid #ccc;">
    """,
    unsafe_allow_html=True,
)

area_input = float(st.session_state.get("area", 40))
rent_input = float(st.session_state.get("rent", 15000))

area_min_default = max(10.0, area_input - 10.0)
area_max_default = area_input + 10.0

col1, col2 = st.columns(2)

with col1:
    area_min, area_max = st.slider(
        "Area range (m²)",
        min_value=10.0,
        max_value=200.0,
        value=(area_min_default, area_max_default),
        step=1.0,
        help="Show apartments with living area within this range.",
        key="area_range_slider"
    )

with col2:
    max_rent = st.slider(
        "Maximum monthly rent (SEK)",
        min_value=0,
        max_value=max(int(max(rent_input * 2, 5000)), int(rent_input)),
        value=int(rent_input),
        step=100,
        help="Show apartments with rent at or below this value.",
        key="max_rent_slider"
    )

location_scope = st.radio(
    "Location scope",
    options=("Only my chosen area", "Show all Stockholm"),
    index=0,
    horizontal=True,
    key="location_scope",
)

# Load and prepare data
@st.cache_data
def load_data():
    df = pd.read_csv("apartments_sweden.csv")

    if "rent" in df.columns:
        df["rent"] = df["rent"].astype(str).str.replace(",", "", regex=False).astype(float)
    return df.dropna()

# Get filtered data based on user inputs
def get_data(df: pd.DataFrame, area_range: tuple, max_rent_val: float, location_scope_val: str) -> pd.DataFrame:
    location_area = st.session_state.get("location_area", "Södermalm")
    number_of_rooms = float(st.session_state.get("number_of_rooms", 2))
    floor = float(st.session_state.get("floor", 3))
    has_elevator = st.session_state.get("has_elevator", "no")
    has_fireplace = st.session_state.get("has_fireplace", "no")
    has_outside = st.session_state.get("has_outside", "no")

    area_min, area_max = area_range
    max_rent = max_rent_val
    scope_choice = location_scope_val

    # Base filtering on user preferences
    filtered = df[
        (df["number_of_rooms"] == number_of_rooms) &
        (df["area"].between(area_min, area_max)) &
        (df["floor"] == floor) &
        (df["has_elevator"] == has_elevator) &
        (df["has_fireplace"] == has_fireplace) &
        (df["has_outside"] == has_outside) &
        (df["rent"] <= max_rent)
    ]

    # Apply location filtering based on scope choice
    if scope_choice == "Only my chosen area":
        filtered = filtered[filtered["location_area"] == location_area]
    # If "Show all Stockholm", don't filter by location_area

    return filtered

# Fixed price thresholds
def get_price_color(price):
    if price < 2_000_000:
        return "green"
    elif price < 4_000_000:
        return "lightgreen"
    elif price < 6_000_000:
        return "orange"
    elif price < 8_000_000:
        return "red"
    else:
        return "darkred"

# Create map with apartment markers
def create_map(apartment_data: pd.DataFrame) -> folium.Map:
    if apartment_data.empty:
        center = [59.3293, 18.0686]
    else:
        center = [
            apartment_data["latitude"].mean(),
            apartment_data["longitude"].mean(),
        ]

    m = folium.Map(location=center, zoom_start=11, tiles="OpenStreetMap")

    if apartment_data.empty:
        return m

    def get_price_color(price):
        if price < 2_000_000:
            return "green"
        elif price < 4_000_000:
            return "lightgreen"
        elif price < 6_000_000:
            return "orange"
        elif price < 8_000_000:
            return "red"
        else:
            return "darkred"

    # Add markers
    for _, row in apartment_data.iterrows():
        price = row["sold_price"]
        color = get_price_color(price)

        popup_content = f"""
        <div style="width: 250px;">
            <h4>🏠 Apartment Details</h4>
            <strong>Price:</strong> {price:,.0f} SEK<br>
            <strong>Location:</strong> {row['location_area']}<br>
            <strong>Adress:</strong> {row['adress']}<br>
            <strong>Rooms:</strong> {row['number_of_rooms']}<br>
            <strong>Area:</strong> {row['area']} m²<br>
            <strong>Floor:</strong> {row['floor']}<br>
            <strong>Rent:</strong> {row['rent']:,.0f} SEK<br>
            <strong>Elevator:</strong> {row['has_elevator']}<br>
            <strong>Fireplace:</strong> {row['has_fireplace']}<br>
            <strong>Outside:</strong> {row['has_outside']}
        </div>
        """

        tooltip_content = (
            f"💰 {price:,.0f} SEK | "
            f"📍 {row['location_area']} | "
            f"🏠 {row['number_of_rooms']} rooms"
        )

        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            icon=folium.Icon(color=color, icon="home"),
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=tooltip_content,
        ).add_to(m)

    return m


df = load_data()
filtered_apartments = get_data(df, (area_min, area_max), max_rent, location_scope)

if filtered_apartments.empty:
    st.warning("⚠️ No apartments match your criteria. Try changing inputs on the User Input page.")
    empty_map = create_map(filtered_apartments)  # full dataset map
    st_folium(empty_map, width=700, height=500)
else:
    stockholm_map = create_map(filtered_apartments)
    st_folium(stockholm_map, width=700, height=500)

# Info expander
with st.expander("ℹ️ How to use this map"):
    st.write(
        """
        - Change apartment details on the **User Input** page.
        - This map shows apartments that match your current inputs.
        - Hover over a marker to see basic info, and click to see full details.
        - Marker color reflects price: green = cheaper, dark red = more expensive.
        """
    )
