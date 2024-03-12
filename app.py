## IMPORTS
import pandas as pd
import streamlit as st

import matplotlib.pyplot as plt
import matplotlib.style as style

import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
from plotly.subplots import make_subplots

import os

## READ DATA
# Set the style to use a black background
style.use('dark_background')

# constants
filename = 'dossier_complet.csv'
meta_filename = 'meta_dossier_complet.csv'
filepath = os.path.join('data', 'dossier_complet', filename)
filepath_meta = os.path.join('data', 'dossier_complet', meta_filename)

# Sample DataFrame (replace this with your actual data)
df = pd.read_csv(filepath, delimiter=';', low_memory=False)
df['CODGEO'] = df['CODGEO'].astype(str)
df = df[df['CODGEO'].str.startswith(('14', '27', '50', '61', '76'))] ## filter for Normandy codes

########################### INFORMATION ##############################
st.title('Homecare Business Optimization in Normandy')

st.write(
    "Normandy, situated in northwestern France, is divided into five departments: Calvados, Eure, La Manche, Orne, and Seine-Maritime."
    " To enhance our homecare services, we aim to strategically expand in regions with a higher density of elderly population."
    " For detailed insights into Normandy's administrative divisions, including departments, arrondissements, cantons, and communes,"
    " you can refer to the official INSEE page: [Normandy INSEE](https://www.insee.fr/fr/metadonnees/cog/region/REG28-normandie)."
    " This page provides comprehensive information about the demographics and structure of each administrative level within the Normandy region."
)

st.subheader('Data Source: INSEE Dataset')
st.write(
    "The data used in this analysis is sourced from the INSEE dataset, providing approximately 1,900 indicators related to population evolution,"
    " family structure, housing, education, employment, income, and various socio-economic characteristics at the communal level."
    " The dataset covers multiple data sources, including population censuses, vital statistics, social and fiscal data, and more."
    " For a detailed description and access to the dataset, you can visit the [INSEE Dataset](https://www.insee.fr/fr/statistiques/5359146)."
)

########################### GRAPH 1 ##############################

# Define area code groups for arrondissments
calvados_area_codes = ['141', '142', '143', '144']
eure_area_codes = ['271', '272', '273']
la_manche_area_codes = ['501', '502', '503', '504']
orne_area_codes = ['611', '612', '613']
seine_maritime_area_codes = ['761', '762', '763']

# Function to calculate density for a given DataFrame and area codes
def calculate_density(data_df, age_group):
    if age_group == '60+':
        columns = ['P20_POP6074', 'P20_POP7589', 'P20_POP90P']
    elif age_group == '75+':
        columns = ['P20_POP7589', 'P20_POP90P']
    elif age_group == '90+':
        columns = ['P20_POP90P']
    else:
        raise ValueError("Invalid age group selection")

    return data_df[columns].sum(axis=1) / data_df['P20_POP'] * 100

# Mapping area codes to names
area_code_names = {
    '141': 'Bayeux',
    '142': 'Caen',
    '143': 'Lisieux',
    '144': 'Vire',
    '271': 'Les Andelys',
    '272': 'Bernay',
    '273': 'Evreux',
    '501': 'Avranches',
    '502': 'Cherbourg',
    '503': 'Coutances',
    '504': 'Saint-Lô',
    '611': 'Alençon',
    '612': 'Argentan',
    '613': 'Mortagne-au-Perche',
    '761': 'Dieppe',
    '762': 'Le Havre',
    '763': 'Rouen'
}

# Streamlit app
st.subheader('Density in Different Arrondissements by Age Group')

# User selection for age group
selected_age_group = st.selectbox('Select Age Group:', ['60+', '75+', '90+'], index=1)

# Plotting
bar_width = 0.25

# Create subplots with one subplot for each region
fig = make_subplots(rows=1, cols=1, subplot_titles=[f'Density of People Ages {selected_age_group} in Different Arrondissements'])

# Plotting for Calvados
for i, area_code in enumerate(calvados_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df, selected_age_group)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='blue', name=f'{area_code} - Calvados'))

# Plotting for Eure
for i, area_code in enumerate(eure_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df, selected_age_group)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='purple', name=f'{area_code} - Eure'))

# Plotting for La Manche
for i, area_code in enumerate(la_manche_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df, selected_age_group)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='green', name=f'{area_code} - la Manche'))

# Plotting for l'Orne
for i, area_code in enumerate(orne_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df, selected_age_group)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='orange', name=f"{area_code} - l'Orne"))

# Plotting for Seine-Maritime
for i, area_code in enumerate(seine_maritime_area_codes):
    area_df = df[df['CODGEO'].astype(str).str.startswith(area_code)]
    area_density = calculate_density(area_df, selected_age_group)
    area_name = f'{area_code_names[area_code]} ({area_code})'
    fig.add_trace(go.Bar(x=[area_name], y=[area_density.mean()], marker_color='red', name=f"{area_code} - Seine-Maritime"))

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



########################### GRAPH 2 ##############################
def generate_fractions_df(df, age_groups):
    # Calculate fractions
    for age_group in age_groups:
        fraction_column = f'fraction_{age_group}'
        df[fraction_column] = df[age_group] / df['P20_POP']

    # Create a new DataFrame with just the fractions
    fractions_df = df[[f'fraction_{age_group}' for age_group in age_groups]]

    return fractions_df

# Define custom labels for the pie chart
custom_labels = ['Ages 0-14', 'Ages 15-29', 'Ages 30-44', 'Ages 45-59', 'Ages 60-74', 'Ages 75-89', 'Ages 90+']
age_groups = ['P20_POP0014', 'P20_POP1529', 'P20_POP3044', 'P20_POP4559', 'P20_POP6074', 'P20_POP7589', 'P20_POP90P']

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


