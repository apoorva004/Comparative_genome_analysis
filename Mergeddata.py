# Import necessary libraries
import os
import shutil
from os import listdir
import pandas as pd
from os.path import isfile, join

# List all files in the specified directory
onlyfiles = [f for f in listdir("/home/apoorva/Diamond_elements/ICESingleGeneDataSorted") if isfile(join("/home/apoorva/Diamond_elements/ICESingleGeneDataSorted", f))]

# Initialize a counter and an empty array
count = 0
array = []

# Loop through each file in the directory
for name in onlyfiles:
    # Create the full file path
    path = os.path.join("/home/apoorva/Diamond_elements/ICESingleGeneDataSorted/", name)

    # Read data from the Excel file into a DataFrame
    df = pd.read_excel(path)

    # Modify the filename to create a new column 'FileName'
    newname = name.replace('tsv_sorted.xlsx', '').replace('_', ' ').replace('Sporosarcina', 'S.')
    df['FileName'] = newname

    # Reorder the columns to place 'FileName' as the first column
    new_cols = ['FileName'] + [col for col in df.columns if col != 'FileName']
    df = df[new_cols]

    # Increment the counter and print a message indicating directory creation
    count += 1
    array.append(df)
    print("Directory '% s' created" % count)

# Concatenate all DataFrames in the 'array' into a single DataFrame
result = pd.concat(array)

# Save the merged DataFrame to an Excel file
result.to_excel("outputAllSortedMerged.xlsx")

# Print the merged DataFrame
print(result)
