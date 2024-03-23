import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use the path variable if needed
# path = '/media/carlosuda/udacfl02/carlos/work_files/vicluis2023/vicluis2023_tables/'
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
    'alpha_m_cnn': '[α/Fe] (CNN)',
    'c_fe': '[C/Fe]',
    'ca_fe': '[Ca/Fe]',
    'feh_cnn': '[Fe/H] (CNN)',
    'logg': 'Log(g)',
    'logg_cnn': 'Log(g) (CNN)',
    'mg_fe': '[Mg/Fe]',
    'n_fe': '[N/Fe]',
    'ni_fe': '[Ni/Fe]',
    'si_fe': '[Si/Fe]',
    'teff_cnn': 'Teff (CNN)',
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

        # Check if either NN or RF dataframe is empty
        if not subset_NN_df.empty or not subset_RF_df.empty:
            # Use a more distinctive color scheme
            axes[i, j].scatter(subset_NN_df['Parameter'], subset_NN_df['Score'], marker='o', s=150, label='NN', color='#1f77b4', alpha=0.8, zorder=2)
            axes[i, j].scatter(subset_RF_df['Parameter'], subset_RF_df['Score'], marker='s', s=150, label='RF', color='#d62728', alpha=0.8, zorder=1)

            # Plotting
            axes[i, j].set_ylabel('Accuracy', fontsize=14)
            axes[i, j].grid(True)
        
            # Replace current column labels with desired labels in the title
            full_survey_name = surveys_mapping.get(survey, survey)
            axes[i, j].set_title(f'{full_survey_name} - {star_type}', fontsize=16)
        
            # Check if any NN parameter has a score greater than or equal to 50
            if not subset_NN_df.empty:
                # Use NN parameters for x-axis ticks
                axes[i, j].set_xticks(range(len(subset_NN_df['Parameter'])))
                axes[i, j].set_xticklabels([column_labels_mapping.get(label, label) for label in subset_NN_df['Parameter']], rotation=45, ha='right', fontsize=14)
            else:
                # Use RF parameters for x-axis ticks
                axes[i, j].set_xticks(range(len(subset_RF_df['Parameter'])))
                axes[i, j].set_xticklabels([column_labels_mapping.get(label, label) for label in subset_RF_df['Parameter']], rotation=45, ha='right', fontsize=14)

            # Set y-axis limits
            axes[i, j].set_ylim([45, 105])  # Adjust as needed
        else:
            # Remove empty subplot
            fig.delaxes(axes[i, j])

# Place the legend outside the plot area with a background color
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper left', bbox_to_anchor=(1, 1), fontsize='x-large', fancybox=True, framealpha=0.7)

# Applying tick-related settings to each subplot
for ax in axes.flat:
    ax.tick_params(axis='x', labelsize=14, rotation=45)  # Rotate X-axis labels
    ax.tick_params(axis='y', labelsize=14)  # Set Y-axis label size
    ax.tick_params(axis='x', which='both', top=False, right=False)
    ax.tick_params(axis='y', which='both', top=False, right=False)

# Adjust the layout here to accommodate the title and legend
plt.tight_layout(rect=[0, 0, 1.1, 0.96])

# Save the plot with higher resolution and tight bounding box
plt.savefig('accuracy-justColors-50-100Obj.png', dpi=300, bbox_inches='tight')


