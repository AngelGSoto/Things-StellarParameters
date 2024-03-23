import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data from CSV
df = pd.read_csv('EfficiencyParameter_2023.csv')

# Filter out rows with NumObjects < 100
df = df[df['NumObjects'] >= 100]

# Print columns in a more readable format
print('\nColumns:', df.columns)

# Mapping current column labels to desired labels
column_labels_mapping = {
     'ALPHA_M': '[α/Fe]',
    'AL_FE': '[Al/Fe]',
    'CA_FE': '[Ca/Fe]',
    'CE_FE': '[Ce/Fe]',
    'CI_FE': '[Ci/Fe]',
    'CO_FE': '[Co/Fe]',
    'CR_FE': '[Cr/Fe]',
    'C_FE': '[C/Fe]',
    'FE_H': '[Fe/H]',
    'K_FE': '[K/Fe]',
    'LOGG': 'Log(g)',
    'MG_FE': '[Mg/Fe]',
    'MN_FE': '[Mn/Fe]',
    'NA_FE': '[Na/Fe]',
    'NI_FE': '[Ni/Fe]',
    'N_FE': '[N/Fe]',
    'O_FE': '[O/Fe]',
    'SI_FE': '[Si/Fe]',
    'TEFF': 'Teff',
    'TIII_FE': '[Ti/Fe]',
    'TI_FE': '[Ti/Fe]',
    'Teff': 'Teff',  # Assuming 'Teff' and 'TIII_FE' are both temperature columns
    'V_FE': '[V/Fe]',
    '[Al/Fe]': '[Al/Fe]',
    '[C/Fe]': '[C/Fe]',
    '[Ca/Fe]': '[Ca/Fe]',
    '[Co/Fe]': '[Co/Fe]',
    '[Cr/Fe]': '[Cr/Fe]',
    '[Cu/Fe]': '[Cu/Fe]',
    '[Fe/H]': '[Fe/H]',
    '[K/Fe]': '[K/Fe]',
    '[Li/Fe]': '[Li/Fe]',
    '[Mg/Fe]': '[Mg/Fe]',
    '[Mn/Fe]': '[Mn/Fe]',
    '[Na/Fe]': '[Na/Fe]',
    '[Ni/Fe]': '[Ni/Fe]',
    '[O/Fe]': '[O/Fe]',
    '[Sc/Fe]': '[Sc/Fe]',
    '[Si/Fe]': '[Si/Fe]',
    '[Ti/Fe]': '[Ti/Fe]',
    '[Ti2/Fe]': '[Ti2/Fe]',
    '[Y/Fe]': '[Y/Fe]',
    '[Zn/Fe]': '[Zn/Fe]',
    '[alpha/Fe]': '[α/Fe]',
    'alpha_m_cnn': '[α/Fe]',
    'c_fe': '[C/Fe]',
    'ca_fe': '[Ca/Fe]',
    'feh_cnn': '[Fe/H]',
    'logg': 'Log(g)',
    'logg_cnn': 'Log(g) ',
    'mg_fe': '[Mg/Fe]',
    'n_fe': '[N/Fe]',
    'ni_fe': '[Ni/Fe]',
    'si_fe': '[Si/Fe]',
    'teff_cnn': 'Teff',
}

# List of surveys and star types
surveys = ["Apogee", "Galah", "LamostMedium"]
star_types = ['Giant', 'Dwarf']

# Mapping survey names to desired names
surveys_mapping = {
      "Apogee": "APOGEE",
    "Galah": "GALAH",
    "LamostMedium": "LAMOST MRS",
}

# Improved subplot size
fig, axes = plt.subplots(nrows=len(surveys), ncols=len(star_types), figsize=(14, 10))

# Loop through surveys and star types
for i, survey in enumerate(surveys):
    for j, star_type in enumerate(star_types):
        # Filter the DataFrame for NN with Score >= 50
        subset_NN_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["PredType"] == 'NNpredict') & (df['Score'] >= 50)]
        
        # Filter the DataFrame for RF with Score >= 50
        subset_RF_df = df[(df['#Survey'] == survey) & (df['StarType'] == star_type) & (df["PredType"] == 'RFpredict') & (df['Score'] >= 50)]
        
        # Check if subset dataframes are not empty
        if not subset_NN_df.empty or not subset_RF_df.empty:
            # Plot NN and RF points
            axes[i, j].scatter(subset_NN_df['Parameter'], subset_NN_df['Score'], marker='o', s=190, edgecolor='blue', label='NN', color='#1f77b4', alpha=0.8, zorder=2)
            axes[i, j].scatter(subset_RF_df['Parameter'], subset_RF_df['Score'], marker='s', s=190, edgecolor='red', label='RF', color='#d62728', alpha=0.9, zorder=1)

            # Plot settings
            axes[i, j].set_ylabel('Accuracy', fontsize=14)
            axes[i, j].tick_params(axis='x', labelsize=14) 
            axes[i, j].tick_params(axis='y', labelsize=14)
            axes[i, j].grid(True)
            full_survey_name = surveys_mapping.get(survey, survey)
            axes[i, j].set_title(f'{full_survey_name} - {star_type}', fontsize=16)
            if not subset_NN_df.empty:
                axes[i, j].set_xticks(range(len(subset_NN_df['Parameter'])))
                axes[i, j].set_xticklabels([column_labels_mapping.get(label, label) for label in subset_NN_df['Parameter']], rotation=45, ha='right', fontsize=14)
            else:
                axes[i, j].set_xticks(range(len(subset_RF_df['Parameter'])))
                axes[i, j].set_xticklabels([column_labels_mapping.get(label, label) for label in subset_RF_df['Parameter']], rotation=45, ha='right', fontsize=14)
        else:
            # If both subsets are empty, remove the subplot
            fig.delaxes(axes[i, j])


# Set y-axis limits between 50 and 100 for all subplots
for ax_row in axes:
    for ax in ax_row:
        ax.set_ylim(45, 105)
        
# Place the legend outside the plot area with a background color
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize='x-large', fancybox=True, framealpha=0.7)

# Adjust the layout here to accommodate the title and legend
plt.tight_layout(rect=[0, 0, 1.1, 0.96])

# Save the plot with higher resolution and tight bounding box
plt.savefig('accuracy-justColors-50-100Obj.png', bbox_inches='tight') #dpi=300,
