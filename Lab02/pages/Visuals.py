# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")


# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

try:
    if os.path.exists("data.csv"):
        csv_data = pd.read_csv("data.csv")
    else:
        csv_data = pd.DataFrame()
except Exception as e:
    csv_data = pd.DataFrame()

st.write(csv_data)

try:
    if os.path.exists("data.json"):
        with open("data.json", "r") as infile:
            json_data = json.load(infile)
        json_data = json_data[0]
        hairData = pd.DataFrame({
            "Hair Color": json_data["Hair Color"],
            "# of Students": json_data["# of Students"]
        })
    else:
        hairData = pd.DataFrame()
except Exception as e:
    hairData = pd.DataFrame()

st.write(hairData)

# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Hair Colors (JSON)") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
#st.warning("Placeholder for your first graph.")

#st.bar_chart(data=hairData, x="Hair Color", y="# of Students")
hairData.columns = [str(col).strip() for col in hairData.columns]

if not hairData.empty and "Hair Color" in hairData.columns:
    st.bar_chart(hairData.set_index("Hair Color"))
    st.write("This graph displays the number of students in a class with each hair color specified.")
else:
    st.warning("Hair color data not found or empty.")


# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Hours Spent in Class Line Chart (CSV)") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.

df = pd.read_csv("data.csv")
df.columns = [str(col).strip() for col in df.columns]

if not df.empty and "Day" in df.columns and "Hours" in df.columns:

    if "selectedDays" not in st.session_state:
        st.session_state.selectedDays = df["Day"].tolist()

    if "minHours" not in st.session_state:
        st.session_state.minHours = 0

    selectedDays = st.multiselect(
        "Select days to display",
        options=df["Day"],
        default=st.session_state.selectedDays
    )
    st.session_state.selectedDays = selectedDays

    minHours = st.slider(
        "Select minimum hours to display",
        0,
        24,
        st.session_state.minHours
    )
    st.session_state.minHours = minHours

    displayData = df[
        (df["Day"].isin(selectedDays)) &
        (df["Hours"] >= minHours)
    ]

    if not displayData.empty:
        st.line_chart(displayData.set_index("Day")["Hours"])
        st.write("This graph shows hours spent in class for selected days.")
    else:
        st.warning("No data matches the selected days and minimum hours.")

else:
    st.warning("CSV data is missing or does not contain 'Day' and 'Hours' columns.")

# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Hair Colors Area Chart (JSON)") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.

df = hairData.copy()

if "selectedHairColors" not in st.session_state:
    st.session_state.selectedHairColors = df["Hair Color"].tolist()

if "minStudents" not in st.session_state:
    st.session_state.minStudents = 0

selectedHairColors = st.multiselect( #NEW
    "Select hair colors to display",
    options=df["Hair Color"],
    default=st.session_state.selectedHairColors
)
st.session_state.selectedHairColors = selectedHairColors

minStudents = st.slider( #NEW
    "Minimum number of students in hair color group to include",
    0,
    30,  
    st.session_state.minStudents
)
st.session_state.minStudents = minStudents

filtered_df = df[
    (df["Hair Color"].isin(selectedHairColors)) &
    (df["# of Students"] >= minStudents)
]

if not filtered_df.empty:
    st.area_chart(filtered_df.set_index("Hair Color")["# of Students"]) #NEW
    st.write("The area chart shows the number of students for each hair color. Use the filters to select specific hair colors and minimum student counts.")
else:
    st.warning("No hair color data matches the selected filters.")
