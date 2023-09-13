# Import necessary libraries
import os
import shutil
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

# List all files in the specified directory
onlyfiles = [f for f in listdir("/home/apoorva/Diamond_elements/filtered") if isfile(join("/home/apoorva/Diamond_elements/filtered", f))]

# Initialize a counter and an empty array
count = 0
array = []

# Loop through each file in the directory
for fileName in onlyfiles:
    # Create the full file path
    path = os.path.join("/home/apoorva/Diamond_elements/filtered/", fileName)

    # Read data from the file into two dataframes
    dforiginal = pd.read_table(path, delim_whitespace=True, header=None)
    df = pd.read_table(path, delim_whitespace=True, header=None)

    # Rename columns of the dataframe for clarity
    df.columns = ['QuerySequenceID', 'ReferenceSequenceID', 'PercentIdentity', 'Length', 'MisMatch', 'GapOpen', 'QuerySequenceStart', 'QuerySequenceEnd', 'ReferenceSequenceStart', 'ReferenceSequencend', 'E-Value', 'BitScore']

    # Calculate new columns based on conditions
    df['newQuerySequenceStart'] = np.where(df['QuerySequenceEnd'] - df['QuerySequenceStart'] >= 0, df['QuerySequenceStart'], df['QuerySequenceEnd'])
    df['newQuerySequenceEnd'] = np.where(df['QuerySequenceEnd'] - df['QuerySequenceStart'] >= 0, df['QuerySequenceEnd'], df['QuerySequenceStart'])

    # Group the dataframe by 'QuerySequenceID'
    groups = df.groupby('QuerySequenceID')

    # Define a class 'Job' for job scheduling
    class Job:
        def __init__(self, start, finish, profit, row):
            self.start = start
            self.finish = finish
            self.profit = profit
            self.row = row

        def __repr__(self):
            return str((self.start, self.finish, self.profit))

    # Function to find non-overlapping jobs involved in maximum profit using the Longest Increasing Subsequence (LIS) algorithm
    def findMaxProfitJobs(jobs):
        # Base case: if no jobs, return 0 profit
        if not jobs:
            return 0

        # Sort the jobs by increasing start time
        jobs.sort(key=lambda x: x.start)

        # Get the number of jobs
        n = len(jobs)

        # Initialize lists to store tasks and maximum profit
        tasks = [[] for _ in range(n)]
        maxProfit = [0] * n

        # Consider every job
        for i in range(n):
            # Consider each job before the current one
            for j in range(i):
                # Update current job if the previous job is non-conflicting and leads to greater profit
                if jobs[j].finish <= jobs[i].start and maxProfit[i] < maxProfit[j]:
                    tasks[i] = tasks[j].copy()
                    maxProfit[i] = maxProfit[j]

            # End the current task with the i'th job
            tasks[i].append(i)
            maxProfit[i] += jobs[i].profit

        # Find the index with the maximum profit
        index = 0
        for i in range(1, n):
            if maxProfit[i] > maxProfit[index]:
                index = i

        # Print the jobs involved in the maximum profit and return their indices
        jobsToReturn = []
        for i in tasks[index]:
            print(jobs[i], end=' ')
            jobsToReturn.append(jobs[i].row)
        return jobsToReturn

    # Process each group in the dataframe
    for name, group in groups:
        jobsToFilter = []
        jobsToFilterdOut = []

        # Iterate through rows in the group
        for r_idx, row in group.iterrows():
            # Create a 'Job' object for each row and add it to the 'jobsToFilter' list
            jobsToFilter.append(Job(row.newQuerySequenceStart, row.newQuerySequenceEnd, row.PercentIdentity, row))
            data.append(row)

        # Find non-overlapping jobs with maximum profit
        jobsToFilterdOut = findMaxProfitJobs(jobsToFilter)

        # Add the filtered job indices to the 'filteredGroups' list
        for item in jobsToFilterdOut:
            filteredGroups.append(item)

    # Create a new dataframe from the filtered job indices
    filteredoutDataFrame = pd.DataFrame(filteredGroups)

    # Save the filtered dataframe to an Excel file with a '_sorted' suffix
    filteredoutDataFrame.to_excel('ICESingleGeneDataSorted/' + fileName + '_sorted.xlsx')

    # Save the original dataframe to an Excel file
    dforiginal.to_excel('ICESingleGeneDataNotSorted/' + fileName + '.xlsx')

    # Increment the counter and print a message indicating directory creation
    count += 1
    print("Directory '%s' created" % count)

# Print the 'array' (which appears to be empty)
for item in array:
    print(item)
