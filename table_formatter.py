import pandas as pd
from IPython.core.display import HTML
from functools import partial

from color_scaler import minmax_color_scale, normalized_color_scale

color_scaler_map_ = {"minmax": minmax_color_scale, "normalized": normalized_color_scale}

COOL_GRAY_HEX = "#242525"


def heatmap_dataframe(
    df: pd.DataFrame,
    scaler="minmax",
    reverse=False,
) -> pd.io.formats:
    """
    Formats a pandas DataFrame as an HTML table with a heatmap.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame with values between 0 and 1.
    scaler: str, optional
        Defines how color palette is created. Supports "minmax" and "normalized". Default value is "minmax".
    reverse : bool, optional
        If True, reverses the color scale. Values closer to 0 are #FF6961, and values closer to 1 are #B3EBF2 (default is False).


    Returns
    -------
    pd.io.formats.style.Styler
        A Styler object that represents the DataFrame with heatmap formatting.
    """

    color_scale = partial(color_scaler_map_[scaler], reverse=reverse)

    if scaler == "minmax":

        def apply_column_colors(col):
            """Apply color formatting for a single column."""
            vmin, vmax = col.min(), col.max()
            return [
                f"background-color: {color_scale(val, vmin, vmax)}; color: #242525"
                for val in col
            ]

        styled_df = df.style.apply(apply_column_colors, axis=0)

    elif scaler == "normalized":

        def apply_color(val):
            """Apply color formatting for a single cell."""
            color = color_scale(val)
            return f"background-color: {color}; color: {COOL_GRAY_HEX}"

        styled_df = df.style.applymap(lambda x: apply_color(x))

    else:
        raise ValueError("Unsupported scaler. Choose between 'minmax' or 'normalized'.")
    return styled_df
