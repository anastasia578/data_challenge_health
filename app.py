import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.express as px
import mplcursors  # Import mplcursors for hover functionality
import os


def generate_fractions_df(df, age_groups):
    # Calculate fractions
    for age_group in age_groups:
        fraction_column = f'fraction_{age_group}'
        df[fraction_column] = df[age_group] / df['P20_POP']

    # Create a new DataFrame with just the fractions
    fractions_df = df[[f'fraction_{age_group}' for age_group in age_groups]]

    return fractions_df


# Set the style to use a black background
style.use('dark_background')

# constants
filename = 'dossier_complet.csv'
meta_filename = 'meta_dossier_complet.csv'
filepath = os.path.join('data', 'dossier_complet', filename)
filepath_meta = os.path.join('data', 'dossier_complet', meta_filename)

# Sample DataFrame (replace this with your actual data)
df = pd.read_csv(filepath, delimiter=';', low_memory=False)

# Define custom labels for the pie chart
custom_labels = ['Ages 0-14', 'Ages 15-29', 'Ages 30-44', 'Ages 45-59', 'Ages 60-74', 'Ages 75-89', 'Ages 90+']
age_groups = ['P20_POP0014', 'P20_POP1529', 'P20_POP3044', 'P20_POP4559', 'P20_POP6074', 'P20_POP7589', 'P20_POP90P']

# Streamlit app
st.title('Normandy Population Distribution')

# Multiselect widget for selecting CODGEO values
selected_codgeo_values = st.multiselect('Select area code(s)', df['CODGEO'].unique())

if selected_codgeo_values:
    # Filter DataFrame based on selected CODGEO values
    df = df[df['CODGEO'].isin(selected_codgeo_values)]

fractions_df = generate_fractions_df(df, age_groups)

# Define custom labels for the pie chart
custom_labels = ['Ages 0-14', 'Ages 15-29', 'Ages 30-44', 'Ages 45-59', 'Ages 60-74', 'Ages 75-89', 'Ages 90+']

# Plot the interactive pie chart using Plotly Express
st.subheader('Population Distribution by Age Group')

reversed_color_sequence = px.colors.sequential.RdBu[::-1]

fig = px.pie(
    values=fractions_df.mean(),
    names=custom_labels,
    hole=0.2,  # Set the size of the hole in the middle of the pie chart
    color_discrete_sequence=px.colors.sequential.YlOrBr,
)

fig.update_traces(sort=False) 

# Display the interactive plot
st.plotly_chart(fig)

########################### GRAPH 2 ##############################
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.patches import Patch

# # Sample DataFrame (replace this with your actual data)
# # df = ...

# # Define area code groups
# calvados_area_codes = ['141', '142', '143', '144']
# next_three_area_codes = ['501', '502', '503', '504']
# last_three_area_codes = ['611', '612', '613']

# # Function to calculate density for a given DataFrame and area codes
# def calculate_density(data_df):
#     return data_df[['P20_POP7589', 'P20_POP90P']].sum(axis=1) / data_df['P20_POP'] * 100

# # Mapping area codes to names
# area_code_names = {
#     '141': 'Bayeux',
#     '142': 'Caen',
#     '143': 'Lisieux',
#     '144': 'Vire',
#     '501': 'Avranches',
#     '502': 'Cherbourg',
#     '503': 'Coutances',
#     '504': 'Saint-Lô',
#     '611': 'Alençon',
#     '612': 'Argentan',
#     '613': 'Mortagne-au-Perche'
# }

# # Plotting
# bar_width = 0.25

# # Streamlit app
# st.title('Density of People Ages 75+ in Different Regions')

# # Plotting in Streamlit
# fig, ax = plt.subplots()

# handles = []  # Custom handles for legend
# labels = []   # Custom labels for legend

# # Plotting for Calvados
# for i, area_code in enumerate(calvados_area_codes):
#     area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
#     area_density = calculate_density(area_df)
#     area_name = f'{area_code_names[area_code]} ({area_code})'
#     ax.bar(area_name, area_density.mean(), width=bar_width, color='blue', label=f'{area_code} - Calvados')
#     if i == 0:
#         handles.append(Patch(color='blue'))
#         labels.append('Calvados')

# # Plotting for Next Three
# for i, area_code in enumerate(next_three_area_codes):
#     area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
#     area_density = calculate_density(area_df)
#     area_name = f'{area_code_names[area_code]} ({area_code})'
#     ax.bar(area_name, area_density.mean(), width=bar_width, color='green', label=f'{area_code} - la Manche')
#     if i == 0:
#         handles.append(Patch(color='green'))
#         labels.append("la Manche")

# # Plotting for Last Three
# for i, area_code in enumerate(last_three_area_codes):
#     area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
#     area_density = calculate_density(area_df)
#     area_name = f'{area_code_names[area_code]} ({area_code})'
#     ax.bar(area_name, area_density.mean(), width=bar_width, color='orange', label=f"{area_code} - l'Orne")
#     if i == 0:
#         handles.append(Patch(color='orange'))
#         labels.append("l'Orne")

# ax.set_xlabel('Area Codes')
# ax.set_ylabel('Density (%)')
# ax.set_title('Density of People Ages 75+ in Different Regions')

# ax.set_xticklabels([f'{area_code_names[code]} ({code})' for code in calvados_area_codes + next_three_area_codes + last_three_area_codes], rotation=45, ha='right')

# # Display a single entry in the legend for each region
# ax.legend(handles, labels, loc='upper right', bbox_to_anchor=(1.25, 1.0), title='Regions')

# # Display the plot using Streamlit
# st.pyplot(fig)

import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Sample DataFrame (replace this with your actual data)
# df = ...

# Define area code groups
calvados_area_codes = ['141', '142', '143', '144']
next_three_area_codes = ['501', '502', '503', '504']
last_three_area_codes = ['611', '612', '613']

# Function to calculate density for a given DataFrame and area codes
def calculate_density(data_df):
    return data_df[['P20_POP7589', 'P20_POP90P']].sum(axis=1) / data_df['P20_POP'] * 100

# Mapping area codes to names
area_code_names = {
    '141': 'Bayeux',
    '142': 'Caen',
    '143': 'Lisieux',
    '144': 'Vire',
    '501': 'Avranches',
    '502': 'Cherbourg',
    '503': 'Coutances',
    '504': 'Saint-Lô',
    '611': 'Alençon',
    '612': 'Argentan',
    '613': 'Mortagne-au-Perche'
}

# Plotting
bar_width = 0.25

# Create subplots with one subplot for each region
fig = make_subplots(rows=1, cols=1, subplot_titles=['Density of People Ages 75+ in Different Regions'])

# Plotting for Calvados
for i, area_code in enumerate(calvados_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='blue', name=f'{area_code} - Calvados'))

# Plotting for Next Three
for i, area_code in enumerate(next_three_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='green', name=f'{area_code} - la Manche'))

# Plotting for Last Three
for i, area_code in enumerate(last_three_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='orange', name=f"{area_code} - l'Orne"))

# Update layout
fig.update_layout(
    xaxis=dict(tickangle=-45),
    xaxis_title='Area Codes',
    yaxis_title='Density (%)',
    legend_title='Regions',
    showlegend=True
)

# Show the figure using Streamlit
st.plotly_chart(fig)
