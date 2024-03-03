import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import locale

# Load dataset
bikesharing_df = pd.read_csv("dashboard/bikesharing.csv")

# Tampilkan data jika berhasil dibaca
#if bikesharing_df is not None:
#    st.write(bikesharing_df)
#else:
#    st.error("File CSV tidak dapat dibaca.")

# Setup
st.set_option('deprecation.showPyplotGlobalUse', False)

st.cache(allow_output_mutation=True)
def set_locale():
    try:
        locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
    except locale.Error as e:
        print("Kesalahan saat mengatur locale:", e)
        print("Menggunakan locale default sistem.")
        locale.setlocale(locale.LC_NUMERIC, '')

# Panggil fungsi set_locale() di awal aplikasi
set_locale()

#locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

# Mengonversi tipe data kolom 'dteday'
bikesharing_df['dteday'] = pd.to_datetime(bikesharing_df['dteday'])

min_date = bikesharing_df['dteday'].min()
max_date = bikesharing_df['dteday'].max()

with st.sidebar:
    # Menambahkan gambar
    st.image("dashboard/foto_sepeda.jpg", width=300, use_column_width=True, output_format='JPEG')
    st.markdown("<style>img {border-radius: 10px;}</style>", unsafe_allow_html=True)

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_data = bikesharing_df[(bikesharing_df['dteday'] >= start_date) & (bikesharing_df['dteday'] <= end_date)]

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Order Harian')

# Menghitung total sepeda yang disewa pada tanggal yang dipilih
total_cnt = filtered_data['cnt'].sum()

# Menghitung total penyewa yang registered dan casual pada tanggal yang dipilih
total_registered = filtered_data['registered'].sum()
total_casual = filtered_data['casual'].sum()

# Menghitung persentase jumlah penyewa yang registered dan casual dari total sepeda yang disewa
percent_registered = (total_registered / total_cnt) * 100
percent_casual = (total_casual / total_cnt) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sepeda Disewa", value=f'{locale.format_string("%d", total_cnt, grouping=True)}')

with col2:
    st.metric("Persentase Penyewa Registered", value=f'{percent_registered:.1f}%')

with col3:
    st.metric("Persentase Penyewa Casual", value=f'{percent_casual:.1f}%')


# Plot grafik total sepeda yang disewa beserta tanggalnya
plt.figure(figsize=(10, 6), facecolor="#F5F5F5")
plt.plot(filtered_data['dteday'], filtered_data['cnt'], linestyle='-', color='#64B5F6')
plt.tight_layout()
st.pyplot()

st.subheader('Order Berdasarkan Working Day')

# Menghitung total penyewa sepeda pada kolom 'workingday'
workingday_total = filtered_data.groupby('workingday')['cnt'].sum()

# Plot barchart untuk total penyewa pada kolom 'workingday'
plt.figure(figsize=(8, 5), facecolor="#F5F5F5")
sns.barplot(x=workingday_total.index, y=workingday_total.values, color='#64B5F6')
plt.xlabel('Working Day (0 = Akhir Pekan, 1 = Hari Kerja)')
plt.tight_layout()
st.pyplot()

st.subheader('Klaster Penyewa Sepeda Berdasarkan Musim dan Cuaca')

# Daftar lengkap klaster
complete_clusters = [0, 1, 2, 3]

# Menghitung total penyewa pada masing-masing klaster
total_rentals = filtered_data.groupby('klaster')[['casual', 'registered']].sum().sum(axis=1)

# Menambahkan nilai 0 untuk klaster yang tidak ada dalam data
for cluster in complete_clusters:
    if cluster not in total_rentals.index:
        total_rentals[cluster] = 0

total_rentals = total_rentals.sort_index()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Penyewa Klaster 0", value=locale.format_string("%d", total_rentals[0], grouping=True))

with col2:
    st.metric("Total Penyewa Klaster 1", value=locale.format_string("%d", total_rentals[1], grouping=True))

with col3:
    st.metric("Total Penyewa Klaster 2", value=locale.format_string("%d", total_rentals[2], grouping=True))

with col4:
    st.metric("Total Penyewa Klaster 3", value=locale.format_string("%d", total_rentals[3], grouping=True))

# Menentukan warna untuk setiap bar
#colors = ['#64B5F6', '#2196F3', '#1976D2', '#1565C0']
colors = ['#64B5F6', '#64B5F6', '#808080', '#808080']

# Membuat plot hasil klastering
plt.figure(figsize=(10, 6), facecolor="#F5F5F5")
plt.barh(total_rentals.index, total_rentals.values, color=colors)
plt.tight_layout()
st.pyplot(plt)

st.write('**Klaster 0** : Musim Semi/Musim Panas - Cerah')
st.write('**Klaster 1** : Musim Dingin/Musim Gugur - Cerah')
st.write('**Klaster 2** : Musim Semi/Musim Panas - Tidak Cerah')
st.write('**Klaster 3** : Musim Dingin/Musim Gugur - Tidak cerah')
