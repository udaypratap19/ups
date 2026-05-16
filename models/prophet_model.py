"""Prophet Model for stock price prediction"""
import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class ProphetModel:
    def __init__(self):
        self.model = None
        
    def prepare_data(self, data, column='close'):
        """Prepare data for Prophet (needs 'ds' and 'y' columns)"""
        df = pd.DataFrame()
        df['ds'] = pd.to_datetime(data['date'])
        df['y'] = data[column]
        return df
    
    def train(self, data, column='close'):
        """Train Prophet model"""
        try:
            prophet_data = self.prepare_data(data, column)
            self.model = Prophet(
                daily_seasonality=True,
                yearly_seasonality=True,
                weekly_seasonality=True,
                changepoint_prior_scale=0.05
            )
            self.model.fit(prophet_data)
            return self.model
        except Exception as e:
            print(f"Error training Prophet: {e}")
            return None
    
    def predict(self, periods=30):
        """Make future predictions"""
        if self.model is None:
            return None
        
        try:
            future = self.model.make_future_dataframe(periods=periods)
            forecast = self.model.predict(future)
            return forecast
        except Exception as e:
            print(f"Error predicting: {e}")
            return None
    
    def predict_on_data(self, data, column='close'):
        """Predict on existing data for evaluation"""
        if self.model is None:
            return None
        
        try:
            prophet_data = self.prepare_data(data, column)
            forecast = self.model.predict(prophet_data)
            return forecast['yhat'].values
        except Exception as e:
            print(f"Error predicting on data: {e}")
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