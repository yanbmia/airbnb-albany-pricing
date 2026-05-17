"""
Model training and preparation script
Extracts core model training logic from the notebook
"""

import pandas as pd
import numpy as np
import joblib
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report
import lightgbm as lgb

SEED = 42


def load_and_prepare_data(data_root='./albany-data'):
    """Load and prepare data from CSV files"""
    try:
        # Load CSVs
        calendar_df = pd.read_csv(f'{data_root}/calendar.csv')
        listings_df = pd.read_csv(f'{data_root}/listings.csv')
        reviews_df = pd.read_csv(f'{data_root}/reviews.csv')
        
        print("✓ Data loaded successfully")
        return calendar_df, listings_df, reviews_df
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return None, None, None


def prepare_features(calendar_df, listings_df, reviews_df):
    """Prepare features for modeling"""
    
    # Merge data - listings uses 'id' instead of 'listing_id'
    df = calendar_df.merge(listings_df, left_on='listing_id', right_on='id', how='left', suffixes=('_calendar', '_listing'))
    df = df.merge(reviews_df.groupby('listing_id').size().reset_index(name='number_of_reviews'), 
                  on='listing_id', how='left')
    
    # Parse date
    df['date'] = pd.to_datetime(df['date'])
    
    # Target: available=f means booked
    df['booked'] = (df['available'] == 'f').astype(int)
    
    # Date features
    df['month'] = df['date'].dt.month
    df['day_of_week_n'] = df['date'].dt.dayofweek
    df['is_weekend'] = df['day_of_week_n'].isin([5, 6]).astype(int)
    df['quarter'] = df['date'].dt.quarter
    df['day_of_month'] = df['date'].dt.day
    
    # Price features - use calendar price (already numeric)
    df['price_num'] = df['price_calendar'].fillna(df['price_listing']).fillna(50)  # fallback to $50 if missing
    
    # Room type encoding
    if 'room_type' in df.columns:
        df['room_type_enc'] = pd.factorize(df['room_type'])[0]
    
    # Neighborhood encoding
    if 'neighbourhood_cleansed' in df.columns:
        df['neighbourhood_enc'] = pd.factorize(df['neighbourhood_cleansed'])[0]
        df['neighbourhood_occ_mean'] = df.groupby('neighbourhood_enc')['booked'].transform('mean')
    
    # Numeric columns - fill NAs
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # Ensure correct data types for LightGBM
    if 'instant_bookable' in df.columns:
        df['instant_bookable'] = (df['instant_bookable'].astype(str).str.lower() == 't').astype(int)
    else:
        df['instant_bookable'] = 0
    
    if 'host_is_superhost' in df.columns:
        df['host_is_superhost'] = (df['host_is_superhost'].astype(str).str.lower() == 't').astype(int)
    else:
        df['host_is_superhost'] = 0
    
    # Ensure price_num is float
    df['price_num'] = pd.to_numeric(df['price_num'], errors='coerce').fillna(50)
    
    print("✓ Features prepared successfully")
    return df


def train_occupancy_model(df):
    """Train occupancy prediction model"""
    
    # Feature selection
    OCCUPANCY_FEATURES = [
        'month', 'day_of_week_n', 'is_weekend', 'quarter',
        'accommodates', 'bedrooms', 'beds', 'minimum_nights',
        'review_scores_rating', 'number_of_reviews',
        'instant_bookable', 'host_is_superhost',
        'price_num',
    ]
    
    # Add encoded features if available
    if 'room_type_enc' in df.columns:
        OCCUPANCY_FEATURES.append('room_type_enc')
    if 'neighbourhood_occ_mean' in df.columns:
        OCCUPANCY_FEATURES.append('neighbourhood_occ_mean')
    
    OCCUPANCY_FEATURES = [f for f in OCCUPANCY_FEATURES if f in df.columns]
    
    # Time-based split (73% train)
    cutoff = df['date'].quantile(0.73)
    train_df = df[df['date'] <= cutoff]
    test_df = df[df['date'] > cutoff]
    
    X_train = train_df[OCCUPANCY_FEATURES].fillna(0)
    y_train = train_df['booked']
    X_test = test_df[OCCUPANCY_FEATURES].fillna(0)
    y_test = test_df['booked']
    
    # Train LightGBM
    model = lgb.LGBMClassifier(
        n_estimators=200,
        learning_rate=0.05,
        num_leaves=31,
        min_child_samples=10,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=SEED,
        n_jobs=-1,
        verbose=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"✓ Occupancy Model Trained | AUC: {auc:.4f}")
    
    return model, OCCUPANCY_FEATURES, auc


def train_price_model(df):
    """Train price recommendation model"""
    
    # Filter reasonable prices
    df_price = df[df['price_num'].between(20, 800)].copy()
    
    PRICE_FEATURES = [
        'month', 'day_of_week_n', 'is_weekend', 'quarter',
        'accommodates', 'bedrooms', 'beds', 'minimum_nights',
        'review_scores_rating', 'number_of_reviews',
        'instant_bookable', 'host_is_superhost',
        'price_num',
    ]
    
    if 'room_type_enc' in df_price.columns:
        PRICE_FEATURES.append('room_type_enc')
    if 'neighbourhood_occ_mean' in df_price.columns:
        PRICE_FEATURES.append('neighbourhood_occ_mean')
    
    PRICE_FEATURES = [f for f in PRICE_FEATURES if f in df_price.columns]
    
    # Time-based split
    cutoff = df_price['date'].quantile(0.73)
    train_df = df_price[df_price['date'] <= cutoff]
    test_df = df_price[df_price['date'] > cutoff]
    
    X_train = train_df[PRICE_FEATURES].fillna(0)
    y_train = np.log1p(train_df['price_num'])
    X_test = test_df[PRICE_FEATURES].fillna(0)
    y_test = np.log1p(test_df['price_num'])
    
    # Train LightGBM Regressor
    model = lgb.LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        num_leaves=63,
        min_child_samples=20,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=1.0,
        random_state=SEED,
        n_jobs=-1,
        verbose=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    from sklearn.metrics import mean_absolute_error, r2_score
    y_pred = np.expm1(model.predict(X_test))
    y_actual = np.expm1(y_test)
    mae = mean_absolute_error(y_actual, y_pred)
    r2 = r2_score(y_actual, y_pred)
    
    print(f"✓ Price Model Trained | MAE: ${mae:.2f} | R²: {r2:.4f}")
    
    return model, PRICE_FEATURES, mae, r2


def save_models(occupancy_model, occupancy_features, price_model, price_features, output_dir='./models'):
    """Save trained models and feature lists"""
    Path(output_dir).mkdir(exist_ok=True)
    
    joblib.dump(occupancy_model, f'{output_dir}/occupancy_model.pkl')
    joblib.dump(occupancy_features, f'{output_dir}/occupancy_features.pkl')
    joblib.dump(price_model, f'{output_dir}/price_model.pkl')
    joblib.dump(price_features, f'{output_dir}/price_features.pkl')
    
    print(f"✓ Models saved to {output_dir}/")


def load_models(model_dir='./models'):
    """Load pre-trained models"""
    occupancy_model = joblib.load(f'{model_dir}/occupancy_model.pkl')
    occupancy_features = joblib.load(f'{model_dir}/occupancy_features.pkl')
    price_model = joblib.load(f'{model_dir}/price_model.pkl')
    price_features = joblib.load(f'{model_dir}/price_features.pkl')
    
    return occupancy_model, occupancy_features, price_model, price_features


if __name__ == '__main__':
    # Load and prepare data
    cal, list_df, rev = load_and_prepare_data()
    if cal is None:
        print("Cannot proceed without data")
        exit(1)
    
    df = prepare_features(cal, list_df, rev)
    
    # Train models
    occ_model, occ_features, auc = train_occupancy_model(df)
    price_model, price_features, mae, r2 = train_price_model(df)
    
    # Save models
    save_models(occ_model, occ_features, price_model, price_features)
    
    print("\n✓ All models trained and saved!")
