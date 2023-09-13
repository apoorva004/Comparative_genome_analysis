# Import necessary libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as plt
from google.colab import data_table
from vega_datasets import data

# Enable Google Colab data_table for improved DataFrame formatting
data_table.enable_dataframe_formatter()

# Read data from an Excel file into a pandas DataFrame
df = pd.read_excel('/content/Mobilegeneticelementsheatmap.xlsx')

# Select only the 'FileName' and 'ReferenceSequenceID' columns from the DataFrame
df = df[['FileName', 'ReferenceSequenceID']]

# Group the DataFrame by 'FileName' and 'ReferenceSequenceID' and count occurrences
count_series = df.groupby(['FileName', 'ReferenceSequenceID']).size()

# Convert the resulting series into a DataFrame with the count as the 'size' column
new_df = count_series.to_frame(name='size').reset_index()

# Extract the 'ReferenceSequenceID' column from the new DataFrame
new_df['ReferenceSequenceID']

# Create a pivot table from the new DataFrame with 'FileName' as rows,
# 'ReferenceSequenceID' as columns, and 'size' as values
heatmapdf = pd.pivot_table(new_df, index='FileName', columns='ReferenceSequenceID', values='size')

# Fill NaN values in the pivot table with 0
heatmapdf = heatmapdf.fillna(0)

# Export the pivot table to an Excel file named 'PCA.xlsx'
heatmapdf.to_excel('PCA.xlsx')

# Rename specific columns in the pivot table
heatmapdf.rename(columns={
    '_putative_conjugative_transposon_DNA_recombination_protein_[Streptococcus_equi_subsp._equi_4047]':
    'Conjugative transposon DNA recombination protein',
    '_type_4_fimbriae_expression_regulatory_protein_pilR_[Vibrio_cholerae_MJ-1236]':
    'Type IV fimbriae expression regulatory protein (pilR)',
    # Add more renaming as needed
}, inplace=True)

# Calculate the sum of each column and add a 'Total' row to the pivot table
heatmapdf.loc['Total'] = heatmapdf.sum(axis=0)

# Calculate the sum of each row and add a 'sum' column to the pivot table
heatmapdf['sum'] = heatmapdf.sum(axis=1)

# Sort the pivot table by the 'sum' column in descending order and then by 'FileName' in ascending order
heatmapdf = heatmapdf.sort_values(['sum', 'FileName'], axis=0, ascending=[False, True])

# Extract the 'sum' column
heatmapdf['sum']

# Drop the 'sum' column from the pivot table
heatmapdf.drop(['sum'], axis=1, inplace=True)

# Export the final pivot table to an Excel file named 'ICEelementsheatmap45sequences_colabSorted.xlsx'

heatmapdf.to_excel('ICEelementsheatmap45sequences_colabSorted.xlsx')

# Configure matplotlib font settings and set figure size
import matplotlib
import matplotlib.pyplot as pltpy
pltpy.rcParams["font.family"] = "Arial"
sns.set(rc={'figure.figsize': (13, 13)})

# Set x and y-axis tick font sizes and colors
pltpy.xticks(fontsize='10', color="black")
pltpy.yticks(fontsize='11', color="black", style='italic')

# Create a heatmap using seaborn with annotations and a specific color map
chart = sns.heatmap(heatmapdf, annot=True, cmap='PuRd')

# Rotate x-axis tick labels by 45 degrees and align them to the right
chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')

# Display the heatmap
pltpy.show()
