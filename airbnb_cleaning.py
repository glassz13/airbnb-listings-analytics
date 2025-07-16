"""
Airbnb Data Cleaning Pipeline
----------------------------
1. Handles missing values (host status, listings count, prices, etc.)
2. Standardizes columns (price to numeric, bathroom extraction)
3. Classifies hosts into 3 types by listing count 
4. Removes extreme outliers for better visualization
5. Exports cleaned CSV for dashboard use
"""

import pandas as pd

# Load the dataset
df = pd.read_csv("raw_airbnb.csv")

# ========================
# --- Step 1: Cleaning ---
# ======================== 

# Clean 'host_is_superhost' to boolean
df["host_is_superhost"] = df["host_is_superhost"].map({"t": True, "f": False})
df["host_is_superhost"] = df["host_is_superhost"].fillna(False)

# Fill missing 'host_total_listings_count' with 1 (assume new host)
df["host_total_listings_count"] = df["host_total_listings_count"].fillna(1)

# Clean 'price' column to numeric
df["price"] = df["price"].replace('[\$,]', '', regex=True).astype(float)
df = df.dropna(subset=["price"])  # Drop listings with missing price

# Extract numeric part from 'bathrooms_text' → new 'bathrooms' column
df["bathrooms"] = df["bathrooms_text"].str.extract('(\d+\.?\d*)').astype(float)
df = df.drop(columns="bathrooms_text")  # Drop original messy column

# Fill 'reviews_per_month' with 0 (no reviews)
df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

# Fill 'name' with placeholder
df["name"] = df["name"].fillna("No name provided")


# 🔻 Not filled for visualization; handle missing at chart level:
# df["review_scores_rating"]
print(df["bedrooms"].isnull().sum())
print(df["beds"].isnull().sum())



# Handle NaNs inside individual chart logic (e.g., df.dropna(subset=["beds"]))

# ================================
# --- Step 2: Host Type Segment ---
# ================================

def classify_host(count):
    if count >= 100:
        return "Big Company"
    elif count >= 5:
        return "Professional"
    else:
        return "Individual"

df["host_type"] = df["host_total_listings_count"].apply(classify_host)

# ================================
# --- Step 3: Outlier Removal ---
# ================================

# Cap extremes to improve visualization quality (not modeling)
df = df[df["price"] <= 1500]
df = df[df["bathrooms"] <= 10]
df = df[df["bedrooms"] <= 10]
df = df[df["beds"] <= 10]
df = df[df["reviews_per_month"] <= 30]
df = df[df["minimum_nights"] <= 120]

# ================================
# --- Step 4: Export Cleaned CSV ---
# ================================

df.to_csv("findings_cleaned.csv", index=False)

# Optional: check summary
print(df.info())
print(df["host_type"].value_counts())
