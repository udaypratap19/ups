"""Demo data generator for when Yahoo Finance API is unavailable"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_demo_stock_data(ticker='DEMO', days=1825):
    """Generate realistic demo stock data — seed varies by ticker."""
    seed = sum(ord(c) for c in ticker)
    rng = np.random.RandomState(seed)

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    date_range = date_range[date_range.dayofweek < 5]

    n = len(date_range)
    initial_price = 100 + rng.uniform(0, 200)

    returns = rng.normal(0.0005, 0.018, n)
    trend = np.linspace(0, 0.25, n)
    returns = returns + trend / n

    prices = initial_price * np.exp(np.cumsum(returns))
    seasonality = 4 * np.sin(np.arange(n) * 2 * np.pi / 252)
    prices = prices + seasonality

    df = pd.DataFrame({
        'date': date_range,
        'open': prices * (1 + rng.uniform(-0.01, 0.01, n)),
        'high': prices * (1 + rng.uniform(0.001, 0.02, n)),
        'low': prices * (1 - rng.uniform(0.001, 0.02, n)),
        'close': prices,
        'volume': rng.randint(50_000_000, 150_000_000, n).astype(float),
    })

    df['high'] = df[['open', 'high', 'close']].max(axis=1)
    df['low'] = df[['open', 'low', 'close']].min(axis=1)
    df['dividends'] = 0.0
    df['stock_splits'] = 0.0
    return df


def get_demo_real_time_data(ticker='DEMO'):
    """Generate demo real-time data — deterministic per ticker."""
    seed = sum(ord(c) for c in ticker)
    rng = np.random.RandomState(seed + 9999)

    current_price = rng.uniform(180, 220)
    previous_close = current_price * rng.uniform(0.98, 1.02)

    return {
        'current_price': round(current_price, 2),
        'previous_close': round(previous_close, 2),
        'open': round(current_price * rng.uniform(0.99, 1.01), 2),
        'day_high': round(current_price * rng.uniform(1.0, 1.02), 2),
        'day_low': round(current_price * rng.uniform(0.98, 1.0), 2),
        'volume': int(rng.randint(80_000_000, 120_000_000)),
        'market_cap': int(current_price * 16_000_000_000),
        'pe_ratio': round(rng.uniform(25, 35), 2),
        '52w_high': round(current_price * rng.uniform(1.05, 1.15), 2),
        '52w_low': round(current_price * rng.uniform(0.85, 0.95), 2),
    }
