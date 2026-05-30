import yfinance as yf
import pandas as pd
import numpy as np

def get_vol_surface(ticker_sym: str):
    ticker = yf.Ticker(ticker_sym)
    spot = ticker.history(period="1d")["Close"].iloc[-1]

    rows = []
    for exp_date in ticker.options:
        chain = ticker.option_chain(exp_date)
        for opt_type, df in [("call", chain.calls), ("put", chain.puts)]:
            df = df.copy()
            # aggressive filtering to remove bad data points
            df = df[df["impliedVolatility"] > 0.02]
            df = df[df["impliedVolatility"] < 1.5]      # cap absurd IVs
            df = df[df["volume"] > 50]
            df = df[df["openInterest"] > 100]
            df = df[df["bid"] > 0.05]                   # must have real bid
            df = df[(df["ask"] - df["bid"]) / df["ask"] < 0.5]  # tight spread only
            for _, row in df.iterrows():
                rows.append({
                    "expiry": exp_date,
                    "strike": row["strike"],
                    "iv": row["impliedVolatility"],
                    "type": opt_type,
                    "volume": row["volume"],
                })

    df = pd.DataFrame(rows)
    df["dte"] = (pd.to_datetime(df["expiry"]) - pd.Timestamp.today()).dt.days
    df["dte_years"] = df["dte"] / 365                          # years for y-axis
    df["moneyness"] = (df["strike"] / spot) * 100             # % moneyness for x-axis
    df["log_moneyness"] = np.log(df["strike"] / spot)         # keep for OTM filter
    return df, spot