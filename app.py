import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium

########
# DATA #
########

diabetes_binary_df = pd.read_csv("diabetes_binary_split_health_indicators.csv")
diabetes_binary_df.head()

diabetes_df = pd.read_csv("diabetes_mortality_by_state.csv")
diabetes_df.head()

# Read the geoJSON file using geopandas
geojson = gpd.read_file(r"gadm41_USA_2.json")

# geojson = gpd.read_file('cb_2018_us_state_500k/cb_2018_us_state_500k.shp')
geojson_no_id = geojson.to_json(drop_id=True)

##########
# INPUTS #
##########

minAvgDeathRate, maxAvgDeathRate = st.sidebar.slider(
    "Average Death Rate 💀 (%)",
    15, 39,
    value=[15, 39],
)

def remove_outside_of_min_and_max(rate):
    print("rate", rate)
    if rate >= minAvgDeathRate and rate <= maxAvgDeathRate:
        return True
    else:
        return False

filtered_death_rates = list(filter(remove_outside_of_min_and_max, diabetes_df['RATE']))#[15, 22, 24, 26, 28, 30, 39]
# Convert to DataFrame
filtered_death_rates = pd.DataFrame(filtered_death_rates, columns = ['RATE'])


st.sidebar.write("Add To Individual Lifestyles & Diabetes Graph")
if st.sidebar.checkbox("🍎Fruits"):
    "Fruits should be toggled"
if st.sidebar.checkbox("🥕Veggies"):
    "Veggies should be toggled"
if st.sidebar.checkbox("👟Physically Active"):
    "Physically Active should be toggled"
if st.sidebar.checkbox("🚬Smoker"):
    "Smoker should be toggled"
if st.sidebar.checkbox("🩺Has Healthcare"):
    "Physically Active should be toggled"
if st.sidebar.checkbox("🧠Mental Health"):
    "Mental Health should be toggled"


minAgeGroup, maxAgeGroup = st.sidebar.slider(
    "Age Groups",
    18, 80,
    value=[18, 80],
)
# if st.sidebar.checkbox("18-24"):
#     "18-24 should be toggled"
# if st.sidebar.checkbox("25-29"):
#     "25-29 should be toggled"
# if st.sidebar.checkbox("30-34"):
#     "30-34 should be toggled"
# if st.sidebar.checkbox("35-39"):
#     "35-39 should be toggled"
# if st.sidebar.checkbox("40-44"):
#     "40-44 should be toggled"
# if st.sidebar.checkbox("45-49"):
#     "45-49 should be toggled"
# if st.sidebar.checkbox("50-54"):
#     "50-54 should be toggled"
# if st.sidebar.checkbox("55-59"):
#     "55-59 should be toggled"
# if st.sidebar.checkbox("60-64"):
#     "60-64 should be toggled"
# if st.sidebar.checkbox("65-69"):
#     "65-69 should be toggled"
# if st.sidebar.checkbox("70-74"):
#     "70-74 should be toggled"
# if st.sidebar.checkbox("75-79"):
#     "75-79 should be toggled"
# if st.sidebar.checkbox("> 80"):
#     "> 80 should be toggled"

st.sidebar.write("Effects of Lifestyle")
lifeStyleChoice = st.sidebar.radio("Lifestyle:",
                                   ("Fruits", "Veggies")
                                   )
#############
# DASHBOARD #
#############

# Layout stuff
col1, col2 = st.columns(2)

def display_map(df, deathRate):
    # df = df[(df['RATE'] == deathRate)]
    df['RATE'] = deathRate

    map = folium.Map(location=[48, -102], zoom_start=3)

    # scale = (df['RATE']).quantile((0,0.1,0.75,0.9,0.98,1)).tolist()

    folium.Choropleth(
        geo_data=geojson_no_id,
        name="choropleth",
        data=df,
        columns=["STATE", "RATE"],
        key_on="feature.properties.NAME_1",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Average Death Rate 💀 (%)",
        # threshold_scale=[10, 20, 30, 40, 50]
    ).add_to(map)

    folium.LayerControl().add_to(map)
    
    st.write("Diabetes Map")
    st_map = st_folium(map, width=700, height=450)

st.title("Interactive dashboard of diabetes in the US")


with col1:
    # 📈 Display our folium map #
    display_map(diabetes_df, filtered_death_rates)

    # 📈 Display our area chart #
    chart_data = pd.DataFrame(
        np.random.randn(20, 2),
        columns=['♂️', '♀️'])

with col2:
    st.area_chart(chart_data)

    # 📈 Display our bar chart #
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=["a", "b", "c"])

    st.bar_chart(chart_data)

    # 📈 Display our heat map #