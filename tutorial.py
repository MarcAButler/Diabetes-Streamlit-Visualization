"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import numpy as np
import pandas as pd
import time

# st.write("Here's our first attempt at using data to create a table:")
# df = pd.DataFrame({
#   'first column': [1, 2, 3, 4],
#   'second column': [10, 20, 30, 40]
# })

# df

# """
# Line graph example
# """
# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=["A", "B", "C"]
# )

# st.line_chart(chart_data)

# """
# Making Map Data
# """
# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=["LAT", "LON"]
# )

# st.map(map_data)

# """
# Simple slider example
# """
# x = st.slider('x')  # 👈 this is a widget
# st.write(x, 'squared is', x * x)

# """
# Make a simple text input
# """
# st.text_input("Your name", key="name")
# # You can access the value at any point with:
# st.session_state.name

# """
# Show checkbox data 
# """
# if st.checkbox('Show Dataframe'):
#     chart_data = pd.DataFrame(
#         np.random.randn(20, 3),
#         columns=["A", "B", "C"]
#     )

#     chart_data

# if st.checkbox("A Secret"):
#     st.write("[A SUPER SECRET]")


# """
# Column swapping
# """
# def handleColumnSwap(df):
#     if st.checkbox("First Column"):
#         df['first column']
#     if st.checkbox("Second Column"):
#         df['second column']

# df = pd.DataFrame({
#     'first column': [1, 2, 3, 4],
#     'second column': [10, 20, 30, 40]
#     })

# option = st.selectbox(
#     'Which number do you like best?',
#     handleColumnSwap(df)
#     )

# 'You selected: ', option


# """
# Slider, side nav, dropdown
# """
# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )


# """
# Columns and radio buttons
# """
# left_column, right_column = st.columns(2)
# # You can use a column just like st.sidebar:
# left_column.button('Press me!')

# # Or even better, call Streamlit functions inside a "with" block:
# with right_column:
#     chosen = st.radio(
#         'Sorting hat',
#         ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#     st.write(f"You are in {chosen} house!")


# """
# Progress bar simulation
# """

# "Starting a long computation..."

# # Add a placeholder
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#     # Update the progress bar with each iteration
#     latest_iteration.text(f"Iteration {i+1}")
#     bar.progress(i + 1)
#     time.sleep(0.1)
# "DONE"


# """
# Make a title
# """
# st.title("Interactive dashboard of diabetes in the US")

# TODO:
# - Clorpleth Map
# - Use same data
