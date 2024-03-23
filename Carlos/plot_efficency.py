import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use the path variable if needed
# path = '/media/carlosuda/udacfl02/carlos/work_files/vicluis2023/vicluis2023_tables/'
df = pd.read_csv('EfficiencyParameter_2023.csv')
df['Score'] = df['Score'] *100

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
        subset_NN_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["Parameter"].isin(parameters)) & (df["PredType"] == "NNpredict")]
        subset_RF_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["Parameter"].isin(parameters)) & (df["PredType"] == "RFpredict")]

        print(f'\nSubset DataFrame for {survey} - {star_type}:')
        print(subset_NN_df)
         # Add your error parameters here..
        axes[i, j].errorbar(subset_NN_df['Parameter'], subset_NN_df['StdMean'], yerr=subset_NN_df['Score']/10.0, fmt='none', color='blue', capsize=2, alpha=0.3)
        axes[i, j].errorbar(subset_RF_df['Parameter'], subset_RF_df['StdMean'], yerr=subset_RF_df['Score']/10.0, fmt='none', color='blue', capsize=2, alpha=0.3)       

        # Plotting
        axes[i, j].scatter(subset_NN_df['Parameter'], subset_NN_df['StdMean'], label='NN', color='blue')
        axes[i, j].scatter(subset_RF_df['Parameter'], subset_RF_df['StdMean'], label='RF', color='red')
        #axes[i, j].bar(subset_df['Parameter'], subset_df['Score'])
        axes[i, j].set_ylabel('Score')
        axes[i, j].grid(True)
        axes[i, j].set_title(f'{survey} - {star_type}')
        axes[i, j].set_yscale('log')  # Set Y-axis to log scale
        axes[i, j].set_xticklabels(subset_NN_df['Parameter'], rotation=90, ha='center')

handles, labels = axes[0, 0].get_legend_handles_labels()

fig.legend(handles, labels, loc='upper right')
fig.suptitle('Comparision of RF and NN', fontsize=16)

# Applying tick-related settings to each subplot
for ax in axes.flat:
    ax.tick_params(axis='x', labelsize='small')
    ax.tick_params(axis='y', which='both', top=False)
    ax.tick_params(axis='x', which='both', right=False)

for ax in axes.flat:
    ax.tick_params(axis='x', labelsize='small', rotation=90)  # Rotate X-axis labels
    ax.tick_params(axis='y', labelsize='small')  # Set Y-axis label size
    ax.tick_params(axis='x', which='both', top=False, right=False)
    ax.tick_params(axis='y', which='both', top=False, right=False)
# Adjust the layout here to accommodate the title and legend ...
plt.tight_layout(rect=[0, 0, 1, 0.96])  
plt.savefig('plot2.png', dpi=300)
