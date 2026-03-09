import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
from datetime import datetime

class PricingModel:
    def __init__(self, model_path='models/pricing_model.joblib'):
        self.model_path = model_path
        self.model = self.load_model()

    def train(self, data=None):
        """
        Trains the RandomForestRegressor on provided data or synthetic data if None.
        Features: hour_of_day, day_of_week, stock_level, demand_score, base_price
        Target: optimal_price
        """
        if data is None:
            # Generate synthetic data for initial training
            np.random.seed(42)
            n_samples = 1000
            
            base_prices = np.random.uniform(10, 500, n_samples)
            stock_levels = np.random.randint(0, 100, n_samples)
            demand_scores = np.random.uniform(0, 10, n_samples)
            days = np.random.randint(0, 7, n_samples)
            hours = np.random.randint(0, 24, n_samples)
            
            # Target logic: higher demand + lower stock + peak hours = higher price
            # Simplified formula for synthetic target
            target_prices = base_prices * (1 + 0.05 * demand_scores / 10 - 0.05 * stock_levels / 100 + 0.03 * (hours > 17))
            
            data = pd.DataFrame({
                'hour_of_day': hours,
                'day_of_week': days,
                'stock_level': stock_levels,
                'demand_score': demand_scores,
                'base_price': base_prices,
                'optimal_price': target_prices
            })

        X = data[['hour_of_day', 'day_of_week', 'stock_level', 'demand_score', 'base_price']]
        y = data['optimal_price']

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model trained and saved to {self.model_path}")

    def load_model(self):
        if os.path.exists(self.model_path):
            return joblib.load(self.model_path)
        return None

    def predict(self, features):
        """
        Predict optimal price based on input features.
        features: list or array [hour, day, stock, demand, base_price]
        """
        if self.model is None:
            self.train() # Initial train if model doesn't exist
            
        return self.model.predict([features])[0]
