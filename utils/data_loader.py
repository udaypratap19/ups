"""Data loading utilities for stock data"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class StockDataLoader:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_historical_data(self, period='5y', interval='1d'):
        """Fetch historical stock data"""
        try:
            df = self.stock.history(period=period, interval=interval, auto_adjust=True)
            if df.empty:
                end_date = datetime.now()
                period_map = {'1y': 365, '2y': 730, '5y': 1825, '10y': 3650, 'max': 7300}
                days = period_map.get(period, 1825)
                start_date = end_date - timedelta(days=days)
                df = self.stock.history(start=start_date, end=end_date, auto_adjust=True)

            if df.empty:
                return None

            df = df.reset_index()
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]

            if 'close' not in df.columns and 'adj_close' in df.columns:
                df['close'] = df['adj_close']
            elif 'close' not in df.columns and 'adjclose' in df.columns:
                df['close'] = df['adjclose']

            return df
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return None

    def get_real_time_data(self):
        """Fetch real-time stock data"""
        try:
            info = self.stock.info
            return {
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                '52w_high': info.get('fiftyTwoWeekHigh', 0),
                '52w_low': info.get('fiftyTwoWeekLow', 0),
            }
        except Exception as e:
            print(f"Error fetching real-time data: {e}")
            return None

    def prepare_data(self, df):
        """Clean and prepare data for modeling"""
        if df is None or df.empty:
            return None

        df = df.dropna()
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        return df

    def split_train_test(self, df, train_size=0.8):
        """Split data into train and test sets"""
        split_idx = int(len(df) * train_size)
        train_data = df[:split_idx]
        test_data = df[split_idx:]
        return train_data, test_data
