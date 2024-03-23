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

# Improved subplot size
fig, axes = plt.subplots(nrows=len(surveys), ncols=len(star_types), figsize=(12, 8))

# Loop through surveys and star types
for i, survey in enumerate(surveys):
    for j, star_type in enumerate(star_types):
        # Filter the DataFrame
        subset_NN_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["PredType"] == 'NNpredict')]
        subset_RF_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["PredType"] == 'RFpredict')]

        # Use a more distinctive color scheme
        axes[i, j].errorbar(range(len(subset_NN_df['Parameter'])), subset_NN_df['Score'], yerr=subset_NN_df['StdMean'] / 10.0, fmt='o', color='#1f77b4', capsize=4, alpha=0.8, label='NN', markersize=8, zorder=2)
        axes[i, j].errorbar(range(len(subset_RF_df['Parameter'])), subset_RF_df['Score'], yerr=subset_RF_df['StdMean'] / 10.0, fmt='s', color='#d62728', capsize=4, alpha=0.8, label='RF', markersize=8, zorder=1)

        # Plotting
        axes[i, j].set_ylabel('Accuracy')
        axes[i, j].grid(True)
        axes[i, j].set_title(f'{survey} - {star_type}')
        axes[i, j].set_xticks(range(len(subset_NN_df['Parameter'])))  # Set the tick positions
        axes[i, j].set_xticklabels(subset_NN_df['Parameter'], rotation=45, ha='right')

# Place the legend outside the plot area
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize='x-large')

#fig.suptitle('Comparison of RF and NN', fontsize=16)

# Applying tick-related settings to each subplot
for ax in axes.flat:
    ax.tick_params(axis='x', labelsize='small', rotation=45)  # Rotate X-axis labels
    ax.tick_params(axis='y', labelsize='small')  # Set Y-axis label size
    ax.tick_params(axis='x', which='both', top=False, right=False)
    ax.tick_params(axis='y', which='both', top=False, right=False)

# Adjust the layout here to accommodate the title and legend
plt.tight_layout(rect=[0, 0, 1.1, 0.96])

# Save the plot with higher resolution and tight bounding box
plt.savefig('accuracy-justColors.png', dpi=300, bbox_inches='tight')

