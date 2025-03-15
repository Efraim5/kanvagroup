import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("🏠Optimalisasi Harga Properti Airbnb di beberapa kota di Eropa")
st.write(
    "By Group 5 Kanva. Team Members: Kevin William, Veraldo Efraim, Novisna Lintang Negari, Adila."
)
st.sidebar.title("Main Menu")
page = st.sidebar.radio("Go to", ["Home", "Goal", "EDA & Data Pre-processing","Business Recommendation","Conclusion"])

# Display different pages based on selection

if page =="Home":
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

    #   Display results
    st.write(f"### ✅ Reasonable Price Listings: {reasonable_pct:.1f}%")
    col1, col2, col3= st.columns(3) 
    with col1:
        st.write("### 📊 Guest Satisfaction by Price Level")
        st.dataframe(satisfaction_by_price)

        # Visualization 
        st.bar_chart(satisfaction_by_price)

    with col2:
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

    with col3:
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

    with col3: 
        # 📊 Price Per Person Analysis CODE
        # Calculate price per person
        df['price_per_person'] = df['realSum'] / df['person_capacity']
        df['price_reasonable'] = df['price_per_person'].between(0, 200)

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

    # Tambahkan slider untuk mengatur rentang harga "reasonable"
    # Price reasonability classification
    min_price, max_price = st.slider(
        "Pilih Rentang Harga per Orang (€)",
        min_value=0, max_value=200, value=(30, 90)
        )



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

elif page == "Goal":
    st.title("Goal")
    st.write("Menentukan harga optimal bagi pelanggan agar host dapat menetapkan biaya sewa yang lebih menguntungkan.")

elif page == "EDA & Data Pre-processing":
    st.title("EDA & Data Pre-processing")
    # Membaca dataset
    df = pd.read_csv("combined_all_data.csv")

    #⚠️ Cek Data Duplikat KODE
    # Menghitung jumlah nilai yang hilang (missing values) di setiap kolom
    missing_count = df.isnull().sum()

    # Menghitung persentase nilai yang hilang
    missing_percentage = (missing_count / len(df)) * 100

    # Membuat DataFrame ringkasan missing values
    missing_summary = pd.DataFrame({
        'Jumlah Missing': missing_count,
        'Persentase Missing (%)': missing_percentage.round(2)
    })

    # Menghitung jumlah baris yang duplikat
    duplicate_count = df.duplicated().sum()

    # Membuat aplikasi Streamlit
    st.title("📊 Laporan Pembersihan Data")

    # Menampilkan ringkasan nilai yang hilang
    st.subheader("🔍 Ringkasan Missing Values")
    st.dataframe(missing_summary)  # Menampilkan tabel interaktif

    # Menampilkan jumlah data duplikat
    st.subheader("⚠️ Cek Data Duplikat")
    st.write(f"**Total Baris Duplikat:** {duplicate_count}")

    #📦 Boxplot Fitur Numerik terhadap Harga CODE
    features_to_check = [
        'realSum',                 # Target (Harga)
        'person_capacity',         # Kapasitas tamu
        'bedrooms',                # Jumlah kamar tidur
        'cleanliness_rating',      # Rating kebersihan
        'guest_satisfaction_overall', # Kepuasan tamu
        'dist',                    # Jarak ke pusat kota
        'metro_dist',              # Jarak ke metro
        'attr_index',              # Indeks atraksi wisata
        'rest_index'               # Indeks restoran
    ]

    # Hapus nilai yang hilang pada fitur yang dianalisis
    df_clean = df[features_to_check].dropna()

    # Membuat visualisasi boxplot
    st.subheader("📦 Boxplot Fitur Numerik terhadap Harga")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.boxplot(df_clean.values, vert=True, patch_artist=True, labels=features_to_check)
    ax.set_title("Boxplot Fitur Numerik terhadap Harga (realSum)")
    ax.set_xticklabels(features_to_check, rotation=45)
    ax.set_ylabel("Nilai Fitur")

    # Menampilkan plot di Streamlit
    st.pyplot(fig)

    df_cleaned = df[df['realSum'] <= 3000]

    # Daftar fitur numerik yang relevan
    relevant_features = [
        'realSum', 'person_capacity', 'bedrooms', 'cleanliness_rating',
        'guest_satisfaction_overall', 'dist', 'metro_dist',
        'attr_index', 'rest_index'
    ]

    # Salin subset data
    df_clean = df_cleaned[relevant_features].copy()

    # Menghapus outlier menggunakan metode IQR
    for col in df_clean.columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]

    # Tampilkan jumlah data sebelum dan sesudah pembersihan
    st.write(f"📌 **Jumlah data sebelum pembersihan**: {df.shape[0]}")
    st.write(f"✅ **Jumlah data setelah pembersihan**: {df_clean.shape[0]}")

    # Plot hasil setelah pembersihan outlier
    st.subheader("📦 Boxplot Setelah Menghapus Outlier")

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.boxplot(df_clean.values, vert=True, patch_artist=True, labels=relevant_features)
    ax.set_title("Boxplot Setelah Menghapus Outlier (Fitur Relevan)")
    ax.set_xticklabels(relevant_features, rotation=45)
    ax.set_ylabel("Nilai Fitur")

    # Tampilkan plot 
    st.pyplot(fig)

    features_to_check = [
        'realSum', 'person_capacity', 'bedrooms', 'cleanliness_rating',
        'guest_satisfaction_overall', 'dist', 'metro_dist', 'attr_index', 'rest_index'
    ]
    
    df_clean = df[features_to_check].dropna()
    
    # Tampilkan preview data
    st.write("### 📋 Data Preview")
    st.dataframe(df_clean.head())
    
    #   Pilih fitur untuk visualisasi boxplot
    selected_feature = st.selectbox("Pilih fitur untuk Boxplot", features_to_check)
    
    # Buat plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(df_clean[selected_feature], vert=False)
    ax.set_title(f"Boxplot: {selected_feature}")
    ax.set_xlabel(selected_feature)
    
    st.pyplot(fig)

   # Menghapus outlier ekstrim dari realSum (misalnya > 3000)
    df_cleaned = df[df['realSum'] <= 3000]
    
    # Fitur numerik yang relevan
    relevant_features = [
        'realSum', 'person_capacity', 'bedrooms', 'cleanliness_rating',
        'guest_satisfaction_overall', 'dist', 'metro_dist',
        'attr_index', 'rest_index'
    ]
    
    # Menyalin subset data
    df_clean = df_cleaned[relevant_features].copy()
    
    # Menghapus outlier menggunakan metode IQR
    for col in df_clean.columns:
        Q1 = df_clean[col].quantile(0.25)
        Q3 = df_clean[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
    
    # Menampilkan hasil dalam bentuk boxplot
    st.write("### Boxplot Setelah Menghapus Outlier")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.boxplot(df_clean.values, vert=False, labels=df_clean.columns)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)  
    

elif page == "Business Recommendation":
    st.markdown("<h1 style='text-align: center; color: white;'>Business Recommendation</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### 📈 **Strategi Optimasi Harga**
    
    🔹 **Sesuaikan Harga Secara Optimal**  
    Sesuaikan harga berdasarkan faktor utama seperti **lokasi, rating kebersihan, dan tipe kamar** agar selaras dengan tren pasar.  
    Gunakan **model harga dinamis** untuk memaksimalkan pendapatan berdasarkan permintaan, musim, dan harga pesaing.  

    🔹 **Tingkatkan Fitur Bernilai Tinggi**  
    Properti dengan **rating tamu dan kebersihan yang lebih tinggi** cenderung dapat menetapkan harga premium.  
    Dorong host untuk meningkatkan kualitas layanan agar mendapatkan rating yang lebih baik.  
    Soroti **kedekatan dengan pusat kota dan stasiun metro** sebagai nilai jual utama dalam deskripsi listing.  

    🔹 **Perkuat Daya Saing**  
    Bandingkan harga dengan pesaing di lokasi serupa untuk memastikan harga yang kompetitif namun tetap menguntungkan.  
    Gunakan wawasan dari **model prediktif** untuk membantu host menetapkan harga optimal dan meningkatkan total pendapatan.  
""", unsafe_allow_html=True) 

elif page == "Conclusion":
    st.markdown("<h1 style='text-align: center; color: white;'>Conclusion</h1>", unsafe_allow_html=True)
    st.markdown("""
        🔹 **Host Airbnb dapat dengan percaya diri menggunakan prediksi ini untuk menetapkan harga yang kompetitif dan optimal.**  
        🔹 **Menyarankan harga yang lebih akurat** sesuai dengan ekspektasi pelanggan.  
        🔹 **Model harga yang lebih baik** membantu mengurangi pembatalan dan meningkatkan kepuasan tamu.  
        🔹 **Tingkat hunian yang lebih tinggi** dan pemesanan ulang dapat dicapai dengan strategi harga yang tepat.  
    """, unsafe_allow_html=True)
