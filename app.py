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
st.set_page_config(
    page_title='Interactive Diabetes Dashboard',
    layout='wide',
    # page_icon=':rocket:'
)

hide_streamlit_style = """
            <style>
            footer {display: none;}
            section > div {{
                padding: 2rem 1rem 2rem;
            }}
            .block-container {padding: 2rem 1rem 2rem;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


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

@st.cache_data(ttl=24*60*60)  # No need for TTL this time; It's static data
def get_diabetes_binary_df():
    diabetes_data = pd.read_csv("diabetes_binary_split_health_indicators.csv")
	
    # Loop through sex to change binary to strings
    diabetes_data["Sex"].replace({0.0: "♀️ Female", 1.0: "♂️ Male"}, inplace=True)

    # Loop through age to change binary to strings
    diabetes_data["Age"].replace(ageGroupMapping, inplace=True)
    return diabetes_data

diabetes_binary_df = get_diabetes_binary_df()


# @st.cache(ttl=24*60*60)  # Use TTL
# def get_diabetes_geo_df():
#     return pd.read_csv("diabetes_mortality_by_state.csv")

diabetes_geo_df = pd.read_csv("diabetes_mortality_by_state.csv")


@st.cache_data(ttl=24*60*60)  # Use TTL
def get_usa_geo_json_df():
    # Read the geoJSON file using geopandas
    geojson = gpd.read_file(r"gadm41_USA_2.json")
    # geojson = gpd.read_file('cb_2018_us_state_500k/cb_2018_us_state_500k.shp')
    geojson_no_id = geojson.to_json(drop_id=True)
    return geojson_no_id


useGeoJson = get_usa_geo_json_df()

def attemptToRenderSumGraphs(lifeStyleSumGraphs):
    try:
        lifeStyleSumGraphs = alt.vconcat(lifeStyleGraphSelections[0], lifeStyleGraphSelections[1])
        st.altair_chart(lifeStyleSumGraphs, use_container_width=True)
        return
    except:
        print("could not conconate sum graphs -- attempting to render single graph")
        # Fallback to a displaying a single sum graph
        pass
    try:
        st.altair_chart(lifeStyleGraphSelections[0], use_container_width=True)
    except:
        print("could not print sum graphs")

##########
# INPUTS #
##########

st.sidebar.write("Average Death Rate 💀 (%)")
minAvgDeathRate, maxAvgDeathRate = st.sidebar.slider(
    "Average Death Rate 💀 (%)",
    # 15, 39,
    0, 100,
    value=[0, 100],
    label_visibility="collapsed"
)

# def remove_outside_of_min_and_max(rate):
#     if rate >= minAvgDeathRate and rate <= maxAvgDeathRate:
#         return True
#     else:
#         return False

# filtered_death_rates = list(filter(remove_outside_of_min_and_max, diabetes_geo_df['RATE']))
# # Convert to DataFrame
# filtered_death_rates = pd.DataFrame(filtered_death_rates, columns = ['RATE'])
diabetes_geo_df = diabetes_geo_df[diabetes_geo_df["RATE"] > minAvgDeathRate]
diabetes_geo_df = diabetes_geo_df[diabetes_geo_df["RATE"] < maxAvgDeathRate]


numOfBoxesChecked = 0
allowedNumberOfCheckboxes = 2

includeFruits = False
includeVeggies = False
includePhysicallyActive = False
includeSmoker = False
includeHasHealthCare = False
includeMentalHealth = False

st.sidebar.write("Add To Individual Lifestyles & Diabetes Graph")
if st.sidebar.checkbox("🍎Fruits", value=True, disabled = True if numOfBoxesChecked >= allowedNumberOfCheckboxes else False):
    numOfBoxesChecked += 1
    includeFruits = True

if st.sidebar.checkbox("🥕Veggies", value=True, disabled = True if numOfBoxesChecked >= allowedNumberOfCheckboxes else False):
    numOfBoxesChecked += 1
    includeVeggies = True

if st.sidebar.checkbox("👟Physically Active", disabled = True if numOfBoxesChecked >= allowedNumberOfCheckboxes else False):
    numOfBoxesChecked += 1
    includePhysicallyActive = True

if st.sidebar.checkbox("🚬Smoker", disabled = True if numOfBoxesChecked >= allowedNumberOfCheckboxes else False):
    numOfBoxesChecked += 1
    includeSmoker = True

if st.sidebar.checkbox("🩺Has Healthcare", disabled = True if numOfBoxesChecked >= allowedNumberOfCheckboxes else False):
    numOfBoxesChecked += 1
    includeHasHealthCare = True

if st.sidebar.checkbox("🧠Mental Health", disabled = True if numOfBoxesChecked >= allowedNumberOfCheckboxes else False):
    numOfBoxesChecked += 1
    includeMentalHealth = True


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

st.sidebar.write("Age Groups")
minAgeGroup, maxAgeGroup = st.sidebar.select_slider(
    label="",
    value=["18-24", "> 80"],
    options=ageRanges,
    label_visibility="collapsed"
)

minIndex = ageRanges.index(minAgeGroup)
maxIndex = ageRanges.index(maxAgeGroup)

ageRangesSelected = ageRanges[minIndex:]
ageRangesSelected = ageRangesSelected[:maxIndex]

diabetes_binary_df = diabetes_binary_df[diabetes_binary_df["Age"].isin(ageRangesSelected)]


st.sidebar.write("Effects of Lifestyle")
lifeStyleChoice = st.sidebar.radio(label="", options=("Fruits", "Veggies"), label_visibility="collapsed")
#############
# DASHBOARD #
#############

def display_map(df):
    # df['RATE'] = deathRate

    # st.write("follium df: ", df)

    map = folium.Map(location=[40, -100], zoom_start=3)

    folium.Choropleth(
        geo_data=useGeoJson,
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
    
    st_folium(map, width=500, height=280)


# Layout stuff #

container = st.container()
col1, col2 = st.columns((1, 1))

with container:

    container.title("Interactive dashboard of diabetes in the US")
    with col1:
        
        # 📈 Display our folium map #
        display_map(diabetes_geo_df)

        # 📈 Display our area chart #
        chart_data = diabetes_binary_df[["Diabetes_binary", "Age", "Sex"]]
        
        chart_data = chart_data.groupby(["Age", "Sex"], as_index=False).sum()

        area_chart = alt.Chart(chart_data).mark_area().encode(
            x=alt.X("Age:O", axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Diabetes_binary:Q", title="Population with Diabetes"),
            color=alt.Color("Sex:O", scale=alt.Scale(range=["#ffc8dd", "#bde0fe"]))
        )

        st.altair_chart(area_chart, use_container_width=True)


    with col2:
        

        # 📈 Display our bar chart #

        activeLifeStyleChoices = diabetes_binary_df[["Diabetes_binary", "Fruits", "Veggies", "PhysActivity", "Smoker", "AnyHealthcare", "MentHlth", "Sex"]]

        # Loop through activeLifeStyleChoices to change binary to strings
        activeLifeStyleChoices["Diabetes_binary"].replace({0.0: "❌ No Diabetes", 1.0: "⭕ Has Diabetes"}, inplace=True)

        # Control which charts to show to save space
        lifeStyleGraphSelections = []

        if (includeFruits == True):
            sumOfFruitsChart = alt.Chart(activeLifeStyleChoices).mark_bar(
                cornerRadiusTopLeft=3,
                cornerRadiusTopRight=3
            ).encode(
                alt.X("sum(Fruits):Q", title="Fruit Eating Population"),
                alt.Y("Diabetes_binary:O", title="Diabetes", stack=None),
                color=alt.Color("sum(Fruits):O", title="",
                    legend=alt.Legend(orient='none',
                    legendX=130, legendY=-60,
                    direction='horizontal',
                    titleAnchor='middle'
                ))
            )
            lifeStyleGraphSelections.append(sumOfFruitsChart)
        if (includeVeggies == True):
            sumOfVeggiesChart = alt.Chart(activeLifeStyleChoices).mark_bar(
                cornerRadiusTopLeft=3,
                cornerRadiusTopRight=3
            ).encode(
                alt.X("sum(Veggies):Q", title="Vegetable Eating Population"),
                alt.Y("Diabetes_binary:O", title="Diabetes", stack=None),
                color=alt.Color("sum(Veggies):O", title="",
                    legend=alt.Legend(orient='none',
                    legendX=130, legendY=-60,
                    direction='horizontal',
                    titleAnchor='middle'
                ))
            )
            lifeStyleGraphSelections.append(sumOfVeggiesChart)
        if (includePhysicallyActive == True):
            sumOfPhysicallyActiveChart = alt.Chart(activeLifeStyleChoices).mark_bar(
                cornerRadiusTopLeft=3,
                cornerRadiusTopRight=3
            ).encode(
                alt.X("sum(PhysActivity):Q", title="Physically Active Population"),
                alt.Y("Diabetes_binary:O", title="Diabetes", stack=None),
                color=alt.Color("sum(PhysActivity):O", title="",
                    legend=alt.Legend(orient='none',
                    legendX=130, legendY=-60,
                    direction='horizontal',
                    titleAnchor='middle'
                ))
            )
            lifeStyleGraphSelections.append(sumOfPhysicallyActiveChart)
        if (includeSmoker == True):
            sumOfSmokerChart = alt.Chart(activeLifeStyleChoices).mark_bar(
                cornerRadiusTopLeft=3,
                cornerRadiusTopRight=3
            ).encode(
                alt.X("sum(Smoker):Q", title="Tobaco Smoking Population"),
                alt.Y("Diabetes_binary:O", title="Diabetes", stack=None),
                color=alt.Color("sum(Smoker):O", title="",
                    legend=alt.Legend(orient='none',
                    legendX=130, legendY=-60,
                    direction='horizontal',
                    titleAnchor='middle'
                ))
            )
            lifeStyleGraphSelections.append(sumOfSmokerChart)
        if (includeHasHealthCare == True):
            sumOfHealthCareChart = alt.Chart(activeLifeStyleChoices).mark_bar(
                cornerRadiusTopLeft=3,
                cornerRadiusTopRight=3
            ).encode(
                alt.X("sum(AnyHealthcare):Q", title="Population w/ Health Care"),
                alt.Y("Diabetes_binary:O", title="Diabetes", stack=None),
                color=alt.Color("sum(AnyHealthcare):O", title="",
                    legend=alt.Legend(orient='none',
                    legendX=130, legendY=-60,
                    direction='horizontal',
                    titleAnchor='middle'
                ))
            )
            lifeStyleGraphSelections.append(sumOfHealthCareChart)
        if (includeMentalHealth == True):
            sumOfMentalHealthChart = alt.Chart(activeLifeStyleChoices).mark_bar(
                cornerRadiusTopLeft=3,
                cornerRadiusTopRight=3
            ).encode(
                alt.X("sum(MentHlth):Q", title="Population w/ Mental Health Affairs"),
                alt.Y("Diabetes_binary:O", title="Diabetes", stack=None),
                color=alt.Color("sum(MentHlth):O", title="",
                    legend=alt.Legend(orient='none',
                    legendX=130, legendY=-60,
                    direction='horizontal',
                    titleAnchor='middle'
                ))
            )
            lifeStyleGraphSelections.append(sumOfMentalHealthChart)


        attemptToRenderSumGraphs(lifeStyleGraphSelections)

        # 📈 Display our heat map #

        # Old Matplotlib version #
        # correlation = diabetes_binary_df[["Diabetes_binary", lifeStyleChoice]]

        # fig, ax = plt.subplots(figsize=(8, 2.5))
        # sns.heatmap(correlation, ax=ax)
        
        # # Based on this answer: https://discuss.streamlit.io/t/cannot-change-matplotlib-figure-size/10295/8
        # # st.pyplot(fig)
        # buf = BytesIO()
        # fig.savefig(buf, format="png")
        # st.image(buf)

        heatMap = alt.Chart(activeLifeStyleChoices).mark_rect().encode(
            alt.X("Diabetes_binary:O", title="Diabetes", axis=alt.Axis(labelAngle=-45)),
            alt.Y("Sex:O", title=""),
            color=alt.Color(f"sum({lifeStyleChoice}):Q", title=f"Total {lifeStyleChoice}")
        ).properties(
            width=400,
            height=300
        )

        st.altair_chart(heatMap, use_container_width=True)
