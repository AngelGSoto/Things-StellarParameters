import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use the path variable if needed
# path = '/media/carlosuda/udacfl02/carlos/work_files/vicluis2023/vicluis2023_tables/'
df = pd.read_csv('EfficiencyParameter_2023.csv')
# df['Score'] = df['Score'] * 100

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
        # Set default conditions
        nn_condition = "NNpredict" 
        rf_condition = "RFpredict"

        # Check if specific conditions exist for NN
        nn_condition += "_TEFF_LOGG" if any("NNpredict_TEFF_LOGG" in pred_type for pred_type in df["PredType"]) else ""

        # Check if specific conditions exist for RF
        rf_condition += "_TEFF_LOGG" if any("RFpredict_TEFF_LOGG" in pred_type for pred_type in df["PredType"]) else ""

        print(f'\nConditions for {survey} - {star_type}:')
        print(f'NN Condition: {nn_condition}')
        print(f'RF Condition: {rf_condition}')

        # Filter the DataFrame for each survey and star type
        subset_NN_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["Parameter"].isin(parameters)) & (df["PredType"] == nn_condition)]
        subset_RF_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["Parameter"].isin(parameters)) & (df["PredType"] == rf_condition)]

        print(f'\nSubset DataFrame for {survey} - {star_type} (NN):')
        print(subset_NN_df[['Parameter', 'Score']])

        print(f'\nSubset DataFrame for {survey} - {star_type} (RF):')
        print(subset_RF_df[['Parameter', 'Score']])

        # Add your error parameters here...
        axes[i, j].errorbar(subset_NN_df['Parameter'], subset_NN_df['Score'], yerr=subset_NN_df['StdMean'] / 10.0, fmt='o', color='blue', capsize=4, alpha=0.5, label='NN', markersize=8, zorder=2)
        axes[i, j].errorbar(subset_RF_df['Parameter'], subset_RF_df['Score'], yerr=subset_RF_df['StdMean'] / 10.0, fmt='s', color='red', capsize=4, alpha=0.5, label='RF', markersize=8, zorder=1)

        # Plotting
        axes[i, j].set_ylabel('Accuracy')
        axes[i, j].grid(True)
        axes[i, j].set_title(f'{survey} - {star_type}')
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

# Adjust the layout here to accommodate the title and legend...
plt.tight_layout(rect=[0, 0, 1.1, 0.96])
plt.savefig('plot2.png', dpi=300, bbox_inches='tight')
