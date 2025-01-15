class ColorScaler:
    """Handles the generation of colors based on a scaling value."""

    RED_RGB = (255, 105, 97)
    BLUE_RGB = (179, 235, 242)

    def __init__(self, reverse=False):
        """
        Initialize the scaler with the color direction.

        Parameters
        ----------
        reverse : bool
            If True, scales from red to blue; otherwise, blue to red.
        """
        self.start_color = self.RED_RGB if reverse else self.BLUE_RGB
        self.end_color = self.BLUE_RGB if reverse else self.RED_RGB

    def get_color(self, normalized_value):
        """
        Generate a color based on a normalized value (0 to 1).

        Parameters
        ----------
        normalized_value : float
            A value between 0 and 1 indicating the position in the scale.

        Returns
        -------
        str
            The resulting color in `rgb(r, g, b)` format.
        """
        r1, g1, b1 = self.start_color
        r2, g2, b2 = self.end_color

        r = int(r1 + (r2 - r1) * normalized_value)
        g = int(g1 + (g2 - g1) * normalized_value)
        b = int(b1 + (b2 - b1) * normalized_value)

        return f"rgb({r}, {g}, {b})"


def normalize_value(value, vmin=0, vmax=1):
    """
    Normalize a value to the range [0, 1].

    Parameters
    ----------
    value : float
        The value to normalize.
    vmin : float, optional
        The minimum value of the range, default is 0.
    vmax : float, optional
        The maximum value of the range, default is 1.

    Returns
    -------
    float
        The normalized value in the range [0, 1].

    Notes
    -----
    If `vmax` is not greater than `vmin`, the normalized value defaults to 0.5.
    """
    if vmax > vmin:
        return max(0, min(1, (value - vmin) / (vmax - vmin)))
    return 0.5  # Default midpoint when range is invalid


def normalized_color_scale(value, reverse=False):
    """
    Generate a color between blue and red based on a normalized value.

    Parameters
    ----------
    value : float
        A value to normalize within [0, 1].
    reverse : bool, optional
        If True, scale from red to blue; otherwise, blue to red.

    Returns
    -------
    str
        The resulting color in `rgb(r, g, b)` format.
    """
    scaler = ColorScaler(reverse=reverse)
    normalized_value = normalize_value(value)
    return scaler.get_color(normalized_value)


def minmax_color_scale(value, vmin, vmax, reverse=False):
    """
    Generate a color based on a value relative to a specified range.

    Parameters
    ----------
    value : float
        The value to scale.
    vmin : float
        The minimum value of the range.
    vmax : float
        The maximum value of the range.
    reverse : bool, optional
        If True, scale from red to blue; otherwise, blue to red.

    Returns
    -------
    str
        The resulting color in `rgb(r, g, b)` format.
    """
    scaler = ColorScaler(reverse=reverse)
    normalized_value = normalize_value(value, vmin, vmax)
    return scaler.get_color(normalized_value)
