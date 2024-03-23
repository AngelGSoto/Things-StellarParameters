# Data Visualization Libraries
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable

def create_scatter_plot(ax, df, loc, colp, colt, norm, cmap, size_col, label, alpha=1, size_factor=10):
    normalized_teff = norm(df.loc[loc]['Teff'])
    scatter = ax.scatter(
        df.loc[loc][colp],
        df.loc[loc][colt + colp],
        c=normalized_teff,
        s=df.loc[loc][size_col] * size_factor,
        cmap=cmap,
        edgecolors="k",
        zorder=2,
        lw=0.5,
        alpha=alpha,
    )
    return scatter

def create_colorbar(ax, scatter, label, orientation, position='right', label_position='top', tick_position='top'):
    if position == 'right':
        cbar = plt.colorbar(scatter, ax=ax, orientation=orientation, pad=0.03, format='%.1f')
    elif position == 'above':
        # Create a divider for the existing axes instance
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("top", size="5%", pad=0.1)
        
        # Add colorbar to the new axes
        cbar = plt.colorbar(scatter, cax=cax, orientation=orientation, format='%.1f')
    
    cbar.set_label(label, fontsize=12, labelpad=5)  # Label for the colorbar with adjusted padding
    cbar.ax.tick_params(labelsize=12, pad=5)  # Adjust the font size and padding for ticks
    
    if label_position == 'top':
        cbar.ax.xaxis.set_label_position('top')  # Place the label at the top of the colorbar
        
    if tick_position == 'top':
        cbar.ax.xaxis.tick_top()  # Place the ticks at the top of the colorbar
    
    return cbar

def plot_Measure_vs_Predicted(df, colp, cols, coln, colt, letp, xyinterval, suname, labname, directory_path,
                               cmap_dwarf="Blues", cmap_giant='Reds', size_factor=10):
    # Create hexbin-like plot using Seaborn
    sns.set(style="whitegrid")

    # Adjust figure size
    fig = plt.figure(figsize=(6, 6.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[4, 1.], hspace=0.07)  # Adjust the width of the subplot
    ax = fig.add_subplot(gs[0])

    # Plot for Dwarf
    loc_dwarf = df['Line_Label'] == 'Dwarf'
    norm_dwarf = Normalize(vmin=min(df.loc[loc_dwarf]['Teff']), vmax=max(df.loc[loc_dwarf]['Teff']))
    scatter_dwarf = create_scatter_plot(ax, df, loc_dwarf, colp, colt, norm_dwarf, cmap_dwarf, 'Logg', 'Teff (Dwarf)', size_factor=size_factor)

    # Plot for Giant
    loc_giant = df['Line_Label'] == 'Giant'
    norm_giant = Normalize(vmin=min(df.loc[loc_giant]['Teff']), vmax=max(df.loc[loc_giant]['Teff']))
    scatter_giant = create_scatter_plot(ax, df, loc_giant, colp, colt, norm_giant, cmap_giant, 'Logg', '$Teff (Giant)', size_factor=size_factor)

    # Set labels and limits
    ax.set(ylabel=f'{cols}$_{{\mathrm{{Predicted}}}}$', xlim=xyinterval[0:2], ylim=xyinterval[2:4])
    ax.set_xticks([])

    # Remove grid
    ax.grid(False)

    # Add colorbar for Dwarf on the right side
    cbar_dwarf = create_colorbar(ax, scatter_dwarf, 'Norm. $T_\mathrm{eff}$ (Dwarf)', "vertical", position='right')

    # Add colorbar for Giant above the plot
    cbar_giant = create_colorbar(ax, scatter_giant, 'Norm. $T_\mathrm{eff}$ (Giant)', "horizontal", position='above', label_position='top', tick_position='top')
 
    # Plot identity line
    xmean_values = np.linspace(xyinterval[0], xyinterval[1], 20)
    ax.plot(xmean_values, xmean_values, color='black', linestyle='--', linewidth=1.5)

    # Add subplot for the difference
    ax_diff = fig.add_subplot(gs[1])
    ax_diff.set_xlim(xyinterval[0:2])  # Set x-axis limits
    ax_diff.set_ylim(xyinterval[4], xyinterval[5])  # Set y-axis limits from -0.5 to 0.5

    diff_dwarf = df.loc[loc_dwarf][colp] - df.loc[loc_dwarf][colt + colp]
    diff_giant = df.loc[loc_giant][colp] - df.loc[loc_giant][colt + colp]

    # Scatter plot for difference with color reflecting logg
    scatter_diff_dwarf = ax_diff.scatter(df.loc[loc_dwarf][colp], diff_dwarf, c=df.loc[loc_dwarf]['Teff'], cmap=cmap_dwarf, edgecolor='black', alpha=1, lw=0.5, s=df.loc[loc_dwarf]['Logg'] * size_factor)
    scatter_diff_giant = ax_diff.scatter(df.loc[loc_giant][colp], diff_giant, c=df.loc[loc_giant]['Teff'], cmap=cmap_giant, edgecolor='black', alpha=1, lw=0.5, s=df.loc[loc_giant]['Logg'] * size_factor)
    # Add colorbar for Dwarf on the right side
    cbar_dwarf_diff = create_colorbar(ax_diff,  scatter_diff_dwarf, 'Norm. $T_\mathrm{eff}$ (Dwarf)', "vertical", position='right')

    cbar_dwarf_diff.ax.set_visible(False)

    
    # Add text annotation to the subplot in the lower right corner
    text_x = xyinterval[1] - 0.01  # Adjust as needed
    text_y = xyinterval[2] - 0.3  # Adjust as needed
    ax_diff.text(text_x, text_y, "Symbol size represents $\log g$", ha='right', va='bottom', fontsize=11, color='black')

    ax_diff.set(ylabel=f'$\\Delta${cols}')
    ax_diff.set_xlabel(cols)

    # Remove grid from the subplot
    ax_diff.grid(False)

    # Add horizontal dashed line through 0 point in the y-axis
    ax_diff.axhline(0, color='black', linestyle='--', linewidth=1.5)

    # Add title outside the plot with adjusted vertical position
    plt.suptitle(f"{suname} (Test Data - N$_{{\mathrm{{D}}}}$: {len(df[loc_dwarf])}, N$_{{\mathrm{{G}}}}$: {len(df[loc_giant])})", y=1)

    # Save the figure with tight layout
    fig.savefig(f"{directory_path}/{coln}_{suname}_{labname}_{colt}.png", dpi=300, bbox_inches='tight')
    print(f"{directory_path}/{coln}_{suname}_{labname}_{colt}.png")

    # If you still encounter the warning, you can try adjusting subplot parameters manually
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)


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
xyinterval = [-0.2, 0.4, -0.2, 0.4, -0.5, 0.5]
suname = 'Apogee'
labname = 'Measure_vs_Predicted_NN'
directory_path = 'Plots/'  # your directory

# Plotting
plot_Measure_vs_Predicted(df, colp, cols, coln, colt, letp, xyinterval, suname, labname, directory_path, size_factor=14)
