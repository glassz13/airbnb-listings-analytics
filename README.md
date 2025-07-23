# 🏡 Airbnb Listings Analytics Dashboard

An end-to-end **Data Cleaning, Analytics, and Business Intelligence** project for Airbnb New York listings, built with **Python, Pandas, Plotly, Streamlit, and Scikit-Learn**.

This dashboard delivers actionable insights for hosts, property managers, and real estate professionals by analyzing **pricing strategies, host behavior, customer reviews, and location trends**.  
Includes a **Quick Price Estimator** via a simple ML model.

---

## 🚀 Live App

https://airbnb-listings-analytics-naojm2epkcttb4q2qtkzvl.streamlit.app/

---

## 📝 Executive Summary (Business Impact)
Airbnb hosts often struggle to optimize pricing and understand how factors like location, property type, and host reputation affect revenue.  
This dashboard helps users:
- Identify profitable neighborhoods.
- Compare pricing across host types (individuals, professionals, big companies).
- Analyze the influence of superhost status.
- Examine customer review patterns.
- Estimate listing prices using a basic ML model.

**Outcome:** Helps maximize rental income and understand market trends visually.

---

## 📂 Project Structure

```
├── app.py                         # Streamlit dashboard (analytics + ML)
├── airbnb_cleaning.py              # Data cleaning pipeline
├── data/
│   ├── raw_airbnb_listings.csv     # Original data
│   └── cleaned_airbnb_listings.csv # Cleaned dataset
├── requirements.txt
└── README.md
```

---

## 🔑 Features
- ✅ Cleaned and standardized Airbnb dataset (missing values, price formatting, host classification)
- ✅ Host segmentation: Individual / Professional / Big Company
- ✅ Interactive filters: neighborhood, price range, room type, host type, superhost
- ✅ Map-based price distribution
- ✅ Neighborhood price and availability trends
- ✅ Review insights: frequency, scores, relationships with price
- ✅ Simple ML-based Price Estimator using RandomForest
- ✅ Download filtered datasets

---

## ⚙️ Technologies Used
- **Python:** Pandas, Plotly, Scikit-learn
- **Streamlit:** Interactive dashboard framework
- **Plotly:** Advanced data visualizations
- **Data:** Airbnb NYC Open Data (CSV)

---

## 📊 Key Business Insights
- 🏙️ Pricing varies significantly by **neighborhood** and **host type**.
- ⭐ **Superhosts** command higher prices and maintain better review scores.
- 🏠 Larger properties increase price, but impact differs across locations.
- 💬 Review patterns reveal what customers value (cleanliness, accuracy, communication).

---

## 📈 Sample Visualizations
- Mapbox scatter: **Price by location**
- Bar charts: **Top neighborhoods by price & count**
- Scatter plots: **Price vs Bedrooms, Accommodates, Reviews**
- Box plots: **Price by room type, host type**
- Histograms: **Availability distribution**
- Pie chart: **Host type breakdown**

---

## 🤖 Quick ML Model (RandomForest)
**Purpose:** A basic price estimator for Airbnb hosts.  
Inputs: `Guests`, `Bedrooms`, `Room Type`  
Outputs: Predicted Price ($)  
Model: RandomForestRegressor trained on current filtered dataset.

---

## ⚙️ How to Run This Project Locally

```bash
# 1. Clone this repository
git clone https://github.com/your-username/airbnb-dashboard.git
cd airbnb-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the Streamlit app
streamlit run app.py
```

---

## 🖼️ Folder Preview (Visualization Assets)
> Consider adding screenshots/GIFs of:
> - Main dashboard
> - Filter examples
> - Price estimator

---

## ✨ Future Enhancements
- Advanced ML modeling: XGBoost / LightGBM for price prediction
- Add authentication (user accounts)
- Expand to multi-city Airbnb datasets
- Deploy on HuggingFace / Vercel for redundancy
- Add KPI export to PDF / PowerPoint

---

## 📅 Project Timeline
| Phase               | Time   |
|----------------------|--------|
| Data Cleaning        | 1 Day  |
| Dashboard Development| 2 Days |
| Testing / Deployment | 1 Day  |

---

## 👤 Author

**Mohit Kumar**  
IIT Delhi | Data Science & Machine Learning Enthusiast  
[GitHub](https://github.com/your-username) | [LinkedIn](https://linkedin.com/in/your-profile)

---

> ⭐ If you found this project valuable, consider giving it a star on GitHub.

