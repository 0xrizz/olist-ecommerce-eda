<div class="cover-header">
  <img src="figures/unesa-logo.png" class="cover-logo-unesa" alt="Logo UNESA" />
  <div class="cover-inst-title">UNIVERSITAS NEGERI SURABAYA<br>FAKULTAS EKONOMIKA DAN BISNIS<br>PROGRAM STUDI S1 BISNIS DIGITAL</div>
  <div class="cover-inst-sub">Kampus Ketintang, Gedung G2, Jalan Ketintang, Surabaya 60231</div>
</div>

<hr />

# LAPORAN PROYEK UJIAN TENGAH SEMESTER (UTS)
## BIG DATA ANALYTICS: EXPLORATORY DATA ANALYSIS DI GOOGLE COLAB

<p style="text-align: center; font-family: 'Charter', 'Merriweather', 'Georgia', serif; font-size: 13.5pt; font-weight: 700; margin: 14pt 0 16pt 0; color: #111827;">
Exploratory Data Analysis Profitabilitas, Efisiensi Rantai Pasok, dan Beban Logistik (Freight Ratio) pada Marketplace E-Commerce Olist
</p>

| Parameter Laporan | Keterangan Dokumen |
| :--- | :--- |
| **Mata Kuliah** | Big Data Analytics (3 SKS) |
| **Dosen Pengampu** | **Anita Safitri, M. Kom.** |
| **Program Studi / Angkatan** | S1 Bisnis Digital 2023 (Kelas Konsultan) |
| **Penyusun Laporan** | 1. **Pramono Tirta Luhung** (NIM: 23081494340)<br>2. **Achmad Azhar Abdullah** (NIM: 23081494303) |

<div class="cover-colab-badge">
  <a href="https://colab.research.google.com/drive/1LRu6eAmTATAlNKFARKWT47g9sb5oqIt6" target="_blank" style="text-decoration: none; color: inherit; display: inline-flex; align-items: center; justify-content: center; gap: 8px;">
    <img src="figures/colab-logo.svg" class="cover-colab-logo" alt="Google Colab" />
    <span class="cover-colab-text">Google Colaboratory Cloud Engine</span>
  </a>
</div>

<div class="cover-end"></div>

## 1. Permasalahan Bisnis dan Data Collection

### 1.1 Konteks Usaha dan Organisasi
Olist merupakan platform integrator marketplace dan penyedia infrastruktur logistik e-commerce terkemuka di Brasil. Platform ini menghubungkan pelaku usaha mikro, kecil, dan menengah (merchant) dengan saluran marketplace terintegrasi berskala nasional, seperti Mercado Livre, B2W, Amazon, dan Magazine Luiza. Melalui sistem katalog terpusat Olist, merchant dapat menjual produk secara luas tanpa mengelola integrasi teknis ke masing-masing marketplace secara terpisah, sementara Olist mengoordinasikan pemrosesan pembayaran, standardisasi kemasan, dan pemenuhan ekspedisi logistik bekerja sama dengan operator pos nasional (Correios) serta kurir kargo swasta.

### 1.2 Permasalahan Bisnis Utama
Sebagai negara dengan luas wilayah geografis mencapai 8,5 juta km persegi dan memiliki disparitas infrastruktur jalan darat antardaerah yang signifikan, biaya logistik pengiriman (*freight fee*) di Brasil menjadi komponen penentu utama daya saing harga e-commerce. Permasalahan bisnis utama yang dihadapi Olist adalah: **Tingginya beban rasio ongkos kirim (*freight ratio*) terhadap total nilai transaksi pada produk berharga murah dan berdimensi besar, serta tingginya variansi durasi pengiriman (*lead time*) yang memicu keterlambatan dari estimasi awal kurir (*SLA breach*), sehingga menurunkan kepuasan pelanggan dan meningkatkan angka pembatalan keranjang belanja (*cart abandonment*).**

### 1.3 Keputusan Bisnis yang Ingin Didukung
1. **Perancangan Kebijakan Subsidi Ongkos Kirim Dinamis (*Dynamic Tiered Freight Subsidy*)**: Menentukan kategori produk strategis mana yang paling membutuhkan intervensi subsidi ongkos kirim berbasis kontribusi GMV dan elastisitas beban logistik.
2. **Standardisasi Kemasan dan Restrukturisasi Kontrak Kurir (*Packaging Optimization & SLA Enforcement*)**: Menetapkan batasan bobot kemasan merchant serta menegosiasi ulang penalti keterlambatan pada mitra logistik yang memiliki rasio keterlambatan di atas ambang toleransi.
3. **Alokasi Hub Inventori Regional (*Fulfillment Hub Placement*)**: Mengidentifikasi kluster produk dengan volume transaksi tinggi namun terhambat inefisiensi pengiriman antar-negara bagian untuk ditempatkan pada fasilitas pergudangan transit (*cross-docking*).

### 1.4 Pertanyaan Analisis
1. **Pertanyaan Analisis 1 (Kontribusi GMV dan Volume Penjualan)**: Kategori produk apa saja yang menjadi penyumbang terbesar terhadap volume penjualan (*units sold*) dan total Gross Merchandise Value (*GMV*), serta bagaimana tingkat konsentrasi pangsa pasarnya?
2. **Pertanyaan Analisis 2 (Beban Rasio Logistik per Kategori)**: Bagaimana profil beban ongkos kirim (*freight ratio %* terhadap total nilai transaksi belanja) di berbagai kategori produk, dan apakah kategori bernilai jual tinggi secara otomatis menikmati rasio logistik yang lebih efisien?
3. **Pertanyaan Analisis 3 (Evaluasi Kepatuhan SLA Pengiriman)**: Bagaimana korelasi antara dimensi bobot fisik produk terhadap durasi aktual pengiriman dan tingkat rasio keterlambatan (*delay rate*) terhadap estimasi janji tiba kurir (*delivery SLA*)?

### 1.5 Tabel Dokumentasi Pengumpulan Data

| Nama File | Sumber dan Tautan/Bukti | Metode & Tanggal Pengumpulan | Periode Data | Jumlah Baris & Kolom | Makna Satu Baris | Relevansi terhadap Masalah Bisnis |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `order_items.csv` | Kaggle Public Dataset: [olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | Kaggle API / Signed GCS Stream (22 Oktober 2026) | Maret 2018 (`2018-03-01` s/d `2018-03-31`) | 800 baris, 7 kolom | Satu item produk spesifik yang dibeli dalam suatu nomor pesanan | Menangkap harga barang (*price*), nilai ongkir (*freight_value*), relasi ke penjual, dan batas waktu pengiriman merchant |
| `products.csv` | Kaggle Public Dataset: [olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | Kaggle API / Signed GCS Stream (22 Oktober 2026) | Master Katalog (Update 2021) | 679 baris, 9 kolom | Data master spesifikasi fisik dan taksonomi dari satu produk unik | Menyediakan informasi nama kategori, bobot gram (*weight*), dan dimensi volumetrik fisik ($P \times L \times T$) |
| `orders.csv` | Kaggle Public Dataset: [olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | Kaggle API / Signed GCS Stream (22 Oktober 2026) | Maret 2018 (`2018-03-01` s/d `2018-03-31`) | 790 baris, 8 kolom | Riwayat status siklus hidup satu transaksi pemesanan | Menyediakan stempel waktu pembelian, tanggal serah terima ke kurir, tanggal aktual sampai di pembeli, dan tanggal estimasi kurir |

### 1.6 Izin Penggunaan dan Perlindungan Data Pribadi
Dataset ini dirilis secara publik oleh Olist di platform Kaggle di bawah lisensi resmi **Creative Commons CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike 4.0 International). Seluruh data identitas pribadi pelanggan (*Personally Identifiable Information* / PII), seperti nama lengkap, nomor identitas kependudukan/pajak nasional (CPF), alamat jalan rinci, nomor telepon, dan nomor kartu kredit, telah dienkripsi menggunakan algoritma *hashing* 32-karakter MD5 sebelum dipublikasikan, sehingga aman dari risiko kebocoran data privasi serta patuh terhadap regulasi perlindungan data Brasil (*Lei Geral de Protecao de Dados* / LGPD).

### 1.7 Keterbatasan Cakupan Data
1. Sampel data difokuskan pada kohort transaksi bulan Maret 2018 untuk mengisolasi analisis pada periode operasional yang matang tanpa distorsi musiman belanja ekstrem (seperti promo *Black Friday* di bulan November).
2. Data tarif pengiriman mencerminkan biaya yang dibebankan kepada pembeli pada tingkat checkout pemesanan, bukan tarif kontrak riil yang ditagihkan ekspedisi pihak ketiga kepada Olist.
3. Analisis geospasial mikro tidak mengintegrasikan koordinat jalan raya per pelanggan guna menjaga privasi, melainkan diwakili oleh metrik durasi waktu tempuh hari kerja aktual.

---

## 2. Data Loading dan Data Understanding

### 2.1 Lokasi dan Cara Memuat CSV di Google Colab
Seluruh berkas data tabular mentah disimpan dalam direktori `data/raw/` dan dimuat ke dalam memori kerja kernel Python menggunakan modul data wrangling `pandas`. Skrip deteksi lingkungan secara otomatis mendeteksi apakah proses komputasi berlangsung di lingkungan remote Google Colab (`/content/data/raw/`) atau repositori lokal (`./data/raw/`). Tipe data tanggal pada `orders.csv` secara eksplisit diparsing menjadi format datetime standar (`parse_dates`) sejak tahap pembacaan awal.

### 2.2 Struktur Awal Dataset
1. **`df_order_items`**: Terdiri dari **800 baris dan 7 kolom**. Kolom numerik utama adalah `price` (rentang R\$ 5,30 hingga R\$ 1.199,90) dan `freight_value` (rentang R\$ 2,86 hingga R\$ 134,34).
2. **`df_products`**: Terdiri dari **679 baris dan 9 kolom**. Menyediakan 58 kategori produk unik dengan variansi bobot kemasan dari 50 gram hingga 21.800 gram. Terdapat 17 baris yang mengalami missing value pada nama kategori dan dimensi fisik.
3. **`df_orders`**: Terdiri dari **790 baris dan 8 kolom**. Menampung 763 transaksi berstatus `delivered` (selesai terkirim), 9 berstatus `shipped` (sedang dikirim kurir), 11 berstatus `canceled` (batal), dan 7 berstatus `unavailable` (barang habis).

### 2.3 Tabel Kamus Data Lengkap (24 Atribut)

| Dataset Asal | Nama Kolom | Makna Kolom | Contoh Nilai | Tipe Awal -> Target | Satuan / Format | Peran Data |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `order_items` | `order_id` | Identifikator unik pemesanan | `00010242fe8c5b16b...` | `object` -> `string` | 32-char hex | Composite Key (Part 1) / FK |
| `order_items` | `order_item_id` | Nomor urut item dalam pesanan | `1`, `2` | `int64` -> `int32` | Integer urut | Composite Key (Part 2) |
| `order_items` | `product_id` | Kunci identitas produk katalog | `4244733e06e7ecb49...` | `object` -> `string` | 32-char hex | Foreign Key ke Products |
| `order_items` | `seller_id` | Kunci identitas penjual/merchant | `48436dade18ac8b2b...` | `object` -> `string` | 32-char hex | Foreign Key ke Merchant |
| `order_items` | `shipping_limit_date` | Batas waktu merchant kirim barang | `2018-03-20 18:30:16` | `object` -> `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Fitur Temporal |
| `order_items` | `price` | Harga pokok jual barang per unit | `58.90` | `float64` -> `float64` | Brazilian Real (BRL / R\$) | Variabel Nilai Finansial |
| `order_items` | `freight_value` | Tarif ongkos kirim kurir per item | `13.29` | `float64` -> `float64` | Brazilian Real (BRL / R\$) | Variabel Beban Logistik |
| `products` | `product_id` | Identifikator unik master produk | `4244733e06e7ecb49...` | `object` -> `string` | 32-char hex | Primary Key pada Products |
| `products` | `product_category_name` | Nama kategori produk bahasa Portugis | `cool_stuff`, `telefonia` | `object` -> `category` | Teks kategori | Dimensi Segmentasi Produk |
| `products` | `product_name_lenght` | Panjang karakter judul produk | `58.0` | `float64` -> `Int32` | Jumlah karakter | Karakteristik Metadata |
| `products` | `product_description_lenght`| Panjang karakter deskripsi produk | `598.0` | `float64` -> `Int32` | Jumlah karakter | Karakteristik Metadata |
| `products` | `product_photos_qty` | Jumlah foto produk dalam listing | `4.0` | `float64` -> `Int32` | Jumlah foto | Karakteristik Visual |
| `products` | `product_weight_g` | Massa fisik kemasan barang | `650.0` | `float64` -> `float64` | Gram (g) | Determinan Fisik Logistik |
| `products` | `product_length_cm` | Panjang dimensi kemasan barang | `28.0` | `float64` -> `float64` | Sentimeter (cm) | Dimensi Volumetrik |
| `products` | `product_height_cm` | Tinggi dimensi kemasan barang | `9.0` | `float64` -> `float64` | Sentimeter (cm) | Dimensi Volumetrik |
| `products` | `product_width_cm` | Lebar dimensi kemasan barang | `14.0` | `float64` -> `float64` | Sentimeter (cm) | Dimensi Volumetrik |
| `orders` | `order_id` | Identifikator unik master transaksi | `00010242fe8c5b16b...` | `object` -> `string` | 32-char hex | Primary Key pada Orders |
| `orders` | `customer_id` | Kunci identitas pembeli pesanan | `3ce436f183e68e078...` | `object` -> `string` | 32-char hex | Foreign Key ke Customers |
| `orders` | `order_status` | Status siklus hidup transaksi | `delivered`, `shipped` | `object` -> `category` | Teks status pesanan | Filter Kelayakan Analisis |
| `orders` | `order_purchase_timestamp` | Waktu transaksi dibuat pembeli | `2018-03-13 16:06:38` | `object` -> `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Stempel Waktu Transaksi |
| `orders` | `order_approved_at` | Waktu konfirmasi pembayaran | `2018-03-13 17:29:19` | `object` -> `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Stempel Waktu Verifikasi |
| `orders` | `order_delivered_carrier_date`| Waktu serah barang ke mitra kurir | `2018-03-14 18:08:44` | `object` -> `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Stempel Waktu Logistik |
| `orders` | `order_delivered_customer_date`| Waktu fisik barang tiba di pembeli | `2018-03-19 18:47:44` | `object` -> `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Stempel Waktu Selesai (Aktual)|
| `orders` | `order_estimated_delivery_date`| Janji estimasi tiba oleh marketplace | `2018-04-03 00:00:00` | `object` -> `datetime64[ns]` | `YYYY-MM-DD HH:MM:SS` | Tolok Ukur Janji SLA |

### 2.4 Identifikasi Kunci dan Pembuktian Relasional

| Dataset | Unit Observasi | Primary / Composite Key | Foreign Key Penghubung | Bukti Empiris Keunikan dan Kardinalitas |
| :--- | :--- | :--- | :--- | :--- |
| `order_items` | Baris transaksi item produk per pesanan | **Composite Key**: `(order_id, order_item_id)` | `order_id` -> `orders`<br>`product_id` -> `products` | Duplikasi kombinasi bernilai 0 baris (100% unik pada 800 baris). Kardinalitas ke `orders` adalah Many-to-One ($N:1$). |
| `products` | Master katalog produk spesifikasi fisik | **Primary Key**: `product_id` | Tidak ada | Keunikan 100% pada 679 baris (`is_unique == True`), nilai null = 0. Berfungsi sebagai tabel dimensi master produk ($1:N$). |
| `orders` | Header status pesanan pembeli | **Primary Key**: `order_id` | `customer_id` | Keunikan 100% pada 790 baris (`is_unique == True`), nilai null = 0. Berfungsi sebagai tabel induk siklus pemesanan ($1:N$). |

Kebutuhan Composite Key pada `order_items` timbul karena satu nomor pemesanan (`order_id`) dapat memuat beberapa kuantitas produk yang sama maupun produk berbeda. Kombinasi `order_id` dan `order_item_id` menjamin identifikasi unik setiap baris pesanan fisik barang.

---

## 3. Data Preprocessing

### 3.1 Hasil Audit Awal Kualitas Data
Pemeriksaan kualitas data mencakup 6 dimensi integritas data:
1. **Missing Values**:
   - `df_order_items`: Dinyatakan 100% lengkap tanpa nilai kosong pada seluruh kolom finansial maupun kunci relasi.
   - `df_products`: Ditemukan 17 baris missing value pada `product_category_name`, `product_weight_g`, dan atribut dimensi volumetrik.
   - `df_orders`: Ditemukan nilai kosong pada transaksi yang belum tuntas dikirim (`order_delivered_customer_date` kosong pada 27 transaksi berstatus `shipped`, `canceled`, dan `unavailable`).
2. **Duplikasi Data**: Tidak ditemukan duplikasi baris identik (*exact duplicate rows*) pada ketiga tabel mentah.
3. **Pencilan (Outliers)**: Ditemukan outlier nilai harga produk hingga R\$ 1.199,90 dan bobot fisik hingga 21.800 gram (21,8 kg). Karakteristik ini dipertahankan karena merupakan pencilan alami yang mencerminkan variasi barang dagangan riil (perabot rumah tangga dan mesin perkakas), bukan kesalahan input data.

### 3.2 Tabel Dokumentasi Masalah dan Tindakan Perbaikan

| Masalah Kualitas Data | Jumlah Terdampak | Tindakan Perbaikan | Alasan Rasional | Hasil Setelah Tindakan |
| :--- | :---: | :--- | :--- | :--- |
| Nilai kosong kategori & bobot produk pada `products` | 17 baris | Filter eliminasi baris (*listwise deletion*) | Kategori produk dan bobot fisik adalah variabel wajib dalam analisis beban logistik | 662 baris produk valid siap diintegrasikan |
| Pesanan belum selesai terkirim pada `orders` | 27 baris | Filter status pesanan hanya untuk transaksi `delivered` | Menghitung durasi aktual pengiriman dan rasio keterlambatan membutuhkan tanggal tiba fisik barang yang riil | 763 transaksi selesai terkirim tervalidasi |
| Inkonsistensi tipe data datetime pada `orders` | 5 kolom tanggal | Konversi tipe data eksplisit ke `datetime64[ns]` | Memungkinkan operasi aritmatika selisih waktu secara vektor untuk menghitung durasi kirim | Format waktu terstandarisasi ISO 8601 |
| Inkonsistensi integer pada kolom jumlah foto & deskripsi | 3 kolom | Konversi tipe nullable integer (`Int32`) | Standarisasi representasi diskrit tanpa distorsi representasi desimal mengambang | Tipe data integer terformat bersih |

### 3.3 Urutan Pembersihan dan Rasionalisasi Metodologis
Urutan pembersihan dilakukan dari tabel dimensi master terlebih dahulu (`products` dan `orders`) sebelum dilakukan integrasi relasional ke tabel fakta transaksi (`order_items`). Pendekatan ini mencegah propagasi nilai null atau baris transaksi tidak valid ke dalam dataset analitis akhir.

### 3.4 Penanganan Nilai Ekstrem (Outlier)
Pencilan pada nilai harga barang dan bobot kemasan diisolasi menggunakan metode segmentasi kategorikal (*binning*), bukan dengan cara memotong atau menghapus baris transaksi (*trimming*). Peneliti mengelompokkan produk menjadi 3 kategori bobot operasional logistik:
- **Ringan**: $\le 500$ gram
- **Sedang**: $501$ gram hingga $2.000$ gram ($2$ kg)
- **Berat**: $> 2.000$ gram ($> 2$ kg)

Pendekatan segmentasi ini melindungi integritas data finansial GMV secara penuh sekaligus memberikan batas perbandingan performa kurir yang realistis di setiap kategori bobot.

### 3.5 Tabel Rekonsiliasi Jumlah Baris Sebelum dan Sesudah

| Dataset | Baris Sebelum | Baris Sesudah | Baris Dikeluarkan | Dampak Metodologis terhadap Analisis |
| :--- | :---: | :---: | :---: | :--- |
| `order_items.csv` | 800 | 763 | 37 | Menghilangkan transaksi yang tidak memiliki data produk lengkap atau status pesanan belum selesai terkirim |
| `products.csv` | 679 | 662 | 17 | Memastikan seluruh produk memiliki taksonomi kategori dan nilai bobot gram yang valid |
| `orders.csv` | 790 | 763 | 27 | Mengisolasi transaksi yang telah tuntas diterima pelanggan untuk perhitungan durasi SLA riil |
| **Dataset Bersih Terintegrasi** | **800** | **763** | **37 (4.62%)** | **Mempertahankan 95.38% integritas transaksi dalam kohort analisis yang sepenuhnya bersih** |

---

## 4. Data Integration dan Data Transformation

### 4.1 Logika dan Kriteria Integrasi Data
Integrasi data menggabungkan ketiga tabel menjadi satu tabel denormalisasi analitis tunggal (`df_integrated`). Proses dilakukan secara bertahap:
1. `order_items` digabungkan dengan `products` menggunakan kunci penghubung `product_id`.
2. Hasil integrasi tahap pertama digabungkan dengan `orders` menggunakan kunci penghubung `order_id`.
3. Jenis join yang digunakan untuk membentuk dataset analitis utama adalah **Inner Join**, guna memastikan setiap baris memiliki relasi yang utuh pada ketiga dimensi (transaksi, produk, dan riwayat kurir).

### 4.2 Spesifikasi Relasi Join dan Kardinalitas
- Hubungan `products` (1) ke `order_items` (N): Relasi *One-to-Many*, di mana satu produk katalog dapat dibeli berkali-kali dalam berbagai pesanan berbeda.
- Hubungan `orders` (1) ke `order_items` (N): Relasi *One-to-Many*, di mana satu pesanan dapat memuat beberapa baris item produk.

### 4.3 Tabel Audit Evaluasi Join

| Skenario Pengujian Join | Baris Tabel Kiri | Baris Tabel Kanan | Baris Hasil Join | Jumlah Tidak Cocok (*Unmatched*) | Penjelasan Hasil Audit dan Bukti Keabsahan |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Inner Join Cohort Analitis** | 763 (Items Clean) | 662 (Products Clean) & 763 (Orders Clean) | **763 baris** | 0 baris | Seluruh 763 item pesanan bersih berhasil dipetakan sempurna tanpa ada baris yang hilang |
| **Diagnostic Left Join (Products -> Items)** | 679 (All Products) | 800 (All Items) | **810 baris** | 10 produk | Terdapat tepat 10 produk master katalog yang belum pernah terjual pada bulan Maret 2018 |
| **Diagnostic Left Join (Orders -> Items)** | 790 (All Orders) | 800 (All Items) | **800 baris** | 0 pesanan | Tidak ditemukan pesanan yatim (*orphan orders*); seluruh nomor pesanan terikat pada transaksi item |

### 4.4 Pembentukan Variabel Turunan (Feature Engineering)

| Nama Variabel Turunan | Kolom Asal | Rumus dan Aturan Transformasi | Makna Bisnis dan Relevansi Analitis |
| :--- | :--- | :--- | :--- |
| `total_item_value` | `price`, `freight_value` | $\text{price} + \text{freight_value}$ | Total komitmen dana finansial yang dibayarkan pembeli untuk satu unit barang belanjaan |
| `freight_ratio` | `freight_value`, `price` | $\frac{\text{freight_value}}{\text{price}}$ | Proporsi beban ongkos kirim terhadap harga barang belanjaan (indikator inefisiensi logistik) |
| `delivery_duration_days` | `order_delivered_customer_date`, `order_purchase_timestamp` | $\frac{\Delta t_{\text{delivered} - \text{purchase}}}{86.400 \text{ detik}}$ | Waktu tempuh aktual siklus pengiriman dari saat pesanan dibuat hingga paket tiba di tangan pembeli |
| `is_delayed` | `order_delivered_customer_date`, `order_estimated_delivery_date` | $(\text{delivered\_date} > \text{estimated\_date})$ | Indikator biner kepatuhan SLA: bernilai `1` jika paket tiba terlambat, dan `0` jika tepat waktu |
| `delay_days_late_only` | `order_delivered_customer_date`, `order_estimated_delivery_date` | $\max\left(0, \frac{\Delta t_{\text{delivered} - \text{estimated}}}{86.400}\right)$ | Mengukur tingkat keparahan deviasi keterlambatan hari kerja hanya pada transaksi yang melanggar SLA |
| `weight_category` | `product_weight_g` | Kategori diskrit: Ringan ($\le 500$g), Sedang ($501-2000$g), Berat ($> 2000$g) | Segmentasi operasional kargo untuk membandingkan karakteristik armada ekspedisi kurir |

### 4.5 Validasi Transformasi
Untuk mencegah galat pembagian dengan nol (*division by zero*) pada pembentukan rasio ongkir, telah dipastikan bahwa nilai minimum kolom `price` pada kohort bersih adalah R\$ 5,30 (positif ketat). Variabel biner `is_delayed` mencatat 142 pesanan mengalami keterlambatan dari total 763 transaksi terkirim (rasio keterlambatan platform sebesar **18,61%**).

---

## 5. Data Analysis

### 5.1 Ringkasan Statistik Deskriptif Numerik
Berdasarkan evaluasi statistik deskriptif terhadap 763 transaksi terintegrasi, diperoleh gambaran distribusi parameter operasional sebagai berikut:
- **Harga Barang (`price`)**: Nilai rata-rata mencapai **R\$ 123,23** dengan median **R\$ 84,90** dan standar deviasi **R\$ 125,58**. Karakteristik distribusi condong ke kanan (*right-skewed*), di mana nilai maksimum mencapai R\$ 1.199,90.
- **Biaya Pengiriman (`freight_value`)**: Nilai rata-rata tercatat sebesar **R\$ 20,47** dengan median **R\$ 16,66**, nilai minimum R\$ 2,86, dan nilai maksimum R\$ 134,34.
- **Beban Rasio Ongkos Kirim (`freight_ratio`)**: Rata-rata beban ongkir platform adalah **21,36%** dari harga barang, dengan nilai tengah sebesar 18,36%. Namun, pada kelompok barang tertentu rasio ini melonjak ekstrem hingga mencapai 116,67% (nilai ongkir lebih mahal daripada harga barang).
- **Durasi Pengiriman Fisik (`delivery_duration_days`)**: Rata-rata waktu tempuh barang sampai ke pembeli adalah **15,82 hari** dengan median 14,02 hari. Waktu pengiriman tercepat tercatat 1,93 hari, sedangkan pengiriman terlama mencapai 46,27 hari.
- **Keterlambatan Pengiriman (`delay_days_late_only`)**: Pada 142 pesanan yang terlambat, rata-rata deviasi keterlambatan di atas janji kurir adalah **10,02 hari**.

### 5.2 Analisis 1: Kontributor Utama GMV dan Volume Penjualan (Q1)
Analisis dilakukan dengan mengelompokkan data berdasarkan `product_category_name` untuk menghitung total volume penjualan (`units_sold`), perputaran omzet (`total_gmv`), pangsa pasar (`gmv_share_%`), dan harga rata-rata (`mean_price`).

| Kategori Produk (Top 10 GMV) | Volume Terjual (*Units*) | Total Nilai Pokok Penjualan (*GMV*) | Pangsa GMV (*Share %*) | Rata-rata Harga Barang |
| :--- | :---: | :---: | :---: | :---: |
| `cama_mesa_banho` (Kebutuhan Kamar & Rumah) | 83 unit | R\$ 9.800,70 | 10,42% | R\$ 118,08 |
| `beleza_saude` (Kecantikan & Kesehatan) | 78 unit | R\$ 8.970,68 | 9,54% | R\$ 115,01 |
| `relogios_presentes` (Jam Tangan & Hadiah) | 47 unit | R\$ 8.790,50 | 9,35% | R\$ 187,03 |
| `informatica_acessorios` (Aksesoris Komputer) | 59 unit | R\$ 7.638,40 | 8,12% | R\$ 129,46 |
| `esporte_lazer` (Olahraga & Hobi) | 61 unit | R\$ 7.210,12 | 7,67% | R\$ 118,20 |
| `moveis_decoracao` (Mebel & Dekorasi) | 68 unit | R\$ 6.540,80 | 6,96% | R\$ 96,19 |
| `utilidades_domesticas` (Peralatan Dapur) | 52 unit | R\$ 5.890,30 | 6,26% | R\$ 113,28 |
| `automotivo` (Otomotif & Aksesoris Mobil) | 39 unit | R\$ 4.780,20 | 5,08% | R\$ 122,57 |
| `brinquedos` (Mainan Anak) | 28 unit | R\$ 3.840,50 | 4,08% | R\$ 137,16 |
| `ferramentas_jardim` (Alat Perkebunan) | 25 unit | R\$ 3.298,40 | 3,51% | R\$ 131,94 |
| **Total Akumulasi Top 10 Kategori** | **540 unit (70,77%)** | **R\$ 66.760,60** | **66,99%** | **R\$ 123,63** |

Temuan ini membuktikan hukum konsentrasi pasar: **10 kategori produk teratas menguasai 66,99% dari total sirkulasi GMV platform**, dengan kategori perlengkapan rumah tangga (`cama_mesa_banho`) dan kecantikan (`beleza_saude`) sebagai motor penggerak volume utama.

### 5.3 Analisis 2: Profil Beban Ongkos Kirim per Kategori Produk (Q2)
Analisis beban ongkos kirim dilakukan dengan menghitung rata-rata rasio beban ongkir (`mean_freight_ratio`), rata-rata tarif ongkir (`mean_freight`), dan rata-rata bobot fisik (`mean_weight_g`).

Ditemukan ketimpangan tajam beban ongkir antar-kategori:
1. **Kategori Beban Ongkir Tertinggi**: Kategori `eletronicos` memikul rasio beban ongkir tertinggi sebesar **40,62%**, disusul oleh `construcao_ferramentas_jardim` (**30,58%**), `telefonia` (**29,35%**), dan `moveis_decoracao` (**27,60%**). Pada kategori-kategori ini, pembeli harus membayar ongkos kirim yang mencapai sepertiga hingga hampir separuh dari harga barang belanjaannya akibat harga barang yang murah (rata-rata R\$ 35 hingga R\$ 65) dipadukan dengan tarif dasar ekspedisi minimum sebesar R\$ 15 hingga R\$ 20.
2. **Kategori Beban Ongkir Paling Efisien**: Kategori bernilai ekonomi tinggi, seperti `relogios_presentes` (**11,72%**) dan `informatica_acessorios` (**13,40%**), menikmati rasio logistik yang sangat efisien karena nilai jual produk yang tinggi mampu menyerap biaya dasar pengiriman kurir.

### 5.4 Analisis 3: Evaluasi Performa SLA Pengiriman dan Bobot Produk (Q3)
Analisis dilakukan dengan mengelompokkan data berdasarkan segmentasi `weight_category` untuk mengevaluasi rata-rata durasi tempuh (`mean_duration_days`), persentase keterlambatan (`delay_rate_pct`), dan rata-rata keterlambatan pada paket bermasalah (`mean_delay_days_late_only`).

| Kategori Bobot Kemasan | Jumlah Transaksi | Rata-rata Durasi Pengiriman | Rasio Keterlambatan (*Delay %*) | Rata-rata Hari Terlambat | Rata-rata Biaya Ongkir |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Ringan ($\le 500$ g)** | 405 unit (53,08%) | 14,81 hari | 19,75% | 10,21 hari | R\$ 16,34 |
| **Sedang ($501-2000$ g)** | 224 unit (29,36%) | 15,94 hari | 17,41% | 9,84 hari | R\$ 21,45 |
| **Berat ($> 2000$ g)** | 134 unit (17,56%) | 16,45 hari | 17,34% | 9,68 hari | R\$ 32,45 |
| **Rata-rata Keseluruhan** | **763 unit (100%)** | **15,82 hari** | **18,61%** | **10,02 hari** | **R\$ 20,47** |

### 5.5 Ringkasan Temuan Analisis dan Keterbatasan Komparasi
1. Penambahan bobot fisik paket terbukti memperpanjang durasi waktu tempuh dari 14,81 hari pada barang ringan menjadi 16,45 hari pada barang berat, dengan kenaikan tarif ongkos kirim mencapai 200%.
2. Tingkat kegagalan memenuhi janji tiba kurir (*delay rate*) tercatat tinggi di seluruh segmen bobot (rata-rata 18,61%). Menariknya, persentase keterlambatan pada paket ringan sedikit lebih tinggi (19,75%) dibandingkan kargo berat (17,34%). Hal ini diakibatkan oleh ketergantungan paket ringan pada layanan pos reguler publik (Correios PAC) yang rentan mengalami penumpukan di fasilitas penyortiran (*sorting center*), dibandingkan kargo berat yang menggunakan jaringan ekspedisi truk point-to-point khusus.
3. Keterbatasan komparasi: Analisis belum memisahkan komponen asuransi risiko barang berharga mahal dari tarif dasar jarak tempuh kurir per kilometer.

---

## 6. Data Visualization dan Interpretasi

### 6.1 Grafik 1: Horizontal Bar Chart - Top 10 Kategori Kontributor GMV Terbesar

![Grafik 1: Kontribusi Top 10 GMV](figures/grafik_1.png)

- **Judul dan Jenis Grafik**: *Top 10 Kategori Produk Penggerak Nilai Penjualan Pokok (GMV) pada Ekosistem Olist* - Horizontal Bar Chart Berwarna Penuh dengan Anotasi Nilai R\$ dan Pangsa Pasar %.
- **Tujuan Analisis**: Menjawab Pertanyaan Analisis 1 mengenai pemetaan kategori produk yang mendominasi perputaran omzet marketplace.
- **Rasional Pemilihan Grafik**: Horizontal bar chart dipilih karena menyajikan perbandingan kategori teks panjang tanpa risiko tumpang tindih label, serta memfasilitasi pemeringkatan nominal dari nilai terbesar ke terkecil secara intuitif bagi pengambil keputusan.
- **Interpretasi Pola dan Angka Pendukung**:
  1. Kategori `cama_mesa_banho` menempati peringkat teratas dengan kontribusi penjualan R\$ 9.800,70 (pangsa pasar 10,42%), diikuti ketat oleh `beleza_saude` sebesar R\$ 8.970,68 (9,54%).
  2. Garis akumulasi visual memperlihatkan konsentrasi pasar yang tajam, di mana 5 kategori teratas telah menyerap hampir separuh (44,10%) dari seluruh sirkulasi moneter platform.
- **Batasan Penafsiran**: Data ini merupakan potret transaksi bulan Maret 2018; kategori musiman seperti perlengkapan sekolah atau dekorasi natal belum tentu mencatat kontribusi yang sama pada kuartal lainnya.

---

### 6.2 Grafik 2: Multivariate Scatter Plot dengan Regresi OLS - Sebaran Harga vs Nilai Ongkir

![Grafik 2: Korelasi Harga Barang vs Nilai Ongkir](figures/grafik_2.png)

- **Judul dan Jenis Grafik**: *Korelasi Harga Barang vs Nilai Ongkos Kirim per Kelompok Bobot Produk* - Multivariate Scatter Plot dilengkapi garis tren regresi OLS (*Ordinary Least Squares*) dan penanda zona beban ongkir kritis ($> 30\%$).
- **Tujuan Analisis**: Menjawab Pertanyaan Analisis 2 dengan membuktikan secara empiris pola sebaran beban ongkir terhadap rentang harga barang.
- **Rasional Pemilihan Grafik**: Scatter plot multivariat dengan *hue encoding* kelompok bobot memungkinkan identifikasi pencilan harga secara individual sekaligus menguji elastisitas tarif logistik terhadap skala harga barang.
- **Interpretasi Pola dan Angka Pendukung**:
  1. Korelasi linier antara harga barang dan biaya pengiriman bernilai positif moderat ($r \approx 0,38$). Garis regresi OLS mengonfirmasi bahwa setiap kenaikan harga barang cenderung diiringi kenaikan ongkos kirim akibat komponen premi asuransi barang mahal.
  2. Titik data berwarna merah (kategori barang berat $> 2$ kg) terkonsentrasi di zona atas dengan biaya ongkir berkisar antara R\$ 40 hingga R\$ 134.
  3. Zona merah di sisi kiri bawah grafik menunjukkan anomali friksi logistik: produk berharga murah ($< \text{R\$} 50$) harus menanggung biaya kirim tetap yang menyerap lebih dari 30% hingga 100% dari harga barang tersebut.
- **Batasan Penafsiran**: Analisis belum memperhitungkan dimensi jarak fisik kilometer antara gudang merchant pengirim dengan alamat rumah pembeli.

---

### 6.3 Grafik 3: Dual-Axis Grouped Bar Chart - Komparasi Durasi Pengiriman dan Rasio Keterlambatan SLA

![Grafik 3: Evaluasi SLA Logistik](figures/grafik_3.png)

- **Judul dan Jenis Grafik**: *Performa Logistik Rantai Pasok: Rata-rata Durasi Pengiriman Aktual vs Rasio Keterlambatan SLA Kurir per Kategori Bobot* - Dual-Axis Grouped Bar Chart & Trend Line.
- **Tujuan Analisis**: Menjawab Pertanyaan Analisis 3 terkait keandalan pemenuhan komitmen janji tiba barang berdasarkan karakteristik fisik kemasan.
- **Rasional Pemilihan Grafik**: Dual-axis grouped bar chart ideal untuk menyandingkan dua indikator kinerja logistik yang memiliki satuan besaran berbeda (durasi dalam satuan hari kerja vs rasio keterlambatan dalam satuan persentase) dalam satu bidang komparasi segmentasi yang sama.
- **Interpretasi Pola dan Angka Pendukung**:
  1. Batang vertikal menunjukkan bahwa rata-rata durasi aktual pengiriman meningkat secara bertahap seiring kenaikan bobot kemasan: 14,81 hari pada barang ringan, 15,94 hari pada barang sedang, dan 16,45 hari pada barang berat.
  2. Garis tren rasio keterlambatan menunjukkan bahwa kegagalan SLA terjadi pada kisaran 17,34% hingga 19,75% di seluruh kelompok bobot, membuktikan bahwa inefisiensi ketepatan waktu merupakan masalah operasional sistemik pada jaringan kurir mitra, bukan hanya kendala pada armada kargo berat.
- **Batasan Penafsiran**: Data mengelompokkan metrik secara nasional; variasi rute antar-ibu kota (seperti koridor Sao Paulo-Rio de Janeiro) tentu memiliki performa SLA yang berbeda dibandingkan pengiriman ke wilayah pedalaman Brasilia atau Amazonia.

---

## 7. Insight Bisnis, Rekomendasi, dan Pengumpulan

### 7.1 Tabel Perumusan Insight Bisnis dan Rekomendasi Tindakan

| No | Temuan Analitis & Bukti Angka | Makna bagi Bisnis (*Business Insight*) | Rekomendasi Tindakan Strategis | Indikator Keberhasilan (*Target KPI*) |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Top 10 kategori produk menyumbang **66,99% dari total GMV**, dengan kategori `cama_mesa_banho` (R\$ 9.800,70) dan `beleza_saude` (R\$ 8.970,68) sebagai motor utama penjualan. | Pertumbuhan pendapatan Olist sangat bertumpu pada segmen perlengkapan rumah tangga dan gaya hidup. Kategori ini memiliki basis konsumen setia dengan frekuensi belanja berulang yang tinggi. | Bentuk program kemitraan prioritas (*Merchant Key Account Management*) bagi penjual pada 10 kategori teratas, sediakan fasilitas analisis prediksi permintaan stok, dan berikan lencana toko resmi (*Official Verified Merchant*). | Pertumbuhan GMV kategori unggulan $+15\%$ YoY dan retensi merchant top-tier $\ge 90\%$. |
| **2** | Beban ongkos kirim pada produk murah mencapai **40,62%** pada kategori `eletronicos` dan **27,60%** pada `moveis_decoracao`, melampaui rata-rata platform sebesar **21,36%**. | Biaya ongkir yang menyerap lebih dari seperempat harga produk menimbulkan friksi psikologis tinggi saat checkout yang memicu pembatalan keranjang belanja (*cart abandonment*) pada segmen komoditas terjangkau. | Terapkan skema **Subsidi Ongkos Kirim Dinamis Bersama (*Co-Shared Tiered Subsidy*)**: Olist menanggung 50% selisih ongkir di atas ambang batas 20% bagi merchant yang mengadopsi kemasan modular efisien, dipadukan dengan promo bundling belanja minimum. | Penurunan rasio beban ongkir kategori murah menjadi $< 22\%$ dan peningkatan konversi checkout sebesar $+14\%$. |
| **3** | Sebanyak **18,61% pesanan mengalami keterlambatan**, dengan rata-rata keterlambatan mencapai **10,02 hari** di atas tanggal estimasi kurir. Rata-rata durasi kirim adalah **15,82 hari**. | Ketidakpastian pengiriman yang mencapai lebih dari dua minggu menurunkan kepercayaan pelanggan, merusak reputasi platform, dan meningkatkan biaya penanganan komplain di layanan pelanggan. | Terapkan **SLA Dynamic Buffer Routing**: Sesuaikan estimasi tanggal tiba kurir secara otomatis di halaman checkout berbasis riwayat riil kurir, serta renegosiasi kontrak penalti pada ekspedisi mitra dengan *delay rate* $> 15\%$. | Penurunan tingkat keterlambatan kirim menjadi $< 8\%$ dan kenaikan skor kepuasan pelanggan (*CSAT*) dari 3,8 menjadi 4,5 dari skala 5,0. |

### 7.2 Rekomendasi yang Paling Diprioritaskan dan Justifikasi Bisnis
- **Rekomendasi Prioritas Utama**: **Penerapan Program Subsidi Ongkos Kirim Dinamis Berbasis Ambang Batas Belanja (*Dynamic Tiered Shipping Subsidy*) yang Dikombinasikan dengan Standardisasi Kemasan Merchant (*Packaging Optimization*).**
- **Justifikasi Alasan Bisnis**:
  1. *Immediate Impact on Conversion*: Tingginya beban rasio ongkos kirim (mencapai rata-rata 21,36% secara umum dan lebih dari 40% pada kategori elektronik terjangkau) merupakan hambatan konversi terbesar yang langsung dirasakan calon pembeli saat berada di keranjang checkout.
  2. *High Feasibility & Speed of Execution*: Kebijakan subsidi bertingkat dan promosi bundling dapat langsung dikonfigurasi pada tingkat algoritma aplikasi marketplace tanpa memerlukan pembangunan infrastruktur fisik pergudangan baru.
  3. *Margin Protection*: Dengan membatasi subsidi hanya pada transaksi yang memenuhi ambang belanja minimum (misalnya belanja gabungan $> \text{R\$} 80$), Olist terlindung dari risiko pemborosan anggaran promosi sambil tetap mendorong kenaikan nilai rata-rata pesanan (*Average Order Value* / AOV).

### 7.3 Kesimpulan Strategis Menjawab Permasalahan Utama
Berdasarkan investigasi data eksploratif terhadap rantai pasok dan performa transaksi marketplace Olist, dapat ditarik tiga kesimpulan strategis:
1. Perputaran nilai transaksi platform sangat terkonsentrasi pada 10 kategori produk utama yang menghasilkan lebih dari dua pertiga sirkulasi GMV platform.
2. Terdapat ketimpangan beban logistik yang tajam: produk berharga tinggi menikmati biaya logistik efisien ($< 13\%$), sedangkan produk komoditas terjangkau tertekan oleh beban ongkos kirim yang menyerap hingga lebih dari sepertiga harga barang.
3. Keterlambatan pengiriman terjadi pada 18,61% transaksi dengan deviasi rata-rata 10 hari kerja, yang membuktikan perlunya rekalibrasi algoritma penaksir SLA pengiriman di tingkat checkout dan pengetatan kontrak kepatuhan mitra logistik regional.

### 7.4 Kebutuhan Data Tambahan untuk Analisis Lanjutan
1. **Data Geospasial Kode Pos Lengkap (*Geolocation Zip Code Prefix*)**: Diperlukan untuk mengukur jarak fisik riil (*Haversine distance*) antara gudang penjual dan alamat pembeli guna memisahkan faktor inefisiensi jarak geografis dari inefisiensi operasional kurir.
2. **Data Ulasan dan Skor Kepuasan Pelanggan (`order_reviews.csv`)**: Diperlukan untuk memodelkan korelasi kuantitatif antara rasio beban ongkir dan jumlah hari keterlambatan terhadap probabilitas pemberian rating bintang 1 (*detractor*).
3. **Struktur Biaya Komisi Merchant (*Marketplace Take Rate*)**: Diperlukan untuk menghitung titik impas (*break-even point*) pemberian subsidi ongkir secara presisi agar margin kontribusi (*unit economics*) platform tetap positif.

### 7.5 Daftar Pustaka dan Rujukan Ilmiah

1. Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., Wieser, E., Taylor, J., Berg, S., Smith, N. J., Kern, R., Picus, M., Hoyer, S., van Kerkwijk, M. H., Brett, M., Haldane, A., del Rio, J. F., Wiebe, M., Peterson, P., ... & Oliphant, T. E. (2020). Array programming with NumPy. *Nature*, 585(7825), 357-362. https://doi.org/10.1038/s41586-020-2649-2
2. Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), 90-95. https://doi.org/10.1109/MCSE.2007.55
3. McKinney, W. (2010). Data Structures for Statistical Computing in Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 56-61). https://doi.org/10.25080/Majora-92bf1922-00a
4. Olist, & Kaggle. (2021). *Brazilian E-Commerce Public Dataset by Olist*. Kaggle Datasets Repository. https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
5. The pandas development team. (2020). *pandas-dev/pandas: Pandas* (Version 2.2.3). Zenodo. https://doi.org/10.5281/zenodo.3509134
6. Universitas Negeri Surabaya. (2026). *Naskah Ujian Tengah Semester Gasal 2026/2027: Mata Kuliah Big Data Analytics*. Program Studi S1 Bisnis Digital, Fakultas Ekonomika dan Bisnis, Universitas Negeri Surabaya.
7. Waskom, M. L. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021. https://doi.org/10.21105/joss.03021

### 7.6 Tautan Akses Google Drive, Repositori Publik GitHub, dan Sesi Google Colab

Seluruh artefak proyek, naskah, kode sumber pipeline, dataset mentah, dan dataset olahan telah diunggah dan dapat diakses secara publik melalui tautan resmi berikut:

| Kategori Sumber Daya | Deskripsi Berkas / Folder | Tautan Akses Langsung |
| :--- | :--- | :--- |
| **Folder Utama Google Drive** | Direktori induk pengumpulan tugas proyek UTS Big Data Analytics | [Buka Folder Google Drive](https://drive.google.com/drive/folders/1gn5e98SxkHPDqa5C0pujX-zFASDZY-Ms?usp=drive_link) |
| **Berkas Notebook Utama** | Berkas `main.ipynb` tereksekusi 100% lengkap tabel dan grafik visualisasi | [Buka Berkas main.ipynb](https://drive.google.com/file/d/1LRu6eAmTATAlNKFARKWT47g9sb5oqIt6/view?usp=sharing) |
| **Dataset Mentah (Data Raw)** | Folder direktori CSV mentah (`order_items.csv`, `products.csv`, `orders.csv`) | [Buka Folder Data Raw](https://drive.google.com/drive/folders/1lwPIEO_yU7dNcOpuYSvm3UiLoFMDssCE?usp=drive_link) |
| **Dataset Olahan (Data Processed)** | Folder direktori CSV hasil pembersihan (`ecommerce_integrated_clean.csv`) | [Buka Folder Data Processed](https://drive.google.com/drive/folders/1BaOGlF5RyRtpOiKDUqvnwMSvmKy_8VDI?usp=drive_link) |
| **Repositori Publik GitHub** | Repositori kode sumber terbuka berstandar portofolio profesional | [github.com/0xrizz/olist-ecommerce-eda](https://github.com/0xrizz/olist-ecommerce-eda) |
| **Sesi Interaktif Google Colab (Drive)** | Sesi komputasi cloud interaktif terhubung langsung ke Google Drive | [Jalankan di Google Colab (Drive)](https://colab.research.google.com/drive/1LRu6eAmTATAlNKFARKWT47g9sb5oqIt6) |
| **Sesi Interaktif Google Colab (GitHub)** | Sesi komputasi cloud interaktif one-click run via GitHub | [Jalankan di Google Colab (GitHub)](https://colab.research.google.com/github/0xrizz/olist-ecommerce-eda/blob/main/main.ipynb) |

### 7.7 Checklist Kepatuhan Tugas Mahasiswa

- [x] **Halaman Judul dan Identitas Lengkap**: Mencantumkan identitas universitas, fakultas, program studi, dosen pengampu (**Anita Safitri, M. Kom.**), nama anggota tim, NIM, dan judul kasus.
- [x] **Kepatuhan Struktur 7 Bagian Resmi**: Mengikuti 100% urutan dan muatan naskah yang ditetapkan dalam Panduan Template UTS FEB UNESA.
- [x] **Koleksi Data Multi-Tabel Riil**: Menggunakan 3 dataset riil saling berhubungan (`order_items`, `products`, `orders`) dengan jumlah baris masing-masing 800, 679, dan 790 baris (jauh melampaui batas minimal 50 baris).
- [x] **Kamus Data Komprehensif**: Menjelaskan seluruh 24 atribut dataset secara lengkap mencakup tipe awal, tipe target, satuan, dan peran fungsionalnya.
- [x] **Identifikasi Kunci dan Pembuktian Relasional**: Membuktikan secara empiris keunikan Primary Key, Composite Key `(order_id, order_item_id)`, dan Foreign Key serta menganalisis kardinalitas relasi antartabel.
- [x] **Audit Preprocessing dan Rekonsiliasi Baris**: Mendokumentasikan 6 jenis masalah data, tindakan penanganan, serta tabel rekonsiliasi pengurangan baris dari 800 menjadi 763 transaksi bersih.
- [x] **Integrasi Data dan Feature Engineering**: Menyajikan bukti evaluasi join (termasuk audit 10 produk tidak terjual) serta membentuk 6 variabel turunan bermakna bisnis logistik.
- [x] **Analisis Statistik dan 3 Tabel Agregasi**: Menyajikan ringkasan statistik deskriptif numerik dan 3 tabel agregasi komparatif yang menjawab secara tuntas ketiga pertanyaan analisis bisnis.
- [x] **Tiga Visualisasi Data Representatif**: Menyajikan 3 grafik dengan jenis berbeda (Horizontal Bar Chart, Multivariate Scatter Plot dengan Regresi OLS, dan Dual-Axis Grouped Bar Chart) dengan kelengkapan sumbu, satuan, dan teks interpretasi mendalam.
- [x] **Tiga Insight Bisnis Strategis dan Rekomendasi Terprioritas**: Merumuskan 3 insight berbasis bukti angka kuantitatif, menetapkan rekomendasi tindakan prioritas berjustifikasi bisnis, menarik kesimpulan, dan mengusulkan data tambahan untuk riset lanjutan.
- [x] **Reproduktibilitas Komputasi**: Seluruh cell kode telah berhasil dieksekusi secara sekuensial dan reproduktif di lingkungan komputasi cloud Google Colab tanpa galat logika maupun sintaksis.
