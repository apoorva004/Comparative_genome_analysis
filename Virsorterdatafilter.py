# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
from google.colab import data_table
from vega_datasets import data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Enable the use of data_table to format DataFrames in Colab
data_table.enable_dataframe_formatter()

# Read data from an Excel file into a DataFrame
# Note: The file path should be adjusted to the actual file location
df = pd.read_excel('/content/outputAllMergedVirsorter48newFiles.xlsx')

# Read data from the same Excel file into another DataFrame (duplicate line)
# Note: It appears that the same file is read twice, which may not be necessary
df = pd.read_excel('/content/outputAllMergedVirsorter48newFiles.xlsx')

# Filter rows based on the 'categoryname' column
# Remove rows where 'categoryname' contains the text 'not so sure'
df = df[~(df.categoryname.str.contains('not so sure'))]

# Pivot the DataFrame to reshape the data
# Index: 'DirName'
# Columns: 'categoryname'
# Values: 'Nb phage hallmark genes'
# Fill missing values with 0
# Aggregate function: Count the occurrences
df = df.pivot_table(
    index=['DirName'],
    columns=['categoryname'],
    values='Nb phage hallmark genes',
    dropna=True,
    fill_value=0,
    aggfunc='count'
)

# Create a new column 'SomeWhat Sure' by summing two specific categories
df['SomeWhat Sure'] = df['## 2 - Complete phage contigs - category 2 (somewhat sure)'] + df['## 5 - Prophages - category 2 (somewhat sure)']

# Select and reorder columns in the DataFrame
# Keep only the 'SomeWhat Sure' and '## 4 - Prophages - category 1 (sure)' columns
df = df[['SomeWhat Sure', '## 4 - Prophages - category 1 (sure)']]

# Create a stacked bar plot from the DataFrame
# Kind: 'bar' (bar chart)
# Stacked: True (stacked bars)
df.plot(kind='bar', stacked=True)
