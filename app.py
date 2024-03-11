import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style
import os

# Set the style to use a black background
style.use('dark_background')

# constants
filename = 'dossier_complet.csv'
meta_filename = 'meta_dossier_complet.csv'
filepath = os.path.join('data', 'dossier_complet', filename)
filepath_meta = os.path.join('data', 'dossier_complet', meta_filename)

# Sample DataFrame (replace this with your actual data)
df = pd.read_csv(filepath, delimiter=';', low_memory=False)

# Calculate fractions
age_groups = ['P20_POP0014', 'P20_POP1529', 'P20_POP3044', 'P20_POP4559', 'P20_POP6074', 'P20_POP7589', 'P20_POP90P']
for age_group in age_groups:
    fraction_column = f'fraction_{age_group}'
    df[fraction_column] = df[age_group] / df['P20_POP']

# Create a new DataFrame with just the fractions
fractions_df = df[[f'fraction_{age_group}' for age_group in age_groups]]

# Define custom labels for the pie chart
custom_labels = ['Ages 0-14', 'Ages 15-29', 'Ages 30-44', 'Ages 45-59', 'Ages 60-74', 'Ages 75-89', 'Ages 90+']

# Streamlit app
st.title('Population Distribution Dashboard')

# Display the DataFrame (optional)
st.subheader('Population Data')
st.dataframe(df)

# Plot the pie chart
st.subheader('Population Distribution by Age Group')
fig, ax = plt.subplots()
ax.pie(fractions_df.mean(), labels=custom_labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired(range(len(age_groups))))
ax.axis('equal')  # Equal aspect ratio ensures that the pie chart is circular.
st.pyplot(fig)
