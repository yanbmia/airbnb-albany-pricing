"""
Configuration file for customizing the web app behavior
Modify these settings without touching the main app code
"""

# ─── APP SETTINGS ───
APP_TITLE = "Albany Airbnb Pricing & Occupancy"
APP_DESCRIPTION = "AI-powered price recommendations and occupancy forecasts for Airbnb hosts in Albany, NY"
APP_ICON = "📊"

# ─── MODEL SETTINGS ───
MODEL_DIR = "./models"  # Directory where trained models are saved
DATA_DIR = "./albany-data"  # Directory with training data

# ─── PRICE MODEL SETTINGS ───
PRICE_MIN = 20      # Minimum allowed recommended price ($)
PRICE_MAX = 800     # Maximum allowed recommended price ($)
PRICE_CONFIDENCE_RANGE = 0.10  # ±10% for aggressive/conservative pricing

# ─── OCCUPANCY MODEL SETTINGS ───
OCCUPANCY_THRESHOLD_LOW = 0.25      # Below 25% = Low
OCCUPANCY_THRESHOLD_MODERATE = 0.50  # 25-50% = Moderate-Low
OCCUPANCY_THRESHOLD_HIGH = 0.75      # 75%+ = Very High

# ─── FEATURE SCALING ───
# These are optional scaling factors if you want to adjust model weights
PRICE_SENSITIVITY = 1.0      # 1.0 = normal, >1.0 makes price changes more aggressive
OCCUPANCY_SENSITIVITY = 1.0  # 1.0 = normal

# ─── DISPLAY SETTINGS ───
SHOW_CONFIDENCE_INTERVALS = True
SHOW_FEATURE_IMPORTANCE = False  # Set to True to show model feature importance
SHOW_DEBUG_INFO = False  # Set to True for technical users

# ─── SEASONAL ADJUSTMENTS (Optional) ───
# Set these to True to enable seasonal pricing recommendations
ENABLE_SEASONAL_ADJUSTMENT = False
SEASONAL_FACTORS = {
    1: 0.90,   # January - winter low
    2: 0.92,   # February
    3: 0.98,   # March
    4: 1.02,   # April
    5: 1.05,   # May
    6: 1.10,   # June - summer high
    7: 1.12,   # July - peak season
    8: 1.10,   # August
    9: 1.05,   # September
    10: 1.02,  # October
    11: 0.95,  # November
    12: 1.00,  # December
}

# ─── WEEKEND ADJUSTMENTS ───
ENABLE_WEEKEND_ADJUSTMENT = True
WEEKEND_PRICE_MULTIPLIER = 1.15  # Increase prices by 15% on weekends

# ─── COLOR SCHEME ───
COLOR_PRIMARY = "#667eea"
COLOR_SECONDARY = "#764ba2"
COLOR_SUCCESS = "#27ae60"
COLOR_WARNING = "#f39c12"
COLOR_DANGER = "#e74c3c"

# ─── ROOM TYPE CATEGORIES ───
ROOM_TYPES = {
    "Entire home/apt": {"code": 0, "emoji": "🏠", "avg_price": 185},
    "Private room": {"code": 1, "emoji": "🛏️", "avg_price": 95},
    "Shared room": {"code": 2, "emoji": "👥", "avg_price": 65},
}

# ─── AMENITIES ───
PREMIUM_AMENITIES = [
    "Instant Bookable",
    "Superhost Status",
]

# ─── PREDICTION EXPLANATIONS ───
PRICE_TIPS = {
    "conservative": "Lower price attracts more bookings and builds reviews. Good for new listings.",
    "recommended": "Market-based optimal price balancing occupancy and revenue.",
    "aggressive": "Higher price targets high-value bookings. Requires strong reviews and demand.",
}

OCCUPANCY_FACTORS = {
    "weekend": "Weekends typically see 50% higher demand than weekdays",
    "reviews": "Higher-rated listings are 20% more likely to get booked",
    "superhost": "Superhost status increases booking likelihood by 15%",
    "instant_booking": "Instant booking can improve conversion by 10-12%",
    "price_sensitivity": "Higher prices reduce occupancy, lower prices increase it",
}

# ─── API SETTINGS (for future cloud deployment) ───
API_ENABLED = False
API_KEY_REQUIRED = False
RATE_LIMIT = None  # Set to number to limit requests per minute

# ─── ANALYTICS SETTINGS ───
SHOW_MARKET_ANALYTICS = True
ANALYTICS_LOOKBACK_DAYS = 90  # Days of data to analyze

# ─── FEEDBACK & TRACKING ───
ENABLE_FEEDBACK = False  # Allow users to provide feedback
TRACK_PREDICTIONS = False  # Save predictions for analysis
