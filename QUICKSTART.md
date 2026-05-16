# IntelliTrade AI - Quick Start Guide

##  Getting Started in 3 Steps

### 1. Install Dependencies
```bash
cd /app/streamlit_app
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run app.py
```

### 3. Access the Application
Open your browser and go to: `http://localhost:8501`

##  Using the Application

### Step 1: Select a Stock
- Choose from S&P 500 dropdown (e.g., AAPL, GOOGL, TSLA)
- OR enter a custom ticker symbol

### Step 2: Configure Settings
- **Data Period:** How much historical data to analyze (1y - 10y)
- **Train/Test Split:** Percentage for model training
- **Model Parameters:** Customize LSTM, ARIMA settings
- **Backtesting:** Set initial capital and transaction costs

### Step 3: Analyze
Click **"Load & Analyze"** button

### Step 4: Explore Results

####  Price & Indicators Tab
- View historical prices
- See technical indicators (RSI, MACD, Bollinger Bands)
- Check trading signals

####  Model Predictions Tab
- Click "Train Models & Predict"
- Wait for LSTM, ARIMA, and Prophet to train
- View future price predictions
- Compare model forecasts

####  Backtesting Tab
- Click "Run Backtest"
- See portfolio performance
- View equity curve
- Check trade history

####  Model Comparison Tab
- Compare accuracy metrics (MAE, RMSE, R²)
- Identify best performing model

##  Example Use Case

### Analyzing Apple (AAPL)

1. Select "AAPL" from dropdown
2. Set period to "5y"
3. Keep default model settings
4. Set initial capital to $10,000
5. Click "Load & Analyze"
6. Train models (takes 2-3 minutes)
7. Run backtest
8. Compare results

##  Recommended Settings

### For Quick Analysis (Fast)
- Period: 1y
- LSTM Epochs: 20
- Look Back: 30 days

### For Accurate Predictions (Slow)
- Period: 5y
- LSTM Epochs: 100
- Look Back: 60 days

### For Day Trading Strategy
- Period: 1y
- Focus on RSI and MACD signals
- Lower transaction costs (0.05%)

### For Long-term Investment
- Period: 5y-10y
- Focus on moving averages
- Initial capital: $50,000+

##  Understanding the Metrics

### Model Performance
- **MAE:** Lower is better (average prediction error)
- **RMSE:** Lower is better (penalizes large errors)
- **MAPE:** Lower is better (percentage error)
- **R² Score:** Higher is better (0-1 scale, 1 = perfect)

### Backtesting Performance
- **Total Return:** Percentage gain/loss
- **Sharpe Ratio:** Risk-adjusted return (>1 is good, >2 is excellent)
- **Max Drawdown:** Largest peak-to-trough decline
- **Win Rate:** Percentage of profitable trades

##  Customization

### Change Theme
Use the theme toggle in the sidebar to switch between Dark and Light modes.

### Adjust Trading Strategy
Modify signal thresholds in `utils/indicators.py`:
- RSI oversold/overbought levels
- MACD crossover sensitivity
- Bollinger Band width

##  Important Notes

1. **First Run Takes Longer:** Model training requires 2-5 minutes
2. **Internet Required:** Real-time data fetching from Yahoo Finance
3. **Memory Usage:** LSTM models use significant RAM
4. **Educational Tool:** Not financial advice, for learning purposes only

##  Common Issues

### "Unable to load data"
- Check internet connection
- Verify ticker symbol is correct
- Try a different stock

### "Training taking too long"
- Reduce LSTM epochs (e.g., 20-30)
- Use shorter historical period (1y instead of 5y)
- Reduce look back period

### "Model comparison empty"
- Train models first in "Model Predictions" tab
- Wait for training to complete

##  Tips for Best Results

1. **Use liquid stocks:** Major companies (AAPL, MSFT, GOOGL)
2. **Start with 2-5 years of data:** Good balance of speed and accuracy
3. **Compare all three models:** Different models work better for different stocks
4. **Adjust parameters:** Experiment with different settings
5. **Check RSI and MACD:** Most reliable indicators for day trading

##  Exporting Data

Use the "Data Table" tab to download full datasets with all indicators as CSV.

##  Ready to Deploy?

See `DEPLOYMENT.md` for instructions on deploying to:
- Streamlit Cloud (easiest)
- Heroku
- AWS
- Docker

--

**Start trading smarter with IntelliTrade AI! **