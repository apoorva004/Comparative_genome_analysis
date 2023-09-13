# Import necessary libraries
import os
import shutil
import pandas as pd
from os import listdir
import numpy as np
from os.path import isfile, join

# Define the path to the Excel file
Filepath = '/root/REBASEdatamergeddiamondnonputativeregular.xlsx'

# Initialize variables
count = 0
array = []

# Read data from the Excel file into a DataFrame
df = pd.read_excel(Filepath)

# Calculate new values based on existing columns
df['newQuerySequenceStart'] = np.where(df['QuerySequenceEnd'] - df['QuerySequenceStart'] >= 0, df['QuerySequenceStart'], df['QuerySequenceEnd'])
df['newQuerySequenceEnd'] = np.where(df['QuerySequenceEnd'] - df['QuerySequenceStart'] >= 0, df['QuerySequenceEnd'], df['QuerySequenceStart'])
df['QuerySequenceIDFileName'] = df['QuerySequenceID'] + df['FileName']

# Group the DataFrame by 'QuerySequenceID'
groups = df.groupby('QuerySequenceID')
data = []
filteredGroups = []

# Iterate through each group
for name, group in groups:
    jobsToFilter = []
    jobsToFilterdOut = []

    # Iterate through rows in the group
    for r_idx, row in group.iterrows():
        # Create Job objects and add them to 'jobsToFilter' list
        jobsToFilter.append(Job(row.newQuerySequenceStart, row.newQuerySequenceEnd, row.PercentIdentity, row))

    # Check for maximum profit jobs using the 'Profit.Check' function
    jobsToFilterdOut = Profit.Check(jobsToFilter)

    # Append the filtered jobs to 'filteredGroups'
    for item in jobsToFilterdOut:
        filteredGroups.append(item)

# Create a DataFrame from the filtered groups
filteredoutDataFrame = pd.DataFrame(filteredGroups)

# Save the filtered DataFrame to an Excel file
filteredoutDataFrame.to_excel("REBASEdatamergeddiamondSortednonputativeregular.xlsx")
