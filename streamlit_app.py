import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("🏠Optimalisasi Harga Properti Airbnb di beberapa kota di Eropa")
st.write(
    "Anggota: Kevin William, Veraldo Efraim, Novisna Lintang Negari, Adila."
)
st.sidebar.title("🔹 Main Menu")
page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Goal"])

# Display different pages based on selection
if page == "Home":
    st.title("Price Reasonable")

df = pd.read_csv('combined_all_data.csv')

price_reasonable = st.slider('Price Reasonable',30,90)

# Clean and prepare
df_clean = df.dropna(subset=['realSum', 'person_capacity', 'guest_satisfaction_overall'])
df_clean['price_per_person'] = df_clean['realSum'] / df_clean['person_capacity']

# Hitung % listing yang harganya "masuk akal"
df_clean['price_reasonable'] = df_clean['price_per_person'].between(30, 90)
reasonable_pct = df_clean['price_reasonable'].mean() * 100
df_clean['price_level'] = pd.cut(
df_clean['price_per_person'],
bins=[0, 30, 60, 90, 9999],
labels=['Low', 'Moderate', 'High', 'Very High']  )

# Calculate average guest satisfaction by price level
satisfaction_by_price = df_clean.groupby('price_level')['guest_satisfaction_overall'].mean()

# Display results in Streamlit
st.write(f"### ✅ Reasonable Price Listings: {reasonable_pct:.1f}%")
st.write("### 📊 Guest Satisfaction by Price Level")
st.dataframe(satisfaction_by_price)

# Visualization 
st.bar_chart(satisfaction_by_price)

# Preprocessing
df_clean = df.dropna(subset=['realSum', 'person_capacity', 'guest_satisfaction_overall'])
df_clean['price_per_person'] = df_clean['realSum'] / df_clean['person_capacity']
df_clean['price_reasonable'] = df_clean['price_per_person'].between(30, 90)

# Count reasonable vs unreasonable listings
reasonable = df_clean['price_reasonable'].sum()
unreasonable = len(df_clean) - reasonable

# Pie chart setup
labels = ['Reasonable Price', 'Unreasonable Price']
sizes = [reasonable, unreasonable]
colors = ['#4CAF50', '#E0E0E0']
explode = (0.1, 0)  # Highlight reasonable prices

# Plotting pie chart
fig, ax = plt.subplots(figsize=(6, 6))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors, explode=explode,
    autopct='%1.1f%%', startangle=140, textprops={'fontsize': 12}
    )

# Styling
plt.setp(autotexts, size=14, weight="bold", color="white")
ax.set_title('📊 Listing Price Reasonability', fontsize=16, fontweight='bold')
ax.axis('equal')  # Ensure circular pie chart

# Display results
st.write("### ✅ Price Reasonability Analysis")
st.write(f"🔹 **Reasonable Listings:** {reasonable} ({(reasonable / len(df_clean)) * 100:.1f}%)")
st.write(f"🔹 **Unreasonable Listings:** {unreasonable} ({(unreasonable / len(df_clean)) * 100:.1f}%)")

# Show Pie Chart 
st.pyplot(fig)

# Calculate price per person
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].between(30, 90)

# Create Histogram
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df['price_per_person'], bins=100, color='teal', alpha=0.8, edgecolor='black')
ax.axvspan(30, 90, color='red', alpha=0.3, label='Reasonable Range (€30–90)')
ax.set_title('Distribution of Price per Person')
ax.set_xlabel('Price per Person (€)')
ax.set_ylabel('Number of Listings')
ax.set_xlim(0, 700)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.5)
  
# Show plot
st.write(f"### 📊 Price Per Person Analysis")
st.pyplot(fig)

df_clean = df.dropna(subset=['realSum', 'person_capacity', 'room_type'])
df_clean['price_per_person'] = df_clean['realSum'] / df_clean['person_capacity']
df_clean['price_reasonable'] = df_clean['price_per_person'].between(30, 90)

# Group by room_type to calculate proportion of reasonable prices
room_group = df_clean.groupby('room_type')['price_reasonable'].mean().sort_values()

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(room_group.index, room_group.values * 100, color="#027A94")
ax.set_xlabel("Percentage of Reasonable Price Listings (%)")
ax.set_title("Room Type vs. Reasonable Price Listings")
ax.grid(axis='x', linestyle='--', alpha=0.6)

# Add percentage labels
for bar in bars:
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
      f"{bar.get_width():.1f}%", va='center')

plt.tight_layout()

# Show Plot
st.write(f"### 🏠 Room Type vs. Reasonable Price Listings")
st.pyplot(fig)

df_clean = df.dropna(subset=['cleanliness_rating', 'price_reasonable'])

# Binning cleanliness ratings into categories
df_clean['cleanliness_bin'] = pd.cut(df_clean['cleanliness_rating'], 
              bins=[0, 6, 7, 8, 9, 10], 
              labels=['≤6', '7', '8', '9', '10'])

 # Calculate the percentage of reasonable price listings by cleanliness rating
clean_rating = df_clean.groupby('cleanliness_bin')['price_reasonable'].mean() * 100

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(clean_rating.index.astype(str), clean_rating.values, color='#007E8A')
    
ax.set_xlabel("Cleanliness Rating")
ax.set_ylabel("Percentage of Reasonable Price Listings (%)")
ax.set_title("Cleanliness vs. Reasonable Price Listings")
ax.set_ylim(0, 100)
    
# Add percentage labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center')

plt.tight_layout()

# Show Plot 
st.write(f"### 🧼 Cleanliness vs. Reasonable Price Listings")
st.pyplot(fig)

df['price_per_person'] = df['realSum'] / df['person_capacity']
#Filter out outliers (above €200 per person)
df_filtered = df[df['price_per_person'] <= 200]
# Create histogram
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(df_filtered['price_per_person'], bins=30, color='#008B8B', edgecolor='black')

# Highlight reasonable price range (€30–90)
ax.axvspan(30, 90, color='lightcoral', alpha=0.3, label='Reasonable Range (€30–90)')

# Labels and title
ax.set_title("Distribution of Price per Person")
ax.set_xlabel("Price per Person (€)")
ax.set_ylabel("Number of Listings")
ax.legend()
    
plt.tight_layout()


# Ensure necessary columns exist
required_columns = {'realSum', 'person_capacity'}
if not required_columns.issubset(df.columns):
    st.error(f"CSV file must contain columns: {required_columns}")
else:
    # Calculate price per person
    df['price_per_person'] = df['realSum'] / df['person_capacity']

    # Filter out outliers (above €200 per person)
    df_filtered = df[df['price_per_person'] <= 200]

    # Create histogram
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df_filtered['price_per_person'], bins=30, color='#008B8B', edgecolor='black')

    # Highlight reasonable price range (€30–90)
    ax.axvspan(30, 90, color='lightcoral', alpha=0.3, label='Reasonable Range (€30–90)')

    # Labels and title
    ax.set_title("Distribution of Price per Person")
    ax.set_xlabel("Price per Person (€)")
    ax.set_ylabel("Number of Listings")
    ax.legend()
        
    plt.tight_layout()

    # Show Plot
    st.write(f"### 💰 Distribution of Price per Person")
    st.pyplot(fig)

# Tambahkan kolom target: price_reasonable (1 jika harga per orang antara €30–90, 0 jika tidak)
df['price_reasonable'] = df['price_per_person'].apply(lambda x: 1 if 30 <= x <= 90 else 0)

required_columns = {'guest_satisfaction_overall', 'price_reasonable'}
if not required_columns.issubset(df.columns):
    st.error(f"CSV file must contain columns: {required_columns}")
else:
    # Drop NA values from necessary columns
    df_clean = df.dropna(subset=['guest_satisfaction_overall', 'price_reasonable'])

    # Binning guest satisfaction ratings
    df_clean['satisfaction_bin'] = pd.cut(
    df_clean['guest_satisfaction_overall'],
    bins=[0, 50, 60, 70, 80, 90, 100],
    labels=['≤50', '51–60', '61–70', '71–80', '81–90', '91–100']
    )

    # Calculate percentage of reasonable price listings per satisfaction rating
    satisfaction_reasonable = df_clean.groupby('satisfaction_bin')['price_reasonable'].mean() * 100

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(satisfaction_reasonable.index.astype(str), satisfaction_reasonable.values, color='#007E8A')

    # Labels
    ax.set_xlabel("Guest Satisfaction Rating")
    ax.set_ylabel("Percentage of Reasonable Price Listings (%)")
    ax.set_title("Guest Satisfaction vs. Reasonable Price Listings")

    # Add percentage labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1, f"{height:.1f}%", ha='center')

    ax.set_ylim(0, 100)
    plt.tight_layout()

    # Show plot 
    st.write(f"### 😊 Guest Satisfaction vs. Reasonable Price Listings")
    st.pyplot(fig)

df_clean = df.dropna(subset=['person_capacity', 'realSum'])
df_clean['price_per_person'] = df_clean['realSum'] / df_clean['person_capacity']

# Price reasonability classification
min_price, max_price = st.slider(
    "Select Reasonable Price Range (€)",
    min_value=10, max_value=100, value=(30, 90)
    )
df_clean['price_reasonable'] = df_clean['price_per_person'].apply(lambda x: 1 if min_price <= x <= max_price else 0)

# Compute proportion of reasonable price listings per capacity
capacity_reasonable = df_clean.groupby('person_capacity')['price_reasonable'].mean() * 100

# Plot
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(capacity_reasonable.index.astype(str), capacity_reasonable.values, color='#007E8A')
ax.set_xlabel('Person Capacity')
ax.set_ylabel('Percentage of Reasonable Price Listings (%)')
ax.set_title('Capacity vs Reasonable Price Listings')
ax.set_ylim(0, 100)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Add percentage labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center')

# Show Plot
st.write(f"### 📊 Capacity vs Reasonable Price Listings")
st.pyplot(fig)
