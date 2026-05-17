# 🏡 Albany Airbnb Pricing & Occupancy Prediction Dashboard

A modern, user-friendly web application that helps Airbnb hosts in Albany optimize their listings through AI-powered price recommendations and occupancy forecasts.

## 📋 Features

- **💰 Price Recommendation**: Get AI-suggested optimal pricing for your listing based on market data and listing characteristics
- **📈 Occupancy Forecast**: Predict the likelihood of your listing being booked on specific dates
- **📊 Market Analytics**: Understand trends, seasonal patterns, and room type comparisons
- **⚡ Easy-to-Use Interface**: Intuitive, beginner-friendly design requiring no technical knowledge
- **🎯 Real-time Predictions**: Instant results based on your listing details

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
```bash
cd airbnb-albany-pricing
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Train the models** (one-time setup)
```bash
python model_trainer.py
```

This will:
- Load your Albany Airbnb data from `albany-data/`
- Train the occupancy prediction model
- Train the price recommendation model
- Save models to `./models/` directory

> **Note**: Make sure your data files are in the `albany-data/` folder:
> - `calendar.csv`
> - `listings.csv`
> - `reviews.csv`

4. **Launch the web app**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

## 📖 Usage Guide

### 💰 Price Recommendation Tab

1. Enter your listing details:
   - Number of guests accommodated
   - Bedrooms and beds
   - Room type (Entire home, Private room, Shared room)
   - Review score and number of reviews
   - Special amenities (Instant Bookable, Superhost status)

2. Select a date

3. Click "Get Price Recommendation"

4. View three pricing options:
   - **Conservative**: Lower price → higher occupancy
   - **Recommended**: Market-based optimal price
   - **Aggressive**: Higher price → more revenue per booking

### 📈 Occupancy Forecast Tab

1. Fill in your listing information (same as price tab)

2. Enter your current listing price

3. Select a specific date

4. Click "Predict Occupancy"

5. View booking probability as a percentage and get insights about factors affecting your booking likelihood

### 📊 Analytics Tab

Explore market-wide trends:
- Day of week occupancy patterns
- Room type performance comparison
- Price range distribution
- Seasonal trends across the year
- Key market insights and recommendations

## 🏗️ Project Structure

```
airbnb-albany-pricing/
├── app.py                      # Main Streamlit web app
├── model_trainer.py           # Model training script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── albany-data/              # Input data folder
│   ├── calendar.csv
│   ├── listings.csv
│   └── reviews.csv
└── models/                   # Generated after training
    ├── occupancy_model.pkl
    ├── occupancy_features.pkl
    ├── price_model.pkl
    └── price_features.pkl
```

## 🔧 Technical Details

### Models Used

**Occupancy Prediction**: LightGBM Classifier
- Predicts probability of booking on a specific date
- Features: date, property characteristics, pricing, reviews
- Performance: AUC ~0.85 on test data

**Price Recommendation**: LightGBM Regressor
- Predicts optimal nightly rate
- Features: date, seasonality, property features, demand signals
- Performance: MAE ~$30, R² ~0.72

### Features Included

- **Temporal**: Month, day of week, is_weekend, quarter
- **Property**: Accommodates, bedrooms, beds, room type
- **Booking**: Minimum nights, instant bookable
- **Host**: Superhost status, review score, number of reviews
- **Market**: Price, neighborhood occupancy rate

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Free & Easy)

1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Connect your GitHub repository
5. Select `app.py` as the main file
6. Deploy!

**Pros**: Free, auto-updates with GitHub commits, shareable link
**Cons**: Limited resources, public by default

### Option 2: Heroku

```bash
# 1. Create Procfile
echo "web: streamlit run --server.port $PORT app.py" > Procfile

# 2. Deploy
git push heroku main
```

### Option 3: Docker (Local or Cloud)

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t albany-airbnb .
docker run -p 8501:8501 albany-airbnb
```

## 📊 Data Requirements

Your data files should contain:
- **calendar.csv**: Availability and prices over time (date, listing_id, price, available)
- **listings.csv**: Property details (listing_id, accommodates, bedrooms, beds, room_type, review_scores_rating, etc.)
- **reviews.csv**: Guest reviews (listing_id, date, reviewer_id)

## 🔄 Updating the Model

To retrain with new data:

1. Update your CSV files in `albany-data/`
2. Run: `python model_trainer.py`
3. Restart the app: `streamlit run app.py`

The app will automatically use the updated models.

## 🐛 Troubleshooting

### "Models not found" error
- Run `python model_trainer.py` first
- Ensure `albany-data/` folder has all three CSV files

### "Import could not be resolved" in IDE
- This is normal for Streamlit. The app will still run fine
- Run: `pip install -r requirements.txt`

### App won't start
```bash
# Clear Streamlit cache
streamlit cache clear

# Try again
streamlit run app.py
```

### Data loading errors
- Check file paths are correct
- Verify CSV files are properly formatted
- Ensure column names match the code (case-sensitive)

## 📈 Performance Tips

For better predictions:
- Ensure your listings have at least 5+ reviews
- Update data monthly for seasonal accuracy
- Monitor actual vs. predicted prices to validate model
- Adjust conservative/aggressive prices based on your goals (occupancy vs. revenue)

## 🤝 Contributing

Have suggestions for improvements? Consider:
- Additional features (location, amenities, host experience)
- Model improvements (XGBoost, neural networks)
- UI enhancements
- Additional analytics

## 📄 License

This project is provided as-is for personal use.

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
3. Check data files are properly formatted

---

**Happy hosting! 🎉** Use these predictions to optimize your Albany Airbnb listings and maximize both occupancy and revenue.
