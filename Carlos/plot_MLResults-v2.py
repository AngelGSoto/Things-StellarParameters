# Data Visualization Libraries
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

def create_scatter_plot(ax, df, loc, colp, colt, norm, cmap, size_col, label, alpha=1, size_factor=10):
    normalized_teff = norm(df.loc[loc]['Teff'])
    scatter = ax.scatter(
        df.loc[loc][colp],
        df.loc[loc][colt + colp],
        c=normalized_teff,
        s=df.loc[loc][size_col] * size_factor,  # Adjust size by multiplying with size_factor
        cmap=cmap,
        edgecolors="k",
        zorder=2,
        lw=0.5,
        alpha=alpha,
    )
    return scatter

def create_colorbar(fig, ax, scatter, norm, cmap, label, position):
    cax = fig.add_axes(position)
    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=cax, orientation='horizontal', label=label)
    cbar.update_normal(scatter)
    return cbar

def plot_Measure_vs_Predicted(df, colp, cols, coln, colt, letp, xyinterval, suname, labname, directory_path,
                               cmap_dwarf="Blues", cmap_giant='Reds', size_factor=10):
    # Create hexbin-like plot using Seaborn
    sns.set(style="whitegrid")

    # Adjust figure size
    fig, ax = plt.subplots(figsize=(6, 6))

    # Plot for Dwarf
    loc_dwarf = df['Line_Label'] == 'Dwarf'
    norm_dwarf = Normalize(vmin=min(df.loc[loc_dwarf]['Teff']), vmax=max(df.loc[loc_dwarf]['Teff']))
    scatter_dwarf = create_scatter_plot(ax, df, loc_dwarf, colp, colt, norm_dwarf, cmap_dwarf, 'Logg', 'Teff (Dwarf)', size_factor=size_factor)

    # Plot for Giant
    loc_giant = df['Line_Label'] == 'Giant'
    norm_giant = Normalize(vmin=min(df.loc[loc_giant]['Teff']), vmax=max(df.loc[loc_giant]['Teff']))
    scatter_giant = create_scatter_plot(ax, df, loc_giant, colp, colt, norm_giant, cmap_giant, 'Logg', 'Teff (Giant)', size_factor=size_factor)

    # Set labels and limits
    ax.set(xlabel=cols, ylabel=f'{cols}$_{{\mathrm{{Predicted}}}}$', xlim=xyinterval[0:2], ylim=xyinterval[2:4])

    # Add colorbar for Dwarf
    cbar_dwarf = create_colorbar(fig, ax, scatter_dwarf, norm_dwarf, cmap_dwarf, 'Teff (Dwarf)', [0.16, 0.85, 0.35, 0.02])

    # Add colorbar for Giant
    cbar_giant = create_colorbar(fig, ax, scatter_giant, norm_giant, cmap_giant, 'Teff (Giant)', [0.51, 0.2, 0.35, 0.02])

    # Plot identity line
    xmean_values = np.linspace(xyinterval[0], xyinterval[1], 20)
    ax.plot(xmean_values, xmean_values, color='black', linestyle='--')

    # Add title outside the plot with adjusted vertical position
    plt.suptitle(f"{suname} (Test Data - N$_{{\mathrm{{D}}}}$: {len(df[loc_dwarf])}, N$_{{\mathrm{{G}}}}$: {len(df[loc_giant])})", y=0.92)

    # Save the figure
    plt.savefig(f"{directory_path}/{coln}_{suname}_{labname}_{colt}-v2.png", dpi=300)
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
plot_Measure_vs_Predicted(df, colp, cols, coln, colt, letp, xyinterval, suname, labname, directory_path, size_factor=15)
