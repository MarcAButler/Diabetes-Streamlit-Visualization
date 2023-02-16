import streamlit as st
import numpy
import pandas


st.title("Interactive dashboard of diabetes in the US")

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
