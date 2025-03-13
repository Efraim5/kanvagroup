import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
st.set_page_config(layout='wide')

st.title("🏠Optimalisasi Harga Properti Airbnb di beberapa kota di Eropa")
st.write(
    "By Group 5 Kanva. Team Members: Kevin William, Veraldo Efraim, Novisna Lintang Negari, Adila."
)
st.sidebar.title("🔹 Main Menu")
page = st.sidebar.radio("Go to", ["Home", "Data Exploration", "Goal"])

# Display different pages based on selection
if page == "Home":
    st.title("Price Reasonable")

df = pd.read_csv('combined_all_data.csv')

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

# Display results
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

# Tambahkan slider untuk mengatur rentang harga "reasonable"
# Price reasonability classification
min_price, max_price = st.slider(
    "Pilih Rentang Harga per Orang (€)",
    min_value=0, max_value=200, value=(30, 90)
    )

# 📊 Price Per Person Analysis CODE
# Calculate price per person
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].between(min_price, max_price)

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

# 🏠 Room Type vs Harga Reasonable
# Tambahkan kolom price per person & label reasonable
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].apply(lambda x: 1 if min_price <= x <= max_price else 0)

# Hitung proporsi listing reasonable berdasarkan Room Type
df_clean_room = df.dropna(subset=['room_type', 'price_reasonable'])
room_group = df_clean_room.groupby('room_type')['price_reasonable'].mean().sort_values()

# Buat plot Room Type vs Harga Reasonable
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(room_group.index, room_group.values * 100, color="#027A94")
ax.set_xlabel("Persentase Listing dengan Harga Reasonable (%)")
ax.set_title("Room Type vs Harga Reasonable")
ax.grid(axis='x', linestyle='--', alpha=0.6)

for bar in bars:
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.1f}%", va='center')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.write("### 🏠 Room Type vs Harga Reasonable")
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

# 📊 Capacity vs Reasonable Price Listings CODE
# Tambahkan kolom price per person & label reasonable
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].apply(lambda x: 1 if min_price <= x <= max_price else 0)

# Hitung proporsi reasonable berdasarkan kapasitas
df_clean_capacity = df.dropna(subset=['person_capacity', 'price_reasonable'])
capacity_reasonable = df_clean_capacity.groupby('person_capacity')['price_reasonable'].mean() * 100

# Buat plot Capacity vs Reasonable Price Listings
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(capacity_reasonable.index.astype(str), capacity_reasonable.values, color='#007E8A')
ax.set_xlabel('Kapasitas Orang')
ax.set_ylabel('Persentase Listing dengan Harga Reasonable (%)')
ax.set_title('Capacity vs Harga Reasonable')
ax.set_ylim(0, 100)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.write("### 👥 Kapasitas vs Harga Reasonable")
st.pyplot(fig)

# 😊 Guest Satisfaction vs Harga Reasonable CODE
# Tambahkan kolom price per person & label reasonable
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].apply(lambda x: 1 if min_price <= x <= max_price else 0)

# Hitung proporsi listing reasonable berdasarkan rating kepuasan tamu
df_clean_satisfaction = df.dropna(subset=['guest_satisfaction_overall', 'price_reasonable'])
df_clean_satisfaction['satisfaction_bin'] = pd.cut(
    df_clean_satisfaction['guest_satisfaction_overall'],
    bins=[0, 50, 60, 70, 80, 90, 100],
    labels=['≤50', '51–60', '61–70', '71–80', '81–90', '91–100']
)

satisfaction_reasonable = df_clean_satisfaction.groupby('satisfaction_bin')['price_reasonable'].mean() * 100

# Buat plot Customer Satisfaction vs Harga Reasonable
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(satisfaction_reasonable.index.astype(str), satisfaction_reasonable.values, color='#007E8A')
ax.set_xlabel('Guest Satisfaction Rating')
ax.set_ylabel('Persentase Listing dengan Harga Reasonable (%)')
ax.set_title('Guest Satisfaction vs Harga Reasonable')
ax.set_ylim(0, 100)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height:.1f}%', ha='center')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.write("### 😊 Guest Satisfaction vs Harga Reasonable")
st.pyplot(fig)


df_clean = df.dropna(subset=['person_capacity', 'realSum'])
df_clean['price_per_person'] = df_clean['realSum'] / df_clean['person_capacity']

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


#🏡 Superhost vs Harga Reasonable CODE
# Tambahkan kolom price per person & label reasonable
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].apply(lambda x: 1 if min_price <= x <= max_price else 0)

# Hitung persentase reasonable price berdasarkan status superhost
superhost_reasonable = df.groupby('host_is_superhost')['price_reasonable'].mean() * 100

# Buat plot
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(['Non-Superhost', 'Superhost'], superhost_reasonable.values, color='#007E8A')

# Tambahkan label persen di ujung bar
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center')

ax.set_xlabel('Persentase Listing dengan Harga Reasonable (%)')
ax.set_title('Superhost vs Harga Reasonable')
ax.set_xlim(0, 100)
plt.tight_layout()

# Tampilkan plot
st.write("### 🏡 Superhost vs Harga Reasonable")
st.pyplot(fig)

# 📅 Day Type vs Harga Reasonable code
# Hitung persentase listing reasonable berdasarkan Day Type
daytype_reasonable = df.groupby('Day_Type')['price_reasonable'].mean() * 100

# Buat plot Day Type vs Harga Reasonable
fig3, ax3 = plt.subplots(figsize=(7, 4))
bars3 = ax3.barh(['Working Day', 'Holiday'], daytype_reasonable.values, color='#007E8A')

# Tambahkan label persentase di samping bar
for bar in bars3:
    width = bar.get_width()
    ax3.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center')

ax3.set_xlabel('Persentase Listing dengan Harga Reasonable (%)')
ax3.set_title('Day Type vs Harga Reasonable')
ax3.set_xlim(0, 100)
plt.tight_layout()

# Tampilkan plot 
st.write("### 📅 Day Type vs Harga Reasonable")
st.pyplot(fig3)

# 🏢 Business Host vs Harga Reasonable CODE
# Buat kolom price_per_person & price_reasonable
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].apply(lambda x: 1 if min_price <= x <= max_price else 0)

# Hitung persentase listing reasonable berdasarkan status bisnis host
biz_reasonable = df.groupby('biz')['price_reasonable'].mean() * 100

# Buat plot Business Host vs Harga Reasonable
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(['Non-Business Host', 'Business Host'], biz_reasonable.values, color='#007E8A')

for bar in bars:
    width = bar.get_width()
    ax.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center')

ax.set_xlabel('Persentase Listing dengan Harga Reasonable (%)')
ax.set_title('Business Host Status vs Harga Reasonable')
ax.set_xlim(0, 100)
plt.tight_layout()

# Tampilkan plot di Streamlit
st.write("### 🏢 Business Host vs Harga Reasonable")
st.pyplot(fig)

# 🛏 Bedrooms vs Harga Reasonable
# Tambahkan kolom price per person & label reasonable
df['price_per_person'] = df['realSum'] / df['person_capacity']
df['price_reasonable'] = df['price_per_person'].apply(lambda x: 1 if min_price <= x <= max_price else 0)

# Hitung jumlah listing & rata-rata reasonable berdasarkan jumlah kamar tidur
df_clean_bedrooms = df.dropna(subset=['bedrooms', 'price_reasonable'])
bedroom_group = df_clean_bedrooms.groupby('bedrooms')['price_reasonable'].agg(['count', 'mean'])
bedroom_group = bedroom_group[bedroom_group['count'] >= 30]

# Buat plot Bedrooms vs Harga Reasonable
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(bedroom_group.index.astype(str), bedroom_group['mean'] * 100, color='#007E8A')
ax.set_xlabel('Jumlah Kamar Tidur')
ax.set_ylabel('Persentase Listing dengan Harga Reasonable (%)')
ax.set_title('Bedrooms vs Harga Reasonable')
ax.set_ylim(0, 100)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f'{height:.1f}%', ha='center')

plt.tight_layout()

# Tampilkan plot di Streamlit
st.write("### 🛏 Bedrooms vs Harga Reasonable")
st.pyplot(fig)

