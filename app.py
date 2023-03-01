import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from matplotlib import rcParams
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
from io import BytesIO


# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

########
# DATA #
########

ageGroupMapping = {
    1: "18-24",
    2: "25-29",
    3: "30-34",
    4: "35-39",
    5: "40-44",
    6: "45-49",
    7: "50-54",
    8: "55-59",
    9: "60-64",
    10: "65-69", 
    11: "70-74", 
    12: "75-79", 
    13: "> 80" 
}

diabetes_binary_df = pd.read_csv("diabetes_binary_split_health_indicators.csv")

# Loop through sex to change binary to strings
# for index, value in enumerate(diabetes_binary_df["Sex"]):
#     diabetes_binary_df["Sex"][index] = "male" if diabetes_binary_df["Sex"][index] == 1 else "female"
diabetes_binary_df["Sex"].replace({0.0: "♀️ Female", 1.0: "♂️ Male"}, inplace=True)


# Loop through age to change binary to strings
diabetes_binary_df["Age"].replace(ageGroupMapping, inplace=True)
print(diabetes_binary_df["Age"])

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
    # 15, 39,
    0, 100,
    value=[0, 100],
)

def remove_outside_of_min_and_max(rate):
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



# ageRanges = {
#     "18-24": 1,
#     "25-29": 2,
#     "30-34": 3,
#     "35-39": 4,
#     "40-44": 5,
#     "45-49": 6,
#     "50-54": 7,
#     "55-59": 8,
#     "60-64": 9,
#     "65-69": 10,
#     "70-74": 11,
#     "75-79": 12,
#     "> 80": 13,
# }

ageRanges = [
    "18-24",
    "25-29",
    "30-34",
    "35-39",
    "40-44",
    "45-49",
    "50-54",
    "55-59",
    "60-64",
    "65-69",
    "70-74",
    "75-79",
    "> 80"
]

minAgeGroup, maxAgeGroup = st.sidebar.select_slider(
    "Age Groups",
    # 18, 80,
    # value=[18, 80],
    value=["18-24", "> 80"],
    options=ageRanges
)

minIndex = ageRanges.index(minAgeGroup)
maxIndex = ageRanges.index(maxAgeGroup)

ageRangesSelected = ageRanges[minIndex:]
ageRangesSelected = ageRangesSelected[:maxIndex]
print("ageRangesSelected: ", ageRangesSelected)

print("minAgeGroup: ", minAgeGroup, "maxAgeGroup: ", maxAgeGroup)
# def remove_outside_of_min_and_max_age_groups(rate):
#     if rate >= minAvgDeathRate and rate <= maxAvgDeathRate:
#         return True
#     else:
#         return False

# diabetes_binary_df['Age'] = list(filter(remove_outside_of_min_and_max_age_groups, diabetes_binary_df['Age']))

diabetes_binary_df = diabetes_binary_df[diabetes_binary_df["Age"].isin(ageRangesSelected)]

#  Convert to DataFrame
# diabetes_binary_df['Age'] = pd.DataFrame(filtered_age_groups, columns = ['RATE'])


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
    
    # st.write("Diabetes Map")
    st_map = st_folium(map, width=600, height=280)


# Layout stuff #

# col1, col2 = st.columns((2, 1))
container = st.container()
col1, col2 = st.columns((1, 1))

with container:

    container.title("Interactive dashboard of diabetes in the US")
    # col1.header("Interactive dashboard of diabetes in the US")
    with col1:
        
        # 📈 Display our folium map #
        display_map(diabetes_df, filtered_death_rates)

        # 📈 Display our area chart #
        # chart_data = pd.DataFrame(
        #     np.random.randn(20, 2),
        #     # diabetes_binary_df[["Age", "Diabetes_binary"]],
        #     # [diabetes_binary_df["Diabetes_binary"].values.toList(), diabetes_binary_df["Age"].values.toList()],
        #     columns=['♂️', '♀️'])
        

        chart_data = diabetes_binary_df[["Diabetes_binary", "Age", "Sex"]]
        
        chart_data = chart_data.groupby(["Age", "Sex"], as_index=False).sum()

        area_chart = alt.Chart(chart_data).mark_area().encode(
            x=alt.X("Age:O", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Diabetes_binary:Q", title="Population with Diabetes"),
            color=alt.Color("Sex:O", scale=alt.Scale(range=["#ffc8dd", "#bde0fe"]))
        )

        

        st.altair_chart(area_chart, use_container_width=True)

        # chart_data = diabetes_binary_df[["Diabetes_binary", "Age"]]
        # # chart_data = diabetes_binary_df[["Diabetes_binary", "Age", "Sex"]]
       
        # # st.write(chart_data.head())
        
        # chart_data = chart_data.groupby('Age', as_index=False).sum()
        # # chart_data = chart_data.groupby(["Age", "Sex"], as_index=False).sum()

        # chart_data.rename(columns={"A": "a", "B": "c"})

        # st.write(chart_data.groupby("Age", as_index=False).sum().head())
        # # st.write(chart_data.groupby(["Age", "Sex"], as_index=False).sum().head())


        # # Add Sex to chart_data
        # # chart_data["Sex"] = ['♂️', '♀️']
        # # chart_data.columns=['♂️', '♀️']

        # # Use go from plotly.graph._objs as go function for plan b
        # st.area_chart(
        #     # diabetes_binary_df[["Age", "Diabetes_binary"]],
        #     # [diabetes_binary_df["Diabetes_binary"].sum(), diabetes_binary_df["Age"]],
        #     chart_data,
        #     # chart_data.groupby('Age').sum(),
        #     height=200,
        #     x="Age",
        #     y="Diabetes_binary"
        # )

    with col2:
        

        # 📈 Display our bar chart #
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            # [diabetes_binary_df["Diabetes_binary"].toList(), diabetes_binary_df["Age"].toList()],
            columns=["a", "b", "c"])

        st.bar_chart(chart_data, height=300)

        # 📈 Display our heat map #
        correlation = diabetes_binary_df[["Diabetes_binary", lifeStyleChoice]]

        fig, ax = plt.subplots(figsize=(8, 2.5))
        sns.heatmap(correlation, ax=ax)
        
        # Based on this answer: https://discuss.streamlit.io/t/cannot-change-matplotlib-figure-size/10295/8
        # st.pyplot(fig)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        st.image(buf)
