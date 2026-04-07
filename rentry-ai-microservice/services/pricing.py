import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_rental_price(market_value):
    try:
        # 1. Load your data
        df = pd.read_csv("pricing_data.csv")
        
        # 2. Log-Log transformation (Industry standard)
        X = np.log10(df[['market_price']].values)
        y = np.log10(df['rental_price'].values)
        
        model = LinearRegression()
        model.fit(X, y)
        
        # 3. Predict for the new value
        input_log = np.log10([[market_value]])
        prediction_log = model.predict(input_log)
        
        # 4. Convert back to normal currency
        prediction = 10 ** prediction_log[0]
        return round(float(prediction), 2)
        
    except Exception as e:
        # --- 5 SECTION TIERED FALLBACK LOGIC ---
        
        if market_value < 1000:
            # Tier 1: Cheap items (2% - e.g., $100 -> $2)
            return round(market_value * 0.02, 2)
            
        elif market_value < 10000:
            # Tier 2: Mid-range (1.5% - e.g., $5,000 -> $75)
            return round(market_value * 0.015, 2)
            
        elif market_value < 100000:
            # Tier 3: Professional equipment (1% - e.g., $50,000 -> $500)
            return round(market_value * 0.01, 2)
            
        elif market_value < 1000000:
            # Tier 4: Expensive items/Cheap cars (0.5% - e.g., $500k -> $2,500)
            return round(market_value * 0.005, 2)
            
        else:
            # Tier 5: High-value assets/Luxury cars (0.1% - e.g., 4M -> 4,000)
            return round(market_value * 0.001, 2)
        # You can log the exception if needed
        # print(f"Error in prediction model: {e}")
        # raise e