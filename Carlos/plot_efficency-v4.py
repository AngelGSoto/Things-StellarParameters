import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use the path variable if needed
# path = '/media/carlosuda/udacfl02/carlos/work_files/vicluis2023/vicluis2023_tables/'
df = pd.read_csv('EfficiencyParameter_2023.csv')
# df['Score'] = df['Score'] * 100

# Filter the DataFrame to include only parameters with a score <= 60
df_filtered = df[df['Score'] >= 60]

# Print columns in a more readable format
print('\nColumns:', df.columns)

# List of surveys and star types
surveys = ["Apogee", "Galah", "LamostMedium"]
star_types = ['Giant', 'Dwarf']

# Unique parameters from the filtered DataFrame
parameters = np.unique(df_filtered["Parameter"])

# Create subplots
fig, axes = plt.subplots(nrows=len(surveys), ncols=len(star_types), figsize=(12, 8))

# Loop through surveys and star types
for i, survey in enumerate(surveys):
    for j, star_type in enumerate(star_types):
        # Filter the filtered DataFrame
        subset_NN_df = df_filtered[(df_filtered['#Survey'] == survey) & (df_filtered['StarType'] == star_type) & (df_filtered["Parameter"].isin(parameters)) & (df_filtered["PredType"] == "NNpredict")]
        subset_RF_df = df_filtered[(df_filtered['#Survey'] == survey) & (df_filtered['StarType'] == star_type) & (df_filtered["Parameter"].isin(parameters)) & (df_filtered["PredType"] == "RFpredict")]

        print(f'\nSubset DataFrame for {survey} - {star_type}:')
        print(subset_NN_df)

        # Add your error parameters here..
        axes[i, j].errorbar(subset_NN_df['Parameter'], subset_NN_df['Score'], yerr=subset_NN_df['StdMean'] / 10.0, fmt='o', color='blue', capsize=4, alpha=0.5, label='NN', markersize=8, zorder=2)
        axes[i, j].errorbar(subset_RF_df['Parameter'], subset_RF_df['Score'], yerr=subset_RF_df['StdMean'] / 10.0, fmt='s', color='red', capsize=4, alpha=0.5, label='RF', markersize=8, zorder=1)

        # Plotting
        axes[i, j].set_ylabel('Score')
        axes[i, j].grid(True)
        axes[i, j].set_title(f'{survey} - {star_type}')
        # axes[i, j].set_yscale('log')  # Set Y-axis to log scale
        axes[i, j].set_xticklabels(subset_NN_df['Parameter'], rotation=45, ha='right')

handles, labels = axes[0, 0].get_legend_handles_labels()

# Move the legend outside the plot area
fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1))
fig.suptitle('Comparison of RF and NN', fontsize=16)

# Applying tick-related settings to each subplot
for ax in axes.flat:
    ax.tick_params(axis='x', labelsize='small', rotation=45)  # Rotate X-axis labels
    ax.tick_params(axis='y', labelsize='small')  # Set Y-axis label size
    ax.tick_params(axis='x', which='both', top=False, right=False)
    ax.tick_params(axis='y', which='both', top=False, right=False)

# Adjust the layout here to accommodate the title and legend ...
plt.tight_layout(rect=[0, 0, 1.1, 0.96])
plt.savefig('plot2.png', dpi=300, bbox_inches='tight')
plt.show()
