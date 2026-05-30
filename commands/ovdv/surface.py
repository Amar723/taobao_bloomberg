import pandas as pd
import numpy as np
from scipy.interpolate import RBFInterpolator

def build_surface(df: pd.DataFrame):
    # OTM convention: puts left of ATM, calls right
    otm = pd.concat([
        df[(df["type"] == "put")  & (df["log_moneyness"] <= 0)],
        df[(df["type"] == "call") & (df["log_moneyness"] >  0)],
    ])

    # deduplicate: if same expiry+strike appears twice, keep higher volume
    otm = otm.sort_values("volume", ascending=False)
    otm = otm.drop_duplicates(subset=["expiry", "strike"])

    # need enough points to interpolate
    if len(otm) < 10:
        raise ValueError("Not enough liquid options data to build surface")

    points = otm[["moneyness", "dte_years"]].values
    values = otm["iv"].values

    # higher smoothing = smoother surface, less overfitting to noise
    interp = RBFInterpolator(points, values, kernel="thin_plate_spline", smoothing=5.0)

    # grid matching Bloomberg axes
    moneyness_grid = np.linspace(60, 150, 60)    # 60% to 150% moneyness
    dte_grid       = np.linspace(0.05, 2.0, 40)  # ~18 days to 2 years

    MN, DTE = np.meshgrid(moneyness_grid, dte_grid)
    grid_pts = np.column_stack([MN.ravel(), DTE.ravel()])
    IV_grid  = interp(grid_pts).reshape(MN.shape)
    IV_grid  = np.clip(IV_grid, 0.01, 1.5)

    return moneyness_grid, dte_grid, IV_grid