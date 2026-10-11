"""Sampling grid for the Land-or-Water eval."""

LAT_TOP = 88.0


def build_grid(step=4):
    """Return (lats, lons). Lats descend north -> south, lons ascend west -> east."""
    if 360 % step or 176 % step:
        raise ValueError("step must divide both 360 and 176 evenly")
    n_lat = int((LAT_TOP - (-LAT_TOP)) / step) + 1
    n_lon = int(360 / step)
    lats = [round(LAT_TOP - i * step, 6) for i in range(n_lat)]
    lons = [round(-180 + j * step, 6) for j in range(n_lon)]
    return lats, lons


def grid_points(lats, lons):
    """Row-major (north -> south) list of (lat, lon)."""
    return [(la, lo) for la in lats for lo in lons]
