import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use the path variable if needed
# path = '/media/carlosuda/udacfl02/carlos/work_files/vicluis2023/vicluis2023_tables/'
df = pd.read_csv('EfficiencyParameter_2023.csv')

# Print columns in a more readable format
print('\nColumns:', df.columns)

# List of surveys and star types
surveys = ["Apogee", "Galah", "LamostMedium"]
star_types = ['Giant', 'Dwarf']

# Unique parameters from the DataFrame
parameters = np.unique(df["Parameter"])

# Create subplots
fig, axes = plt.subplots(nrows=len(surveys), ncols=len(star_types), figsize=(12, 8))

# Loop through surveys and star types
for i, survey in enumerate(surveys):
    for j, star_type in enumerate(star_types):
        # Filter the DataFrame
        subset_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["Parameter"].isin(parameters)) & (df["PredType"] == "NNpredict")]
        
        print(f'\nSubset DataFrame for {survey} - {star_type}:')
        print(subset_df)

        
