import streamlit as st
import numpy
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium

diabetes_df = pd.read_csv("diabetes_mortality_by_state.csv")
diabetes_df.head()

# Read the geoJSON file using geopandas
geojson = gpd.read_file(r"gadm41_USA_2.json")

# geojson = gpd.read_file('cb_2018_us_state_500k/cb_2018_us_state_500k.shp')
geojson_no_id = geojson.to_json(drop_id=True)


# geojson.head()
# geojson=geojson[['coty_code','geometry']]
# geojson=geojson[['geometry']]



def display_map(df):

    map = folium.Map(location=[48, -102], zoom_start=3)

    folium.Choropleth(
        geo_data=geojson_no_id,
        name="choropleth",
        data=diabetes_df,
        columns=["STATE", "RATE"],
        key_on="feature.properties.NAME_1",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="💀 Rate (%)",
    ).add_to(map)

    folium.LayerControl().add_to(map)
    
    st.write("Diabetes Map")
    st_map = st_folium(map, width=700, height=450)
    st.write(df.head())
    # st.write(df.columns())


st.title("Interactive dashboard of diabetes in the US")

# Display our folium map
display_map(diabetes_df)

st.sidebar.slider(
    "Average Death Rate 💀"
)

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

st.sidebar.write("Add To Diabetes: Age & Sex Graph")
if st.sidebar.checkbox("18-24"):
    "18-24 should be toggled"
if st.sidebar.checkbox("25-29"):
    "25-29 should be toggled"
if st.sidebar.checkbox("30-34"):
    "30-34 should be toggled"
if st.sidebar.checkbox("35-39"):
    "35-39 should be toggled"
if st.sidebar.checkbox("40-44"):
    "40-44 should be toggled"
if st.sidebar.checkbox("45-49"):
    "45-49 should be toggled"
if st.sidebar.checkbox("50-54"):
    "50-54 should be toggled"
if st.sidebar.checkbox("55-59"):
    "55-59 should be toggled"
if st.sidebar.checkbox("60-64"):
    "60-64 should be toggled"
if st.sidebar.checkbox("65-69"):
    "65-69 should be toggled"
if st.sidebar.checkbox("70-74"):
    "70-74 should be toggled"
if st.sidebar.checkbox("75-79"):
    "75-79 should be toggled"
if st.sidebar.checkbox("> 80"):
    "> 80 should be toggled"

st.sidebar.write("Effects of Lifestyle")
lifeStyleChoice = st.sidebar.radio("Lifestyle:",
                                   ("Fruits", "Veggies")
                                   )
