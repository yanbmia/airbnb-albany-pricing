# 🚀 Quick Start Guide - Albany Airbnb Pricing Dashboard

**Get up and running in 5 minutes!**

## Step 1: Install Dependencies (2 min)

```bash
pip install -r requirements.txt
```

## Step 2: Train Models (2-3 min)

```bash
python model_trainer.py
```

You'll see:
```
✓ Data loaded successfully
✓ Features prepared successfully
✓ Occupancy Model Trained | AUC: 0.8523
✓ Price Model Trained | MAE: $28.45 | R²: 0.7234
✓ Models saved to ./models/
✓ All models trained and saved!
```

## Step 3: Launch the App (1 min)

```bash
streamlit run app.py
```

The app opens automatically at: **http://localhost:8501**

---

## Using the Dashboard

### 💰 Get Price Recommendations
1. Go to **"Price Recommendation"** tab
2. Enter your listing details:
   - Guest capacity, bedrooms, beds
   - Room type, review score
   - Special features (superhost, instant booking)
3. Pick a date
4. Click **"Get Price Recommendation"**
5. See suggested prices: Conservative | Recommended | Aggressive

### 📈 Predict Occupancy
1. Go to **"Occupancy Forecast"** tab
2. Fill in same listing details
3. Enter your current nightly price
4. Pick a date
5. Click **"Predict Occupancy"**
6. Get booking probability % and insights

### 📊 View Market Analytics
1. Go to **"Analytics"** tab
2. Explore trends:
   - Day of week patterns
   - Room type comparison
   - Seasonal trends
   - Market insights

---

## ✅ Checklist

- [ ] `requirements.txt` is in project folder
- [ ] `albany-data/` folder has: calendar.csv, listings.csv, reviews.csv
- [ ] Run `python model_trainer.py` once to create models
- [ ] Run `streamlit run app.py` to start app
- [ ] App opens at http://localhost:8501

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'streamlit'` | Run: `pip install -r requirements.txt` |
| `Models not found` error | Run: `python model_trainer.py` |
| Data loading error | Check `albany-data/` has all 3 CSV files |
| App won't respond | Restart: `Ctrl+C` then `streamlit run app.py` |

---

## 📱 Share Your App

### Option A: Streamlit Cloud (Free, easiest)
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Deploy in 2 clicks
4. Get shareable link

### Option B: Local Network
Share with others on your network:
```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from other computers at: `http://[your-ip]:8501`

---

## 📚 Next Steps

- Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed deployment options
- Check [README.md](README.md) for complete documentation
- Update models monthly with new data: `python model_trainer.py`

**Questions?** Most issues are fixed by reinstalling dependencies or retraining models.

Happy pricing! 🏡💰
