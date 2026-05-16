"""LSTM Model for stock price prediction"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class LSTMModel:
    def __init__(self, look_back=60):
        self.look_back = look_back
        self.model = None
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self._scaler_fitted = False

    def prepare_data(self, data, column='close', fit_scaler=True):
        """Prepare data for LSTM.
        fit_scaler=True for training data, False for test data."""
        values = data[column].values.reshape(-1, 1)

        if fit_scaler:
            scaled_data = self.scaler.fit_transform(values)
            self._scaler_fitted = True
        else:
            scaled_data = self.scaler.transform(values)

        if len(scaled_data) <= self.look_back:
            return np.array([]).reshape(0, self.look_back, 1), np.array([])

        X, y = [], []
        for i in range(self.look_back, len(scaled_data)):
            X.append(scaled_data[i - self.look_back:i, 0])
            y.append(scaled_data[i, 0])

        X, y = np.array(X), np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        return X, y

    def build_model(self, input_shape):
        """Build LSTM model"""
        import tensorflow as tf
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout

        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=input_shape),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            LSTM(units=50),
            Dropout(0.2),
            Dense(units=1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model
        return model

    def train(self, X_train, y_train, epochs=50, batch_size=32, verbose=0):
        """Train LSTM model"""
        if X_train.shape[0] == 0:
            return None
        if self.model is None:
            self.build_model((X_train.shape[1], 1))
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose,
            validation_split=0.1
        )
        return history

    def predict(self, X):
        """Make predictions"""
        if self.model is None or X.shape[0] == 0:
            return np.array([])
        predictions = self.model.predict(X, verbose=0)
        predictions = self.scaler.inverse_transform(predictions)
        return predictions

    def predict_future(self, data, days=30, column='close'):
        """Predict future prices"""
        if self.model is None or not self._scaler_fitted:
            return np.zeros(days)

        last_data = data[column].values[-self.look_back:]
        predictions = []

        for _ in range(days):
            scaled_data = self.scaler.transform(last_data.reshape(-1, 1))
            X = scaled_data.reshape(1, self.look_back, 1)
            pred = self.model.predict(X, verbose=0)
            pred_price = self.scaler.inverse_transform(pred)[0, 0]
            predictions.append(pred_price)
            last_data = np.append(last_data[1:], pred_price)

        return np.array(predictions)

    @staticmethod
    def evaluate(y_true, y_pred):
        """Calculate evaluation metrics"""
        if len(y_true) == 0 or len(y_pred) == 0:
            return {'MAE': np.nan, 'RMSE': np.nan, 'MAPE': np.nan, 'R2': np.nan}
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        nonzero = y_true != 0
        mape = np.mean(np.abs((y_true[nonzero] - y_pred[nonzero]) / y_true[nonzero])) * 100 if nonzero.any() else np.nan
        r2 = r2_score(y_true, y_pred)
        return {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'R2': r2}
