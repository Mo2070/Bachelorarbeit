"""Shared helpers for the three final notebooks.

Keeping the cluster definition, the colour scheme and the table renderer in one
place guarantees that all three notebooks use exactly the same logic.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


# Cluster colours, used consistently across every figure
GREEN = "#2E8B57"    # Advanced Digital Economies
ORANGE = "#E07B39"   # Catching-up Economies

# The seven indicators the clustering is based on.
# GDP is deliberately excluded because it is the dependent variable later on.
CLUSTER_VARS = [
    "Internet Access",
    "Internet Use",
    "Cloud Computing",
    "Fixed_Broadband",
    "Secure_Servers",
    "HighTech_Exports",
    "R&D expenditure",
]


def make_clusters(panel):
    """Assign each country to one of two clusters.

    K-Means (k=2) is run on the z-standardised country averages of CLUSTER_VARS.
    The cluster with the higher average GDP is named "Advanced Digital Economies",
    the other "Catching-up Economies", so the labels are stable regardless of the
    integer K-Means happens to assign.

    Returns the panel with a Cluster column merged in, the country-level table,
    the integer id of the advanced cluster, and the name/colour lookups.
    """
    country_means = panel.groupby("Country")[CLUSTER_VARS].mean()
    standardised = StandardScaler().fit_transform(country_means)
    country_means["Cluster"] = KMeans(n_clusters=2, random_state=42, n_init=10).fit(standardised).labels_

    # Which numeric label is the richer ("advanced") cluster?
    gdp_by_cluster = panel.merge(country_means[["Cluster"]], left_on="Country", right_index=True)
    advanced = gdp_by_cluster.groupby("Cluster")["GDP Per Capita PPS"].mean().idxmax()

    names = {advanced: "Advanced Digital Economies", 1 - advanced: "Catching-up Economies"}
    colors = {advanced: GREEN, 1 - advanced: ORANGE}
    country_means["Cluster_Name"] = country_means["Cluster"].map(names)

    panel = panel.merge(country_means[["Cluster"]], left_on="Country", right_index=True)
    return panel, country_means, advanced, names, colors


def save_table(rows, col_labels, out_path, title, row_labels=None, cell_colors=None,
               note=None, figsize=(12, 5), fontsize=9, col_widths=None):
    """Render a list of rows as a clean PNG table and save it to out_path (dpi=300)."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")

    table = ax.table(
        cellText=rows,
        colLabels=col_labels,
        rowLabels=row_labels,
        cellColours=cell_colors,
        cellLoc="center",
        loc="center",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(1, 1.4)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#BBBBBB")
        if col_widths is not None and col >= 0:
            cell.set_width(col_widths[col])
        # Bold the header row and the row labels; tint the header light blue.
        if row == 0 or col == -1:
            cell.set_text_props(fontweight="bold")
            if row == 0:
                cell.set_facecolor("#E3F2FD")

    ax.set_title(title, fontweight="bold", pad=14)
    if note:
        fig.text(0.5, 0.02, note, ha="center", fontsize=8, style="italic")
        fig.tight_layout(rect=[0, 0.05, 1, 1])
    else:
        fig.tight_layout()

    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.show()
