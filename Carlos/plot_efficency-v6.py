import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('EfficiencyParameter_2023.csv')

# Extract unique surveys
surveys = df['#Survey'].unique()

# Iterate over surveys
for survey in surveys:
    # Filter data for the current survey
    survey_data = df[df['#Survey'] == survey]

    # Extract unique star types
    star_types = survey_data['StarType'].unique()

    # Iterate over star types
    for star_type in star_types:
        # Filter data for the current star type
        star_type_data = survey_data[survey_data['StarType'] == star_type]

        # Extract unique parameters
        parameters = star_type_data['Parameter'].unique()

        # Create subplots for each parameter
        fig, axes = plt.subplots(len(parameters), 2, figsize=(12, 3 * len(parameters)))
        plt.suptitle(f'{survey} - {star_type}', y=1.02)

        for i, parameter in enumerate(parameters):
            # Filter data for the current parameter
            parameter_data = star_type_data[star_type_data['Parameter'] == parameter]

            # Check if 'NNpredict_TEFF_LOGG' and 'RFpredict_TEFF_LOGG' are present
            if 'NNpredict_TEFF_LOGG' in parameter_data['PredType'].values:
                nn_data = parameter_data[parameter_data['PredType'] == 'NNpredict_TEFF_LOGG']
            else:
                nn_data = parameter_data[parameter_data['PredType'] == 'NNpredict']

            if 'RFpredict_TEFF_LOGG' in parameter_data['PredType'].values:
                rf_data = parameter_data[parameter_data['PredType'] == 'RFpredict_TEFF_LOGG']
            else:
                rf_data = parameter_data[parameter_data['PredType'] == 'RFpredict']

            # Plot the data
            xtick_positions = range(len(nn_data))
            axes[i, 0].bar(xtick_positions - 0.2, nn_data['Score'], width=0.4, label='NN')
            axes[i, 0].bar(xtick_positions + 0.2, rf_data['Score'], width=0.4, label='RF')
            axes[i, 0].set_title(f'{parameter} - {star_type} - {survey}')
            axes[i, 0].legend()

            # Plot other relevant information if needed
            # axes[i, 1].plot(...)
            # axes[i, 1].set_title('Other Information')

        plt.tight_layout()
        plt.show()
