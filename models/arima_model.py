"""ARIMA Model for stock price prediction"""
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class ARIMAModel:
    def __init__(self, order=(5, 1, 0)):
        self.order = order
        self.model = None
        self.fitted_model = None
        
    def train(self, data, column='close'):
        """Train ARIMA model"""
        try:
            self.model = ARIMA(data[column], order=self.order)
            self.fitted_model = self.model.fit()
            return self.fitted_model
        except Exception as e:
            print(f"Error training ARIMA: {e}")
            return None
    
    def predict(self, steps=1):
        """Make predictions"""
        if self.fitted_model is None:
            return None
        
        try:
            forecast = self.fitted_model.forecast(steps=steps)
            return forecast.values
        except Exception as e:
            print(f"Error predicting: {e}")
            return None
    
    def predict_in_sample(self, start, end):
        """Predict in-sample"""
        if self.fitted_model is None:
            return None
        
        try:
            predictions = self.fitted_model.predict(start=start, end=end)
            return predictions.values
        except Exception as e:
            print(f"Error in-sample prediction: {e}")
            return None
    
    def evaluate(self, y_true, y_pred):
        """Calculate evaluation metrics"""
        # Remove NaN values
        mask = ~(np.isnan(y_true) | np.isnan(y_pred))
        y_true_clean = y_true[mask]
        y_pred_clean = y_pred[mask]
        
        if len(y_true_clean) == 0:
            return {'MAE': np.nan, 'RMSE': np.nan, 'MAPE': np.nan, 'R2': np.nan}
        
        mae = mean_absolute_error(y_true_clean, y_pred_clean)
        rmse = np.sqrt(mean_squared_error(y_true_clean, y_pred_clean))
        
        # Avoid division by zero in MAPE
        mape_values = np.abs((y_true_clean - y_pred_clean) / y_true_clean)
        mape_values = mape_values[np.isfinite(mape_values)]
        mape = np.mean(mape_values) * 100 if len(mape_values) > 0 else np.nan
        r2 = r2_score(y_true_clean, y_pred_clean)
        return {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'R2': r2
        }