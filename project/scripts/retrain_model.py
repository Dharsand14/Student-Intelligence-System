import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import os
from config.constants import MODEL_PATH
from database.predictions_db import get_all

def retrain_random_forest():
    """
    Pulls historical data from the database and updates the Random Forest model.
    """
    df = get_all()
    if df is None or df.empty or len(df) < 50:
        print("⚠️ Insufficient data to retrain. Need at least 50 records.")
        return False
        
    print("🔄 Retraining model from new database records...")
    
    # Feature Engineering
    features = ['study_hours', 'attendance', 'sleep_hours', 'mental_health']
    X = df[features].fillna(0)
    y = df['exam_scores']  # Ensure exam_scores is tracked or use actual test scores
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    score = model.score(X_test, y_test)
    print(f"📊 New model R^2 score: {score:.4f}")
    
    if score < 0.5:
        print("❌ Model performance dropped below acceptable threshold. Not saving.")
        return False
        
    # Save Model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"✅ Best model updated and saved to: {MODEL_PATH}")
    return True

if __name__ == "__main__":
    retrain_random_forest()
