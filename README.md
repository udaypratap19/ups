#  [IntelliTrade AI](https://intellitrade-ai.streamlit.app/)

## Stock Price Prediction & Automated Trading Strategy System

### Overview
IntelliTrade AI is a comprehensive data-driven system designed to predict stock prices and simulate automated trading...

### Features

####  Multiple AI Models
- **LSTM (Deep Learning)**: Captures long-term dependencies and non-linear patterns
- **ARIMA**: Statistical model for linear time-series forecasting
- **Prophet**: Handles seasonality and holidays, robust to missing data

####  S&P 500 Coverage
- Pre-loaded with 120+ popular S&P 500 companies
- Custom ticker input for any stock symbol
- Real-time data from Yahoo Finance

####  Technical Analysis
- Moving Averages (SMA 20, 50, 200 & EMA 12, 26)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Volume analysis

####  Trading Strategy & Backtesting
- Automated buy/sell signals based on technical indicators
- Comprehensive backtesting engine
- Performance metrics:
   - Total Return
   - Sharpe Ratio
   - Maximum Drawdown
   - Win/Loss Ratio
   - Equity curve visualization
####  User Interface
- Dark/Light theme toggle
- Interactive charts using Plotly
- Real-time stock information
- Model comparison dashboard

### Installation

1. Navigate to the streamlit app directory:
```bash
cd /app/streamlit_app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Select a stock from the S&P 500 dropdown or enter a custom ticker

4. Configure your settings:
    - Historical period
    - Train/test split
    - Model parameters
    - Backtesting capital and transaction costs
5. Click "Load & Analyze" to start

### Project Structure

```
streamlit_app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── data/
│   └── sp500_companies.py     # S&P 500 companies list
├── models/
│   ├── lstm_model.py          # LSTM implementation
│   ├── arima_model.py         # ARIMA implementation
│   └── prophet_model.py       # Prophet implementation
└── utils/
     ├── data_loader.py         # Data fetching utilities
     ├── indicators.py          # Technical indicators
     └── backtesting.py         # Backtesting engine
```
### Technologies Used

- **Python 3.8+**
- **Streamlit**: Web application framework
- **TensorFlow/Keras**: Deep learning (LSTM)
- **Statsmodels**: Statistical modeling (ARIMA)
- **Prophet**: Time series forecasting by Meta
- **yfinance**: Yahoo Finance data API
- **Plotly**: Interactive visualizations
- **Pandas & NumPy**: Data manipulation
- **TA-Lib**: Technical analysis indicators

### Model Details

#### LSTM (Long Short-Term Memory)
- Architecture: 3 LSTM layers with dropout
- Input: Historical price data with configurable lookback period
- Output: Future price predictions
- Training: Configurable epochs and batch size

#### ARIMA (AutoRegressive Integrated Moving Average)
- Configurable p, d, q parameters
- Suitable for stationary time series
- Fast training and prediction

#### Prophet
- Developed by Meta (Facebook)
- Handles seasonality (daily, weekly, yearly)
- Robust to missing data and outliers
- Automatic detection of change points

### Trading Strategy Logic

**Buy Signals:**
- RSI < 30 (oversold)
- MACD crossover (bullish)
- Golden Cross (SMA 50 > SMA 200)
- Price below lower Bollinger Band

**Sell Signals:**
- RSI > 70 (overbought)
- MACD crossover (bearish)
- Death Cross (SMA 50 < SMA 200)
- Price above upper Bollinger Band

### Performance Metrics

**Model Evaluation:**
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- R² Score

**Backtesting Metrics:**
- Total Return (%)
- Sharpe Ratio
- Maximum Drawdown (%)
- Win Rate (%)
- Total number of trades

### Real-World Applications

-  Algorithmic Trading
-  Quantitative Finance
-  Portfolio Management
-  Hedge Fund Strategy Testing
-  Retail Investor Tools

### Future Enhancements

- Sentiment analysis from news and social media
- Reinforcement learning-based trading agent
- Multi-stock portfolio optimization
- Real-time trading bot integration
- Options trading strategies
- Cryptocurrency support

### Disclaimer

  This tool is for educational and research purposes only. Stock trading involves risk, and past performance does no...
  
---

**Built with using Streamlit**
