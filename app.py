"""
Airbnb Listings Analytics Dashboard
----------------------------------
Interactive web app for exploring Airbnb data with:

1. Spatial Analysis - Price distribution maps & neighborhood trends
2. Pricing Insights - Price distributions, room type comparisons
3. Host & Reviews - Host type analysis, review patterns

Features:
- Dynamic filtering by neighborhood/price/room type
- Interactive visualizations (maps, charts, histograms)
- Key metrics summary
- Data export capability
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor

# Set up page
st.set_page_config(page_title="Airbnb Analytics Pro", layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
st.title("🏡 Airbnb Listings Analytics")
st.markdown("---")
# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_airbnb.csv")


df = load_data()

# Sidebar filters
with st.sidebar:
    
    st.header("🔍 Filters")
    
    neighborhood = st.multiselect(
        "Neighborhood",
        options=df['neighbourhood_cleansed'].unique(),
        default=df['neighbourhood_cleansed'].unique()[:3]
    )
    room_type = st.multiselect(
        "Room Type",
        options=df['room_type'].unique(),
        default=df['room_type'].unique()
    )
    host_type = st.multiselect(
        "Host Type",
        options=df['host_type'].unique(),
        default=df['host_type'].unique()
    )
    price_range = st.slider(
        "Price Range ($)",
        min_value=int(df['price'].min()),
        max_value=int(df['price'].max()),
        value=(50, 500)
    )

    superhost_only = st.checkbox("⭐ Superhosts only", False)

# Apply filters
filtered_df = df[
    (df['neighbourhood_cleansed'].isin(neighborhood)) &
    (df['room_type'].isin(room_type)) &
    (df['host_type'].isin(host_type)) &
    (df['price'].between(*price_range)) &  ((df['host_is_superhost'] == True) if superhost_only else True)
]

# Show toast notification with filtered count
st.toast(f"✅ Filtered from {len(df):,} to {len(filtered_df):,} listings", icon="✔️")

# Display warning if no results
if filtered_df.empty:
    st.warning("No listings match the selected filters. Please adjust your filters.")

# Key Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Listings", len(filtered_df))
col2.metric("Avg Price", f"${filtered_df['price'].mean():.0f}")
col3.metric("Avg Rating", f"{filtered_df['review_scores_rating'].mean():.1f}")
col4.metric("Superhosts", f"{filtered_df['host_is_superhost'].sum()}")


# Key Distributions
st.write("**📌 Key Distributions**")
col1, col2, col3 = st.columns(3)
col1.write(f"**Median:** ${filtered_df['price'].median():.0f}")
col2.write(f"**Range:** ${filtered_df['price'].min():.0f}-${filtered_df['price'].max():.0f}")
col3.write(f"**Top Area:** {filtered_df['neighbourhood_cleansed'].mode()[0]}")

# Tab layout
tab1, tab2, tab3 = st.tabs(["🌍 Spatial Analysis", "💲 Pricing Insights", "👥 Host & Reviews"])

with tab1:
    # 1. Price Distribution Map
    st.subheader("Price Distribution by Location")
    fig1 = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        color="price",
        size="number_of_reviews",
        hover_name="name",
        hover_data=["room_type", "review_scores_rating"],
        color_continuous_scale='RdBu',
        zoom=11,
        height=500
    )
    fig1.update_layout(mapbox_style="carto-positron",coloraxis_colorbar_title='Price',  coloraxis_colorbar_len=0.9 )
    st.plotly_chart(fig1, use_container_width=True)
    
    # 2. Neighborhood Analysis
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Listings by Neighborhood")
        fig2 = px.bar(
            filtered_df['neighbourhood_cleansed'].value_counts().reset_index(),
            x='count',
            y='neighbourhood_cleansed', color='neighbourhood_cleansed', title="Distribution of Listings Across Neighborhoods",
            orientation='h', labels={'count':"No. of Listings", 'neighbourhood_cleansed':"Neighbourhood"}
            , color_discrete_sequence=px.colors.qualitative.Pastel2
        )
        fig2.update_traces(
        texttemplate='%{x}',
         textposition='outside'
            )
        fig2.update_layout( showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.subheader("Avg Price by Neighborhood")
        fig3 = px.bar(
            filtered_df.groupby('neighbourhood_cleansed')['price'].mean().sort_values().reset_index(),
            x='price',  title="Neighborhood-wise Average Pricing",
            y='neighbourhood_cleansed', color='neighbourhood_cleansed', labels={'price':"Price", 'neighbourhood_cleansed':"Neighbourhood"},
            orientation='h', color_discrete_sequence=px.colors.qualitative.Pastel1
        )
        fig3.update_traces(
        texttemplate='%{x:.0f}',
         textposition='outside'
            )
        fig3.update_layout( showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)


    # 3. Availability Insights
    st.subheader("Availability Distribution")
    fig13 = px.histogram(
        filtered_df,
        x="availability_365",
        nbins=30,  
        title="Distribution of Days Available per Year",
        labels={"availability_365": "Days Available (out of 365)"}, color_discrete_sequence=["#6CC1C3"] 
    )
    median_days = filtered_df["availability_365"].median()
    fig13.add_vline(
    x=median_days,
    line_dash="dash",
    line_color="grey",
    annotation_text=f"Median: {median_days:.0f}",
    annotation_position="top right"
)
    fig13.update_layout(  yaxis_title="Number of Listings",
    xaxis_title="Days Available per Year",) 
    st.plotly_chart(fig13, use_container_width=True)


with tab2:
    # 3. Price Distribution
    st.subheader("Price Distribution Analysis")
    col1, col2 = st.columns(2)
    with col1:
        fig4 = px.histogram(
            filtered_df,
            x='price',
            nbins=30,
            title="Price Distribution",color_discrete_sequence=["#81BC79"] 
        )
        median_price = filtered_df["price"].median()
        
        fig4.add_vline(
    x=median_price,
    line_dash="dash",
    line_color="grey",
    annotation_text=f"Median: ${median_price:.0f}",
    annotation_position="top right"
)
        fig4.update_layout(xaxis_title="Price (USD)", yaxis_title="Count")
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        fig5 = px.box(
            filtered_df,
            x='room_type',
            y='price', color= 'room_type', 
            title="Price by Room Type", color_discrete_sequence=px.colors.qualitative.Pastel 
        )
        fig5.update_layout(showlegend=False, yaxis_title="Price (USD)", xaxis_title="Room Type")
        st.plotly_chart(fig5, use_container_width=True)
    
    # 4. Property Attributes
    st.subheader("Property Attributes Impact")
    col1, col2 = st.columns(2)
    with col1:
        fig6 = px.scatter(
            filtered_df,
            x='bedrooms',
            y='price',
            color='room_type',
            trendline="lowess",
            title="Price vs Bedrooms",color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig6.update_layout(xaxis_title="No. of Bedrooms", yaxis_title="Price (USD)", legend_title_text='Room Type')
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        fig7 = px.scatter(
            filtered_df,
            x='accommodates',
            y='price',
            color='neighbourhood_cleansed',
            title="Price vs Accommodates", color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig7.update_layout(xaxis_title="No. of Accomodates", yaxis_title="Price (USD)",  legend_title_text='NeighbourHood')
        st.plotly_chart(fig7, use_container_width=True)
    
    # 5. Price vs Rating
    st.subheader("Price vs. Rating")
    fig12 = px.scatter(
        filtered_df,
        x="price",
        y="review_scores_rating",
        color="room_type",
        trendline="ols",
        title="Prices vs Ratings", color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig12.update_layout(xaxis_title="Price (USD)", yaxis_title="Rating (1-5)",legend_title_text='Room Type')
    st.plotly_chart(fig12, use_container_width=True)


with tab3:
    # 5. Host Analysis
    st.subheader("Host Characteristics")
    col1, col2 = st.columns(2)
    with col1:
        fig8 = px.pie(
            filtered_df,
            names='host_type', color_discrete_sequence=px.colors.qualitative.Pastel, 
            title="Host Type Distribution"
        )
        fig8.update_traces(pull=0.02, textinfo='percent+label')
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        fig9 = px.box(
            filtered_df,
            x='host_type',
            y='price',
            color='host_is_superhost',
            title="Price by Host Type", color_discrete_sequence=px.colors.qualitative.Pastel1
        )
        fig9.update_layout(xaxis_title="Type of Host", yaxis_title="Price (USD)", legend_title_text='Host is Superhost')
        st.plotly_chart(fig9, use_container_width=True)
    
    # 6. Review Analysis
    st.subheader("Review Insights")
    col1, col2 = st.columns(2)
    with col1:
        fig10 = px.scatter(
            filtered_df,
            x='number_of_reviews',
            y='review_scores_rating',
            color='price',
            title="Rating vs Number of Reviews"
            ,color_discrete_sequence=px.colors.qualitative.Pastel2_r
        )
        fig10.update_layout(xaxis_title="No. of Reviews", yaxis_title="Rating (1-5)",coloraxis_colorbar_title='Price',  coloraxis_colorbar_len=0.9
                           )
        st.plotly_chart(fig10, use_container_width=True)
    
    with col2:
        fig11 = px.scatter(
            filtered_df,
            x='reviews_per_month',
            y='price',
            color='review_scores_rating',  color_continuous_scale='Viridis',
            title="Price vs Review Frequency"
        )
        fig11.update_layout(xaxis_title='Reviews per Month', yaxis_title='Price (USD)',
                            coloraxis_colorbar_title='Rating',  coloraxis_colorbar_len=0.9
                           )
        st.plotly_chart(fig11, use_container_width=True)
    prop_reviews = filtered_df.groupby("property_type")["number_of_reviews"].mean().sort_values(ascending=False).head(10).reset_index()


# Raw data
#view and Download the filtered data
if st.checkbox("Show filtered data"):
    st.dataframe(filtered_df)
    st.download_button(
        label="Download CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='airbnb_data.csv',
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.markdown("Built with 💛 by Mohit Kumar | Last Updated: July 2025")
st.write("")
st.write("")
st.write("")
st.write("") 


