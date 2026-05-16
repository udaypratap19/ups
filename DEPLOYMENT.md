# IntelliTrade AI - Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Navigate to the project directory:**
```bash
cd /app/streamlit_app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

### Using the Run Script

Alternatively, use the provided run script:
```bash
cd /app/streamlit_app
./run.sh
```

## Streamlit Cloud Deployment

### Step 1: Prepare Your Repository

1. Create a GitHub repository for your project
2. Push the `/app/streamlit_app` folder to the repository
3. Ensure these files are in the root:
   - `app.py` (main application)
   - `requirements.txt` (dependencies)
   - `.streamlit/config.toml` (configuration)

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Choose the branch (usually `main`)
6. Set the main file path: `app.py`
7. Click "Deploy"

### Step 3: Configuration

Streamlit Cloud will automatically:
- Install dependencies from `requirements.txt`
- Use settings from `.streamlit/config.toml`
- Provide a public URL for your app

## Alternative Deployment Options

### Heroku Deployment

1. Create a `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
" > ~/.streamlit/config.toml
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t intellitrade-ai .
docker run -p 8501:8501 intellitrade-ai
```

### AWS EC2 Deployment

1. Launch an EC2 instance (Ubuntu recommended)
2. SSH into the instance
3. Install Python and dependencies:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```
4. Run the app:
```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```
5. Configure security group to allow port 8501

## Environment Variables

No API keys required! The app uses Yahoo Finance's free API through the `yfinance` library.

## Performance Optimization

### For Large-Scale Deployment:

1. **Use Caching:**
   - Add `@st.cache_data` decorators to data loading functions
   - Cache trained models to avoid retraining

2. **Optimize Model Training:**
   - Reduce LSTM epochs for faster training
   - Use smaller lookback periods
   - Consider pre-training models

3. **Database Integration:**
   - Store historical data in a database


    - Cache predictions and technical indicators
## Troubleshooting

### Issue: Module Import Errors
**Solution:** Ensure all `__init__.py` files are present in subdirectories

### Issue: TensorFlow Warnings
**Solution:** These are normal and can be ignored, or suppress with:
```python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
```

### Issue: Slow Model Training
**Solution:** 
- Reduce LSTM epochs (default: 50)
- Use smaller datasets (shorter time periods)
- Consider using CPU-optimized TensorFlow

### Issue: Yahoo Finance Rate Limiting
**Solution:** 
- Add delays between requests
- Cache data locally
- Use batch requests

## Monitoring

### View App Logs
```bash
streamlit run app.py --logger.level=debug
```

### Check Resource Usage
- Memory: Monitor RAM usage during model training
- CPU: LSTM training is CPU-intensive
- Network: Yahoo Finance API calls

## Updates & Maintenance

### Updating Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Adding New S&P 500 Companies
Edit `data/sp500_companies.py` and add ticker symbols to the dictionary.

### Customizing Models
- LSTM: Modify `models/lstm_model.py`
- ARIMA: Modify `models/arima_model.py`
- Prophet: Modify `models/prophet_model.py`

## Security Considerations

1. **No Sensitive Data:** App doesn't require API keys or personal information
2. **HTTPS:** Use HTTPS in production (automatic on Streamlit Cloud)
3. **Input Validation:** Ticker symbols are validated against Yahoo Finance

## Cost Considerations

### Free Options:
- **Streamlit Cloud:** Free tier available (limited resources)
- **Yahoo Finance API:** Completely free

### Paid Options:
- **Heroku:** Starts at $7/month
- **AWS EC2:** Pay per usage
- **DigitalOcean:** Starts at $5/month

## Support

For issues or questions:
1. Check the README.md
2. Review error logs
3. Verify all dependencies are installed
4. Ensure Python version compatibility (3.8+)

--

**Happy Trading! **