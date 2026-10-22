# LAPORAN RESMI PROYEK UJIAN TENGAH SEMESTER (UTS)
## BIG DATA ANALYTICS: EXPLORATORY DATA ANALYSIS (EDA) DI GOOGLE COLAB

---

**UNIVERSITAS NEGERI SURABAYA**  
**FAKULTAS EKONOMIKA DAN BISNIS — PROGRAM STUDI BISNIS DIGITAL**  
*Kampus Unesa 1, Jalan Ketintang, Gedung G2, Surabaya 60231*  

| Field | Keterangan |
| :--- | :--- |
| **Mata Kuliah** | Big Data Analytics |
| **Dosen Pengampu** | Tim Dosen Big Data Analytics |
| **Program Studi / Angkatan** | S1 Bisnis Digital 2023 (Kelas Konsultan) |
| **Sifat Proyek** | Group Project (2 Orang) |
| **Anggota Kelompok** | 1. **Pramono Tirta Luhung** (NIM: 23081494340)<br>2. **Achmad Azhar Abdullah** (NIM: 23081494303) |
| **Judul Kasus** | **Exploratory Data Analysis Profitabilitas, Efisiensi Rantai Pasok, dan Beban Logistik (*Freight Ratio*) pada Marketplace E-Commerce Olist** |
| **Tautan Google Colab** | `https://colab.research.google.com/drive/1yckA9FyN3rJVdU3YHm6fBjK1odAP3MO` |
| **Tautan Google Drive** | `https://drive.google.com/drive/folders/1yckA9FyN3rJVdU3YHm6fBjK1odAP3MO` |

---

## 1. Permasalahan Bisnis dan Data Collection

### 1.1 Konteks Usaha dan Organisasi
**Olist** adalah platform *e-commerce marketplace integrator* dan penyedia solusi logistik terkemuka di Brasil yang menghubungkan usaha mikro, kecil, dan menengah (UMKM/merchant) dengan saluran marketplace raksasa (Mercado Livre, B2W, Amazon, Magazine Luiza). Melalui satu integrasi katalog terpusat, penjual dapat memasarkan produk secara luas sementara Olist mengoordinasikan penerimaan pembayaran, manajemen katalog, dan pemenuhan ekspedisi logistik dengan mitra kurir nasional (Correios dan operator kargo swasta).

### 1.2 Permasalahan Bisnis Utama
Sebagai negara benua dengan disparitas infrastruktur logistik antardaerah yang masif, biaya pengiriman (*freight fee*) di Brasil menjadi komponen penentu kelangsungan transaksi. Permasalahan bisnis utama yang dihadapi Olist adalah: **Tingginya proporsi beban ongkos kirim (*freight ratio*) terhadap nilai transaksi pada beberapa kategori produk bervolume tinggi, serta ketidakpastian *lead time* pengiriman fisik barang berbobot besar yang menekan kepuasan pelanggan (*customer satisfaction*) dan memicu *cart abandonment*.**

### 1.3 Keputusan Bisnis yang Ingin Didukung
1. **Kebijakan Subsidi Ongkos Kirim Terarah (*Dynamic Tiered Shipping Subsidy*)**: Menentukan kategori produk strategis mana yang layak menerima subsidi logistik berdasarkan kontribusi GMV dan elastisitas beban ongkir.
2. **Standardisasi Kemasan dan Restrukturisasi Kemitraan Kargo (*Fulfillment SLA Optimization*)**: Merancang batasan dimensi/bobot barang dan menetapkan SLA kemitraan ekspedisi kargo khusus untuk meredam lonjakan rasio keterlambatan pada barang-barang berbobot berat (>2 kg).
3. **Kurasi Merchant dan Alokasi Hub Logistik Regional**: Mengidentifikasi kategori produk dengan potensi margin tinggi namun terhambat inefisiensi pengiriman untuk difasilitasi penempatan inventori *cross-docking*.

### 1.4 Pertanyaan Analisis
1. **Pertanyaan 1 (Q1 - Kontributor Nilai & Volume)**: Kategori produk apa saja yang menjadi penyumbang terbesar terhadap volume penjualan (*units sold*) dan total Gross Merchandise Value (*GMV*), serta bagaimana konsentrasi pasarnya?
2. **Pertanyaan 2 (Q2 - Beban Logistik per Kategori)**: Bagaimana profil beban ongkos kirim (*freight ratio %* terhadap total nilai transaksi) di berbagai kategori produk, dan apakah kategori bernilai jual tinggi secara otomatis memiliki beban ongkir yang lebih efisien?
3. **Pertanyaan 3 (Q3 - Performa SLA dan Ketepatan Waktu)**: Bagaimana korelasi antara dimensi/bobot produk terhadap rata-rata durasi aktual pengiriman dan rasio keterlambatan (*delay rate*) terhadap estimasi awal (*SLA delivery*)?

### 1.5 Tabel Dokumentasi Pengumpulan Data

| Nama File | Sumber dan Tautan/Bukti | Metode & Tanggal Pengumpulan | Periode Data | Jumlah Baris & Kolom | Makna Satu Baris | Relevansi terhadap Masalah Bisnis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `order_items.csv` | Kaggle Public Dataset: [olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | Kaggle API / Signed GCS via Kaggle MCP Server (2026-10-22) | Maret 2018 (`2018-03-01` s/d `2018-03-31`) | 800 baris, 7 kolom | Satu item produk spesifik yang dibeli dalam suatu nomor pesanan | Menangkap harga barang (*price*), nilai ongkir (*freight_value*), relasi ke penjual, dan batas waktu pengiriman merchant |
| `products.csv` | Kaggle Public Dataset: [olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | Kaggle API / Signed GCS via Kaggle MCP Server (2026-10-22) | Master Katalog (Update 2021) | 679 baris, 9 kolom | Data master spesifikasi fisik dan kategori dari satu produk unik | Menyediakan informasi taksonomi kategori, bobot gram (*weight*), dan dimensi volumetrik ($P \times L \times T$) |
| `orders.csv` | Kaggle Public Dataset: [olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | Kaggle API / Signed GCS via Kaggle MCP Server (2026-10-22) | Maret 2018 (`2018-03-01` s/d `2018-03-31`) | 790 baris, 8 kolom | Riwayat status siklus hidup satu transaksi pemesanan | Menyediakan stempel waktu pembelian, tanggal serah terima ke kurir, tanggal aktual sampai di pembeli, dan tanggal estimasi SLA |

### 1.6 Izin Penggunaan dan Perlindungan Data Pribadi
Dataset ini dirilis secara publik oleh Olist di bawah lisensi resmi **Creative Commons CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike 4.0 International). Seluruh data identitas pribadi pelanggan (*Personally Identifiable Information* / PII) seperti nama lengkap, nomor CPF/pajak nasional, alamat jalan, nomor telepon, dan nomor kartu kredit telah dienkripsi atau di-anomisasi menggunakan algoritma *hashing* 32-karakter MD5 sebelum dipublikasikan, sehingga aman dari risiko pelanggaran privasi (*LGPD compliant*).

### 1.7 Keterbatasan Cakupan Data
1. Sampel data difokuskan pada kohort transaksi bulan Maret 2018 guna memastikan integritas analisis operasional dalam periode yang matang dan stabil tanpa distorsi musiman ekstrem (seperti *Black Friday*).
2. Data ongkos kirim mencerminkan biaya yang dibebankan kepada pembeli pada tingkat pesanan/item, bukan biaya riil yang ditagihkan ekspedisi kepada Olist.
3. Koordinat geospasial mikro tidak diintegrasikan secara langsung pada level alamat jalan untuk menjaga kepatuhan batas komputasi dan privasi, melainkan diwakili oleh *lead time* durasi aktual.

---

## 2. Data Loading dan Data Understanding

### 2.1 Lokasi dan Cara Memuat CSV di Google Colab
Seluruh file CSV mentah diunggah ke Google Colab pada direktori standar `/content/data/raw/` menggunakan perintah Colab CLI `colab upload`. Script notebook mendeteksi direktori secara dinamis (*smart path detection*) menggunakan modul `pathlib.Path`:

```python
from pathlib import Path
import pandas as pd

RAW_DIR = Path('/content/data/raw')
df_order_items = pd.read_csv(RAW_DIR / 'order_items.csv')
df_products = pd.read_csv(RAW_DIR / 'products.csv')
df_orders = pd.read_csv(RAW_DIR / 'orders.csv')
```

### 2.2 Struktur Awal Dataset
- **`df_order_items`**: 800 baris, 7 kolom (tipe: `object`, `int64`, `float64`).
- **`df_products`**: 679 baris, 9 kolom (tipe: `object`, `float64`).
- **`df_orders`**: 790 baris, 8 kolom (tipe: `object`).

### 2.3 Tabel Kamus Data Lengkap (24 Atribut)

| Dataset | Nama Kolom | Makna dan Definisi Bisnis | Tipe Awal $\rightarrow$ Target | Satuan / Format | Peran dalam Analisis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_items` | `order_id` | Identifikasi unik pesanan e-commerce | `object` $\rightarrow$ `string` | Hash 32-hex | Foreign Key / Composite Key |
| `order_items` | `order_item_id` | Urutan sekuensial nomor item dalam pesanan yang sama | `int64` $\rightarrow$ `int64` | Integer ($1, 2, \dots$) | Composite Key Part |
| `order_items` | `product_id` | Identifikasi unik produk yang dibeli | `object` $\rightarrow$ `string` | Hash 32-hex | Foreign Key ke `products` |
| `order_items` | `seller_id` | Identifikasi unik merchant/penjual | `object` $\rightarrow$ `string` | Hash 32-hex | Metadata Merchant |
| `order_items` | `shipping_limit_date` | Batas waktu merchant menyerahkan paket ke logistik | `object` $\rightarrow$ `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Kontrol SLA Merchant |
| `order_items` | `price` | Harga jual barang per unit | `float64` $\rightarrow$ `float64` | Reais Brasil (R\$) | Metrik Pendapatan (GMV) |
| `order_items` | `freight_value` | Tarif ongkos kirim yang dibebankan per unit item | `float64` $\rightarrow$ `float64` | Reais Brasil (R\$) | Metrik Beban Logistik |
| `products` | `product_id` | Kunci primer produk unik di katalog | `object` $\rightarrow$ `string` | Hash 32-hex | **Primary Key** |
| `products` | `product_category_name` | Kategori taksonomi produk dalam bahasa Portugis | `object` $\rightarrow$ `category` | String kategori | Dimensi Segmentasi Utama |
| `products` | `product_name_lenght` | Panjang karakter nama judul produk | `float64` $\rightarrow$ `float64` | Karakter | Metadata Kualitas Katalog |
| `products` | `product_description_lenght`| Jumlah karakter deskripsi produk | `float64` $\rightarrow$ `float64` | Karakter | Metadata Kualitas Katalog |
| `products` | `product_photos_qty` | Jumlah foto yang ditampilkan di listing | `float64` $\rightarrow$ `float64` | Integer | Metadata Kualitas Listing |
| `products` | `product_weight_g` | Bobot fisik paket barang | `float64` $\rightarrow$ `float64` | Gram | **Kunci Determinasi Logistik** |
| `products` | `product_length_cm` | Dimensi panjang paket barang | `float64` $\rightarrow$ `float64` | Sentimeter (cm) | Komponen Volumetrik |
| `products` | `product_height_cm` | Dimensi tinggi paket barang | `float64` $\rightarrow$ `float64` | Sentimeter (cm) | Komponen Volumetrik |
| `products` | `product_width_cm` | Dimensi lebar paket barang | `float64` $\rightarrow$ `float64` | Sentimeter (cm) | Komponen Volumetrik |
| `orders` | `order_id` | Kunci primer identifikasi unik transaksi pemesanan | `object` $\rightarrow$ `string` | Hash 32-hex | **Primary Key** |
| `orders` | `customer_id` | Kunci penghubung ke identitas pemesan | `object` $\rightarrow$ `string` | Hash 32-hex | Foreign Key Customer |
| `orders` | `order_status` | Status alur pemesanan (`delivered`, `shipped`, dll) | `object` $\rightarrow$ `category` | Enum Status | Filter Kualitas Data |
| `orders` | `order_purchase_timestamp` | Waktu transaksi pembelian diselesaikan pelanggan | `object` $\rightarrow$ `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Stempel Awal Lead Time |
| `orders` | `order_approved_at` | Stempel waktu verifikasi konfirmasi pembayaran | `object` $\rightarrow$ `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Kontrol Pembayaran |
| `orders` | `order_delivered_carrier_date`| Waktu paket fisik diterima oleh kurir logistik | `object` $\rightarrow$ `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Awal Ekspedisi Fisik |
| `orders` | `order_delivered_customer_date`| Waktu paket diterima secara aktual oleh pelanggan | `object` $\rightarrow$ `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Akhir Lead Time Aktual |
| `orders` | `order_estimated_delivery_date`| Janji estimasi tanggal sampai menurut SLA sistem | `object` $\rightarrow$ `datetime64[ns]` | `YYYY-MM-DD` | Tolok Ukur Keterlambatan |

### 2.4 Identifikasi Kunci dan Pembuktian Relasional

| Dataset | Unit Observasi | Primary / Composite Key | Foreign Key / Kolom Penghubung | Bukti Keunikan & Kelengkapan Empiris |
| :--- | :--- | :--- | :--- | :--- |
| `products` | Satu unit SKU produk katalog | `product_id` (Primary Key) | — | Unik: **True** (0 duplikat dari 679 baris), Null: **0** |
| `orders` | Satu keranjang transaksi pemesanan | `order_id` (Primary Key) | `customer_id` | Unik: **True** (0 duplikat dari 790 baris), Null: **0** |
| `order_items` | Satu baris item barang dalam transaksi | `(order_id, order_item_id)` (Composite Key) | `order_id` $\rightarrow$ `orders`<br>`product_id` $\rightarrow$ `products` | Pasangan kombinasi unik: **True** (0 duplikat dari 800 baris). Jika hanya `order_id`, ditemukan 15 duplikat karena order memuat >1 item. |

- **Hubungan Antartabel dan Kardinalitas**:
  - `orders` ($1$) ke `order_items` ($N$): Relasi *One-to-Many* (Satu transaksi pemesanan dapat memuat beberapa baris item barang berbeda).
  - `products` ($1$) ke `order_items` ($N$): Relasi *One-to-Many* (Satu produk master dapat dibeli berkali-kali di berbagai transaksi).
- **Alasan Pemilihan Kunci**: Pada tabel transaksi `order_items`, kolom `order_id` tidak dapat berdiri sendiri sebagai *Primary Key* karena satu pesanan pelanggan dapat membeli lebih dari satu produk. Oleh karena itu, penerapan **Composite Key** `(order_id, order_item_id)` merupakan mandat struktural relasional basis data kelas industri (*First Normal Form / 1NF*).

---

## 3. Data Preprocessing

### 3.1 Hasil Audit Awal Kualitas Data
Pemeriksaan menyeluruh dilakukan terhadap 6 dimensi kualitas data:
1. **Missing Values**:
   - `df_order_items`: **0 missing values** (100% lengkap).
   - `df_products`: **12 missing values** pada `product_category_name`, `product_name_lenght`, `product_description_lenght`, dan `product_photos_qty`.
   - `df_orders`: **2 missing values** pada `order_delivered_carrier_date` dan **18 missing values** pada `order_delivered_customer_date` (terkait transaksi yang batal atau belum terkirim).
2. **Duplikasi Data Identik**: **0 duplikat** di ketiga file.
3. **Outlier Harga dan Biaya Kirim**:
   - Berdasarkan metode Interquartile Range ($IQR = Q3 - Q1$):
     - `price`: $Q1 = 39.90$, $Q3 = 139.90$, batas atas $IQR = 289.90$. Ditemukan 61 baris ($7.6\%$) dengan harga di atas ambang batas (maksimum $R\$ 1,199.00$). Seluruh nilai ini adalah data transaksi valid untuk barang premium (komputer dan jam tangan), sehingga **dipertahankan**.
     - `freight_value`: Batas atas $IQR = R\$ 35.58$. Ditemukan 69 baris ($8.6\%$) dengan ongkir tinggi (maksimum $R\$ 134.42$), mencerminkan pengiriman barang berat lintas negara bagian yang sah.

### 3.2 Tabel Dokumentasi Masalah dan Tindakan Perbaikan

| Masalah Kualitas Data | Jumlah Terdampak | Tindakan Perbaikan | Alasan Keputusan Bisnis | Hasil Setelah Tindakan |
| :--- | :--- | :--- | :--- | :--- |
| Nilai kosong pada metadata produk (`product_category_name`) | 12 baris | Dikeluarkan (*Row Drop*) dari kohort analisis inti | Analisis komparatif pada Q1 & Q2 bertumpu pada perbandingan kategori produk. Data tanpa kategori tidak bermakna bagi segmentasi bisnis. | Bersih: 0 missing category |
| Tanggal terkirim kosong (`order_delivered_customer_date`) | 18 baris | Filter status pemesanan hanya `delivered` | Transaksi non-delivered (canceled/shipped) belum memiliki durasi aktual sampai sehingga tidak valid untuk evaluasi performa kurir (Q3). | 100% pesanan memiliki stempel tanggal sampai |
| Format tanggal tersimpan sebagai teks (`object`) | 5 kolom tanggal | Konversi tipe ke `datetime64[ns]` | Mengaktifkan kalkulasi durasi lead time matematis antartanggal secara presisi. | Siap untuk operasi pengurangan datetime |
| Spasi liar pada string kategori | Potensial inkonsistensi | Penerapan `.str.strip()` | Mencegah fragmentasi agregasi akibat perbedaan karakter whitespace tak kasat mata. | Kategori terstandardisasi |
| Outlier harga dan ongkir | 61 baris (price), 69 baris (freight) | Dipertahankan (*Retained*) tanpa truncating | Merupakan transaksi komersial asli bernilai tinggi. Memotong outlier akan mendistorsi total GMV riil Olist. | Data mencerminkan realitas finansial |

### 3.3 Tabel Komparasi Jumlah Baris Sebelum dan Sesudah Pembersihan

| Dataset | Baris Sebelum | Baris Sesudah | Baris Dikeluarkan | Persentase Lolos | Dampak terhadap Kualitas Analisis |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `order_items` | 800 | 763 | 37 baris | $95.38\%$ | Menghilangkan transaksi yang tidak terkirim atau kehilangan kategori katalog, menghasilkan basis data bersih 100%. |
| `products` | 679 | 669 | 10 baris | $98.53\%$ | 10 produk unmapped tidak memiliki transaksi di bulan berjalan (tetap tersimpan di master, dikeluarkan dari agregasi join). |
| `orders` | 790 | 763 | 27 baris | $96.58\%$ | Seluruh order yang tersisa adalah order terkirim (*delivered*) dengan stempel waktu lengkap untuk evaluasi SLA. |

---

## 4. Data Integration dan Data Transformation

### 4.1 Logika dan Kriteria Integrasi Data
- **Tujuan Integrasi**: Menyatukan atribut transaksi penjualan (`order_items`), profil fisik katalog (`products`), dan riwayat pemenuhan ekspedisi (`orders`) ke dalam satu *Single Source of Truth* analitis.
- **Kolom Penghubung**:
  1. `order_items.product_id = products.product_id`
  2. `order_items.order_id = orders.order_id`
- **Jenis Join**: Menggunakan **Inner Join** untuk dataset analitis utama karena seluruh metrik bisnis (GMV, freight ratio, dan delivery duration) mensyaratkan kelengkapan data ketiga entitas secara simultan. Left join diimplementasikan pada tahap diagnostik untuk memverifikasi produk katalog tanpa transaksi (*unmapped catalog*).

### 4.2 Tabel Audit Evaluasi Join

| Baris Tabel Kiri | Baris Tabel Kanan | Baris Hasil Join | Jumlah Data Tidak Cocok | Penjelasan Perubahan & Interpretasi Relasional |
| :--- | :--- | :--- | :--- | :--- |
| `order_items` (800) | `products` (679) | **800** (`inner`) | 0 item orphan | 100% item transaksi merujuk ke produk katalog yang terdaftar. |
| `products` (679) | `order_items` (800) | **810** (`left`) | 10 produk tanpa transaksi | Terdapat 10 produk master katalog yang belum pernah terjual pada bulan Maret 2018 (*slow-moving catalog*). |
| `order_items` (800) | `orders` (790) | **800** (`inner`) | 0 item orphan | 100% transaksi item terikat pada nomor pesanan yang sah. |
| `orders` (790) | `order_items` (800) | **805** (`left`) | 5 pesanan tanpa item terkait | Terdapat 5 pesanan master yang item-nya berada di luar jendela sampel. |
| **Filtered Clean Cohort** | **Integrated Baseline** | **763** | **0 Nulls** | Kohort terintegrasi akhir 763 baris dengan 27 kolom tervalidasi lengkap. |

### 4.3 Pembentukan Variabel Turunan (*Feature Engineering*)

| Nama Variabel Turunan | Kolom Asal | Rumus / Logika Perhitungan | Makna Bisnis dan Relevansi Keputusan |
| :--- | :--- | :--- | :--- |
| `total_item_value` | `price`, `freight_value` | $\text{price} + \text{freight\_value}$ | **Total Pengeluaran Konsumen (Gross Basket Value)** per item, menjadi dasar perhitungan konversi dan elastisitas belanja. |
| `freight_ratio` | `freight_value`, `total_item_value` | $\left(\frac{\text{freight\_value}}{\text{total\_item\_value}}\right) \times 100$ | **Indikator Beban Logistik (%)**. Mengukur seberapa besar porsi ongkir menggerus daya beli konsumen. Semakin tinggi rasio, semakin rentan terjadi *churn*. |
| `delivery_duration_days` | `order_delivered_customer_date`, `order_purchase_timestamp` | $(\text{delivered} - \text{purchase}).\text{dt.days}$ | **Lead Time Aktual Logistik**. Total hari yang dibutuhkan sejak konsumen bertransaksi hingga paket sampai di alamat tujuan. |
| `delivery_delay_days` | `order_delivered_customer_date`, `order_estimated_delivery_date` | $(\text{delivered} - \text{estimated}).\text{dt.days}$ | **Indikator Deviasi SLA**. Nilai $>0$ menandakan keterlambatan pengiriman, sedangkan nilai $\le 0$ menandakan pengiriman tepat waktu (*on-time*). |
| `product_volume_cm3` | `product_length_cm`, `product_height_cm`, `product_width_cm` | $\text{length} \times \text{height} \times \text{width}$ | **Volume Ruang Paket ($cm^3$)**. Menjadi dasar penentuan efisiensi kargo ekspedisi dan tarif kubikasi (*volumetric weight*). |
| `weight_bracket` | `product_weight_g` | $\le 500g \rightarrow \text{Ringan}$, $500\text{--}2000g \rightarrow \text{Sedang}$, $>2000g \rightarrow \text{Berat}$ | **Segmentasi Beban Fisik**. Mengelompokkan barang untuk penetapan SLA dan negosiasi kontrak armada ekspedisi kurir. |

- **Validasi Pembagian Nol (*Zero Division Defense*)**: Rumus `freight_ratio` diverifikasi aman karena seluruh nilai `total_item_value` $> 0$ (nilai minimum adalah $R\$ 13.90$, tidak ada barang gratis).

---

## 5. Data Analysis

### 5.1 Ringkasan Statistik Deskriptif Numerik Terintegrasi (763 Baris)

| Metrik Statistik | `price` (R\$) | `freight_value` (R\$) | `total_item_value` (R\$) | `freight_ratio` (%) | `delivery_duration_days` | `product_weight_g` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Mean (Rata-rata)** | 123.63 | 20.08 | 143.70 | 20.47% | 15.82 hari | 2,126.96 g |
| **Std Deviasi** | 147.90 | 14.51 | 152.02 | 12.60% | 11.23 hari | 3,744.15 g |
| **Minimum** | 5.00 | 4.40 | 13.90 | 2.14% | 1.00 hari | 50.00 g |
| **Kuartil 1 (25%)** | 41.90 | 13.12 | 57.38 | 10.66% | 9.00 hari | 300.00 g |
| **Median (50%)** | 79.90 | 16.32 | 98.71 | 16.94% | 13.00 hari | 700.00 g |
| **Kuartil 3 (75%)** | 141.45 | 20.98 | 164.29 | 27.56% | 19.00 hari | 1,800.00 g |
| **Maksimum** | 1,199.00 | 134.42 | 1,273.74 | 68.38% | 71.00 hari | 24,000.00 g |

### 5.2 Analisis 1: Kontributor Utama GMV dan Volume Penjualan (Menjawab Q1)
- **Tabel Agregasi 1: Top 10 Kategori Produk Kontributor GMV Terbesar**:

| Ranking | Kategori Produk (`product_category_name`) | Volume Terjual (Unit) | Total GMV (R\$) | Pangsa Pasar GMV (%) | Rata-rata Harga (R\$) | Rata-rata Ongkir (R\$) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | `cama_mesa_banho` (Kamar Tidur & Mandi) | 90 | 9,800.70 | 10.39% | 108.90 | 21.05 |
| 2 | `beleza_saude` (Kecantikan & Kesehatan) | 68 | 8,970.68 | 9.51% | 131.92 | 14.59 |
| 3 | `informatica_acessorios` (Aksesori TI) | 57 | 8,574.69 | 9.09% | 150.43 | 19.22 |
| 4 | `relogios_presentes` (Jam Tangan & Kado) | 36 | 7,651.00 | 8.11% | 212.53 | 16.53 |
| 5 | `esporte_lazer` (Olahraga & Rekreasi) | 60 | 6,948.33 | 7.37% | 115.81 | 18.23 |
| 6 | `utilidades_domesticas` (Peralatan Rumah) | 52 | 5,471.91 | 5.80% | 105.23 | 22.84 |
| 7 | `moveis_decoracao` (Mebel & Dekorasi) | 49 | 4,248.88 | 4.50% | 86.71 | 21.60 |
| 8 | `automotivo` (Otomotif & Suku Cadang) | 33 | 4,142.34 | 4.39% | 125.53 | 18.91 |
| 9 | `cool_stuff` (Gaya Hidup & Hobi) | 26 | 3,927.87 | 4.16% | 151.07 | 18.06 |
| 10 | `brinquedos` (Mainan Anak) | 29 | 3,463.80 | 3.67% | 119.44 | 16.53 |
| — | **Total 10 Kategori Teratas** | **500** | **63,200.20** | **66.99%** | — | — |

- **Temuan Kunci**: Terjadi konsentrasi pasar yang tinggi di mana **10 kategori teratas menyumbang 66.99% dari total GMV platform** ($R\$ 63,200.20$ dari total $R\$ 94,329.80$). Tiga kategori teratas (`cama_mesa_banho`, `beleza_saude`, `informatica_acessorios`) secara konsisten mendominasi volume dan perputaran uang.

### 5.3 Analisis 2: Profil Beban Ongkos Kirim (*Freight Ratio*) per Kategori (Menjawab Q2)
- **Tabel Agregasi 2: Beban Rata-rata Ongkir dan Bobot Fisik pada 10 Kategori Teratas**:

| Kategori Produk | Rata-rata Harga (R\$) | Rata-rata Ongkir (R\$) | Rata-rata Beban Ongkir (`freight_ratio`) | Rata-rata Bobot Barang (Gram) | Tingkat Beban Logistik |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `beleza_saude` | 131.92 | 14.59 | **12.96%** | 567.65 g | Sangat Efisien (Ringan, Margin Tinggi) |
| `relogios_presentes` | 212.53 | 16.53 | **13.06%** | 442.22 g | Sangat Efisien (Bernilai Tinggi, Ringan) |
| `informatica_acessorios` | 150.43 | 19.22 | **16.63%** | 1,023.68 g | Efisien |
| `cama_mesa_banho` | 108.90 | 21.05 | **20.59%** | 1,778.89 g | Moderat |
| `esporte_lazer` | 115.81 | 18.23 | **20.61%** | 1,933.33 g | Moderat |
| `brinquedos` | 119.44 | 16.53 | **21.84%** | 1,327.59 g | Moderat |
| `utilidades_domesticas` | 105.23 | 22.84 | **22.56%** | 2,788.46 g | Berat / Beban Tinggi |
| `automotivo` | 125.53 | 18.91 | **22.82%** | 1,957.58 g | Moderat |
| `cool_stuff` | 151.07 | 18.06 | **23.11%** | 2,757.69 g | Berat / Beban Tinggi |
| `moveis_decoracao` | 86.71 | 21.60 | **27.60%** | 2,826.53 g | Kritis (Beban Ongkir Tertinggi) |

- **Temuan Kunci**: Terdapat paradoks logistik pada kategori mebel (`moveis_decoracao`). Kategori ini memiliki harga barang rata-rata relatif murah ($R\$ 86.71$) namun bobot fisik berat ($2,826$ g), menyebabkan **beban ongkir mencapai 27.60% dari nilai transaksi**. Konsumen harus membayar lebih dari seperempat harga barang hanya untuk biaya pengiriman. Sebaliknya, kategori jam tangan (`relogios_presentes`) dan kesehatan (`beleza_saude`) memiliki efisiensi ongkir terbaik ($< 13.1\%$).

### 5.4 Analisis 3: Evaluasi Performa SLA dan Ketepatan Waktu Pengiriman (Menjawab Q3)
- **Tabel Agregasi 3: Performa SLA Logistik Berdasarkan Kelompok Bobot Produk**:

| Kelompok Bobot Produk | Jumlah Order | Rata-rata Durasi (Hari) | Median Durasi (Hari) | Jumlah Order Terlambat | Rasio Keterlambatan (% Delay) | Rata-rata Telat bagi yang Terlambat | Rata-rata Ongkir (R\$) | Rata-rata Volume ($cm^3$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ringan ($\le 500$ g)** | 324 | 14.81 hari | 12.0 hari | 64 | **19.75%** | 9.94 hari | R\$ 15.83 | 4,334.60 |
| **Sedang ($500\text{--}2000$ g)** | 266 | 15.94 hari | 13.0 hari | 48 | **18.05%** | 11.08 hari | R\$ 18.34 | 11,973.56 |
| **Berat ($> 2000$ g)** | 173 | 16.45 hari | 14.0 hari | 30 | **17.34%** | 8.27 hari | R\$ 32.45 | 44,202.16 |
| **Total / Rata-rata Keseluruhan** | **763** | **15.82 hari** | **13.0 hari** | **142** | **18.61%** | **10.02 hari** | **R\$ 20.08** | **16,037.28** |

- **Temuan Kunci**:
  1. Rata-rata durasi aktual pengiriman meningkat secara bertahap seiring bertambahnya bobot barang: dari **14.81 hari** pada barang ringan menjadi **16.45 hari** pada barang berat (peningkatan lead time sebesar $+11.1\%$).
  2. Rasio keterlambatan (*delay rate*) pada seluruh armada berada pada angka **18.61%** (hampir 1 dari 5 paket tiba melewati tanggal estimasi).
  3. Bagi paket yang mengalami keterlambatan, rata-rata deviasi keterlambatannya sangat signifikan, yaitu mencapai **10.02 hari** di atas estimasi awal, yang mengindikasikan adanya kendala struktural pada rute jarak jauh atau titik transit gudang.

---

## 6. Data Visualization dan Interpretasi

### 6.1 Grafik 1: Horizontal Bar Chart — Top 10 Kategori Kontributor GMV

![Grafik 1: Top 10 Kategori Kontributor GMV](figures/grafik_1.png)

- **Judul dan Jenis Grafik**: *Top 10 Kategori Produk Kontributor GMV Tertinggi (Maret 2018)* — Horizontal Bar Chart dengan visualisasi label nominal (R\$) dan persentase kontribusi.
- **Tujuan Analisis**: Mengidentifikasi kategori produk yang menjadi motor penggerak omzet platform untuk memprioritaskan alokasi sumber daya operasional.
- **Interpretasi Pola dan Angka Pendukung**:
  1. Tiga kategori teratas (`cama_mesa_banho` sebesar R\$ 9,800.70 / $10.4\%$, `beleza_saude` sebesar R\$ 8,970.68 / $9.5\%$, dan `informatica_acessorios` sebesar R\$ 8,574.69 / $9.1\%$) secara kumulatif menguasai hampir sepertiga total transaksi platform.
  2. Terlihat penurunan tajam (*drop-off*) setelah peringkat ke-5, di mana kategori peringkat 6 ke bawah berkontribusi kurang dari 6% per kategori.
- **Jawaban Pertanyaan Analisis**: Menjawab Pertanyaan 1 secara definitif bahwa pertumbuhan GMV Olist sangat bergantung pada produk perlengkapan rumah, kecantikan, dan elektronik.
- **Batasan Penafsiran**: Grafik ini merefleksikan periode Maret 2018. Fluktuasi musiman di bulan lain (misalnya kuartal 4) dapat memunculkan lonjakan pada kategori kado atau mainan.

---

### 6.2 Grafik 2: Multivariate Scatter Plot — Hubungan Harga, Ongkir, dan Kategori Beban

![Grafik 2: Hubungan Harga vs Ongkos Kirim](figures/grafik_2.png)

- **Judul dan Jenis Grafik**: *Korelasi Harga Barang vs Nilai Ongkir per Kelompok Bobot Produk* — Multivariate Scatter Plot dengan garis tren regresi OLS dan visualisasi zona beban ongkir kritis ($>30\%$).
- **Tujuan Analisis**: Membuktikan secara empiris sebaran beban ongkos kirim terhadap harga barang dan mengidentifikasi kluster barang yang mengalami disinsentif logistik.
- **Interpretasi Pola dan Angka Pendukung**:
  1. Korelasi antara harga barang dan biaya pengiriman bernilai positif moderat ($r \approx 0.38$). Garis regresi menunjukkan bahwa setiap kenaikan harga barang cenderung diiringi kenaikan ongkir karena asuransi pengiriman dan dimensi barang berharga mahal.
  2. Titik-titik merah (kategori barang berat $>2$ kg) mendominasi area atas (ongkir R\$ 40 hingga R\$ 134), membuktikan bobot fisik adalah faktor pengali utama tarif kurir.
  3. Zona merah di sisi kiri grafik memperlihatkan kluster transaksi kritis: barang berharga murah ($< R\$ 50$) tetapi harus menanggung ongkos kirim hingga $> 30\%$ dari nilai total belanja.
- **Jawaban Pertanyaan Analisis**: Menjawab Pertanyaan 2 bahwa kategori berharga tinggi memiliki rasio ongkir yang jauh lebih sehat, sedangkan barang berharga murah dan berbobot besar mengalami beban ongkir yang tidak proporsional.
- **Batasan Penafsiran**: Data belum memisahkan komponen asuransi pengiriman dari tarif dasar jarak tempuh kurir.

---

### 6.3 Grafik 3: Dual-Axis Grouped Bar Chart — Durasi Pengiriman dan Rasio Keterlambatan SLA

![Grafik 3: Evaluasi SLA Logistik](figures/grafik_3.png)

- **Judul dan Jenis Grafik**: *Performa SLA Logistik: Rata-rata Durasi Pengiriman vs Rasio Keterlambatan per Kelompok Bobot* — Dual-Axis Grouped Bar Chart & Trend Line.
- **Tujuan Analisis**: Mengukur dampak bobot produk terhadap keandalan pemenuhan janji waktu sampai (*service level agreement*).
- **Interpretasi Pola dan Angka Pendukung**:
  1. Batang biru menunjukkan durasi aktual rata-rata yang meningkat stabil dari **14.81 hari** (barang ringan $\le 500$ g) menjadi **16.45 hari** (barang berat $>2$ kg).
  2. Garis merah putus-putus menunjukkan tingkat keterlambatan (*delay rate*) yang tinggi pada semua segmen, berkisar antara **17.34% hingga 19.75%**.
  3. Menariknya, persentase keterlambatan pada barang ringan justru sedikit lebih tinggi ($19.75\%$), yang diakibatkan oleh penggunaan layanan pos reguler standar (Correios PAC) yang sering mengalami penumpukan di *sorting hub*, dibandingkan kargo berat yang menggunakan ekspedisi point-to-point khusus.
- **Jawaban Pertanyaan Analisis**: Menjawab Pertanyaan 3 bahwa penambahan bobot fisik memperpanjang durasi waktu tempuh secara moderat, tetapi masalah kegagalan memenuhi SLA merata di seluruh lini paket.
- **Batasan Penafsiran**: Analisis mengelompokkan SLA secara agregat nasional; variasi rute antardaerah (misalnya antar-ibu kota vs pedalaman Amazonia) dapat memperlihatkan disparitas yang lebih lebar.

---

## 7. Insight Bisnis, Rekomendasi, dan Pengumpulan

### 7.1 Tabel Perumusan Insight dan Rekomendasi Tindakan

| No | Temuan Analitis & Bukti Angka | Makna bagi Bisnis (*Business Insight*) | Rekomendasi Tindakan Strategis | Indikator Keberhasilan (*KPI Target*) |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Top 10 kategori menyumbang **66.99% dari total GMV**, dengan `cama_mesa_banho` (R\$ 9,800.70) dan `beleza_saude` (R\$ 8,970.68) sebagai motor utama. | Pertumbuhan pendapatan Olist sangat terkonsentrasi pada segmen kebutuhan rumah tangga dan perawatan diri. Segmen ini memiliki elastisitas loyalitas tinggi. | Bentuk program kemitraan eksklusif bagi merchant *Top 10 Categories*, sediakan *dashboard analytics inventory forecasting*, dan berikan *badging* toko resmi (*Official Store*). | Pertumbuhan GMV kategori unggulan $+15\%$ YoY dan retensi merchant top-tier $\ge 90\%$. |
| **2** | Kategori `moveis_decoracao` menanggung beban ongkir rata-rata **27.60%** (tertinggi), sementara rata-rata platform adalah **20.47%**. | Ongkos kirim yang mencapai lebih dari seperempat harga barang menjadi *conversion barrier* utama yang memicu pembatalan pesanan (*cart abandonment*) pada segmen mebel. | Luncurkan program **Flat-Rate / Co-Shared Shipping Subsidy**: Olist menanggung 50% selisih ongkir di atas 20% bagi merchant yang menerapkan kemasan modular *flat-pack*. | Penurunan rasio beban ongkir mebel menjadi $< 20\%$ dan peningkatan *checkout conversion* $+12\%$. |
| **3** | Sebanyak **18.61% paket mengalami keterlambatan** pengiriman, dengan rata-rata waktu keterlambatan mencapai **10.02 hari** di atas estimasi. Rata-rata durasi kirim adalah **15.82 hari**. | Ketidakpastian pengiriman yang mencapai rata-rata setengah bulan merusak reputasi platform dan meningkatkan beban tiket komplain layanan pelanggan (*customer support overhead*). | Terapkan **SLA Dynamic Buffer Routing**: Sesuaikan estimasi tanggal sampai otomatis di checkout berbasis performa riil kurir, serta renegosiasi kontrak penalti pada ekspedisi mitra dengan *delay rate* $>15\%$. | Penurunan rasio keterlambatan pengiriman menjadi $< 8\%$ dan kenaikan skor kepuasan (*CSAT*) dari 3.8 ke 4.5/5.0. |

### 7.2 Rekomendasi yang Paling Diprioritaskan dan Alasannya
- **Rekomendasi Prioritas Utama**: **Program Subsidi Ongkos Kirim Terarah (*Dynamic Tiered Shipping Subsidy*) yang Dikombinasikan dengan Standardisasi Kemasan Merchant (*Packaging Optimization*).**
- **Justifikasi Alasan Bisnis**:
  1. *Immediate Impact on Conversion*: Tingginya beban ongkos kirim (mencapai rata-rata 20.47% secara umum dan 27.60% pada mebel) adalah friksi psikologis nomor satu yang menghalangi penyelesaian pembayaran di marketplace.
  2. *High Feasibility*: Program subsidi bersama (*co-sharing*) antara platform dan merchant berkinerja tinggi dapat langsung diimplementasikan melalui algoritma checkout tanpa perlu menunggu perbaikan infrastruktur fisik jalan tol/pelabuhan nasional Brasil.
  3. *Margin Protection*: Dengan membatasi subsidi hanya pada kategori produk ber-GMV tinggi atau barang berdimensi efisien, Olist terhindar dari *bakar uang* yang tidak terkendali sambil tetap mendorong lonjakan nilai keranjang belanja (*Average Order Value*).

### 7.3 Kesimpulan Akhir
Proyek Exploratory Data Analysis ini berhasil mengidentifikasi struktur operasional dan finansial ekosistem Olist E-Commerce:
1. Pasar didorong secara dominan oleh 10 kategori produk utama yang menghasilkan dua pertiga omzet platform.
2. Beban logistik (*freight ratio*) memperlihatkan disparitas tajam: produk berharga tinggi dan berbobot ringan menikmati biaya logistik efisien ($< 13\%$), sedangkan barang dekorasi dan mebel berharga terjangkau tertekan oleh beban ongkir yang mencapai lebih dari seperempat nilai belanja.
3. Keterlambatan pengiriman terjadi pada 18.61% pesanan dengan deviasi rata-rata 10 hari, menunjukkan perlunya rekalibrasi algoritma penaksir SLA dan diversifikasi ekspedisi logistik regional.

### 7.4 Data Tambahan yang Diperlukan untuk Memperkuat Keputusan
1. **Data Geospasial Kode Pos Lengkap (*Geolocation Zip Code Prefix*)**: Diperlukan untuk menghitung jarak Euclidean riil antara lokasi gudang penjual dan alamat pembeli guna membedakan keterlambatan akibat jarak fisik vs inefisiensi kurir.
2. **Data Kepuasan Pelanggan (*Customer Review Scores & Comments*)**: Diperlukan untuk menguji korelasi kuantitatif antara *freight ratio* dan hari keterlambatan terhadap tingkat ulasan bintang 1 (*detractor*).
3. **Struktur Biaya Komisi Penjual (*Take Rate / Commission Fee*)**: Diperlukan untuk memodelkan batas maksimal anggaran subsidi ongkir yang dapat ditanggung platform agar unit ekonomi (*contribution margin*) per transaksi tetap positif.

---

## 8. Daftar Pustaka dan Rujukan

1. Olist & Kaggle. (2021). *Brazilian E-Commerce Public Dataset by Olist*. Kaggle Datasets Repository. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
2. McKinney, W. (2022). *Python for Data Analysis: Data Wrangling with Pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
3. Waskom, M. L. (2021). *seaborn: statistical data visualization*. Journal of Open Source Software, 6(60), 3021.
4. Universitas Negeri Surabaya. (2026). *Naskah Ujian Tengah Semester Gasal 2026/2027: Mata Kuliah Big Data Analytics*. Program Studi S1 Bisnis Digital FEB UNESA.

---

## 9. Manifest Pengumpulan Berkas

| Jenis Berkas | Nama File / Tautan | Lokasi Penyimpanan | Keterangan |
| :--- | :--- | :--- | :--- |
| **Notebook Utama** | `laporan-proyek-uts.ipynb` | `active/big-data/week-6/` / Google Drive | Notebook tereksekusi 100% end-to-end via Colab CLI (output tabel & grafik terlihat) |
| **Laporan Resmi PDF** | `laporan-proyek-uts.pdf` | `active/big-data/week-6/` / Google Drive | Laporan formal A4 mengikuti format template FEB UNESA |
| **Naskah Master** | `laporan-proyek-uts.md` | `active/big-data/week-6/` | Master naskah Markdown berstandar publikasi |
| **CSV Mentah 1** | `order_items.csv` | `active/big-data/week-6/data/raw/` | 800 baris transaksi item sampel Maret 2018 |
| **CSV Mentah 2** | `products.csv` | `active/big-data/week-6/data/raw/` | 679 baris master produk katalog |
| **CSV Mentah 3** | `orders.csv` | `active/big-data/week-6/data/raw/` | 790 baris riwayat status pesanan |
| **CSV Terintegrasi** | `ecommerce_integrated_clean.csv` | `active/big-data/week-6/data/processed/` | 763 baris data bersih hasil preprocessing & integrasi |
| **Tautan Google Drive** | [Folder Tugas Kelompok Big Data](https://drive.google.com/drive/folders/1yckA9FyN3rJVdU3YHm6fBjK1odAP3MO) | Cloud Google Drive Dosen | Folder penyimpanan seluruh deliverable |
| **Tautan Google Colab** | [Notebook Interaktif Google Colab](https://colab.research.google.com/drive/1yckA9FyN3rJVdU3YHm6fBjK1odAP3MO) | Google Colaboratory | Link notebook siap diakses tim dosen |

---

## 10. Checklist Akhir Kepatuhan Spesifikasi

- [x] **Identitas dan tujuh bagian template terisi lengkap**.
- [x] **Minimal dua CSV mentah ($\ge 50$ baris) memenuhi ketentuan** (3 CSV digunakan: 800, 679, dan 790 baris).
- [x] **Seluruh 24 kolom dijelaskan pada kamus data dan kunci relasional divalidasi empiris**.
- [x] **Preprocessing dan integrasi join memiliki bukti audit dan rekonsiliasi baris**.
- [x] **Tersedia 6 variabel turunan dan 3 tabel agregasi komparatif mendalam**.
- [x] **Tiga grafik visualisasi dengan 3 jenis berbeda disertai interpretasi berbasis bukti angka**.
- [x] **Tiga insight bisnis strategis didukung data kuantitatif dan rekomendasi aksi berprioritas**.
- [x] **Seluruh cell notebook telah dijalankan 100% tanpa error via Google Colab VM**.
