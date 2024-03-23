# Data Visualization Libraries
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_Measure_vs_Predicted(df, colp, cols, coln, colt, letp, xyinterval, suname, labname, directory_path):
    # Create hexbin-like plot using Seaborn
    sns.set(style="whitegrid")

    # Adjust figure size
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot for Dwarf
    loc_dwarf = df['Line_Label'] == 'Dwarf'
    scatter_dwarf = sns.scatterplot(
        data=df.loc[loc_dwarf], x=colp, y=colt + colp,
        hue=df.loc[loc_dwarf]['Teff'], palette='Blues',
        s=10, alpha=0.60, edgecolor='darkblue',
        size=df.loc[loc_dwarf]['Teff'], sizes=(20, 50), legend=False
    )

    # Plot for Giant
    loc_giant = df['Line_Label'] == 'Giant'
    scatter_giant = sns.scatterplot(
        data=df.loc[loc_giant], x=colp, y=colt + colp,
        hue=df.loc[loc_giant]['Teff'], palette='Reds',
        s=10, alpha=0.60, edgecolor='darkred',
        size=df.loc[loc_giant]['Teff'], sizes=(20, 50), legend=False
    )

    # Set labels and limits
    ax.set(xlabel=cols, ylabel=f'{cols}$_{{\mathrm{{Predicted}}}}$', xlim=xyinterval[0:2], ylim=xyinterval[2:4])

    # Add colorbar for Dwarf
    cax_dwarf = fig.add_axes([0.16, 0.85, 0.35, 0.02])
    cbar_dwarf = plt.colorbar(cax=cax_dwarf, mappable=scatter_dwarf.collections[0], orientation='horizontal', label='Teff (Dwarf)')

    # Add colorbar for Giant
    cax_giant = fig.add_axes([0.51, 0.2, 0.35, 0.02])
    cbar_giant = plt.colorbar(cax=cax_giant, mappable=scatter_giant.collections[0], orientation='horizontal', label='Teff (Giant)')

    # Plot identity line
    xmean_values = np.linspace(xyinterval[0], xyinterval[1], 20)
    ax.plot(xmean_values, xmean_values, color='black', linestyle='--')

    # Add title outside the plot with adjusted vertical position
    plt.suptitle(f"{suname} (Test Data - N$_{{\mathrm{{D}}}}$: {len(df[loc_dwarf])}, N$_{{\mathrm{{G}}}}$: {len(df[loc_giant])})", y=0.92)

    # Save the figure
    plt.savefig(f"{directory_path}/{coln}_{suname}_{labname}_{colt}.png", dpi=300)
    print(f"{directory_path}/{coln}_{suname}_{labname}_{colt}.png")

    # Adjust layout
    # plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # Adjust the rect parameter based on your needs

    # Show the plot
    # plt.show()

# Assuming 'df' is your concatenated dataframe
# Replace the following lines with your actual data loading logic

df_file0 = 'RFresults_Apogee_Giant_ALPHA_M.csv'
df_file1 = 'RFresults_Apogee_Dwarf_ALPHA_M.csv'
df_dwarf = pd.read_csv(df_file0)
df_giant = pd.read_csv(df_file1)
df_dwarf = df_dwarf[df_dwarf['split'] == 'test']
df_giant = df_giant[df_giant['split'] == 'test']
df = pd.concat([df_dwarf, df_giant], ignore_index=True)

# Parameters
colp = 'ALPHA_M'
cols = '[$\\alpha$/M]'
coln = 'ALPHA_M'
colt = 'RFpredict_'
letp = '(a)'
xyinterval = [-0.2, 0.4, -0.2, 0.4]
suname = 'Apogee'
labname = 'Measure_vs_Predicted_NN'
directory_path = 'Plots/'  # your directory

# Plotting
plot_Measure_vs_Predicted(df, colp, cols, coln, colt, letp, xyinterval, suname, labname, directory_path)
