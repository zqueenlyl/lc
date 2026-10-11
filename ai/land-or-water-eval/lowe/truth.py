"""Ground truth: point-in-polygon against Natural Earth land polygons."""

from pathlib import Path as FsPath

import numpy as np
import shapefile
from matplotlib.path import Path as MplPath


def _shape_to_path(shape):
    """One matplotlib Path per shapefile record; all rings kept so even-odd
    fill makes interior holes (e.g. Caspian Sea) count as non-land."""
    pts = shape.points
    starts = list(shape.parts) + [len(pts)]
    verts, codes = [], []
    for a, b in zip(starts[:-1], starts[1:]):
        ring = pts[a:b]
        if len(ring) < 3:
            continue
        verts.append(ring[0])
        codes.append(MplPath.MOVETO)
        for p in ring[1:]:
            verts.append(p)
            codes.append(MplPath.LINETO)
        verts.append(ring[0])
        codes.append(MplPath.CLOSEPOLY)
    if not verts:
        return None
    arr = np.asarray(verts, dtype=float)
    return MplPath(arr, codes)


class LandTruth:
    def __init__(self, shp_path):
        shp_path = FsPath(shp_path)
        sf = shapefile.Reader(str(shp_path))
        self.shapes = []
        self.paths = []
        for sr in sf.iterShapes():
            p = _shape_to_path(sr)
            if p is None:
                continue
            v = p.vertices
            self.shapes.append(v)
            self.paths.append((v[:, 0].min(), v[:, 1].min(), v[:, 0].max(), v[:, 1].max(), p))

    def is_land(self, pts):
        """pts: sequence of (lat, lon). Returns bool ndarray, True = land."""
        xy = np.asarray([[lo, la] for la, lo in pts], dtype=float)
        out = np.zeros(len(xy), dtype=bool)
        for x0, y0, x1, y1, p in self.paths:
            sel = (~out) & (xy[:, 0] >= x0) & (xy[:, 0] <= x1) & (xy[:, 1] >= y0) & (xy[:, 1] <= y1)
            if sel.any():
                out[sel] |= p.contains_points(xy[sel])
        return out
