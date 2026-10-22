# Olist E-Commerce Logistics & Profitability EDA

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2%2B-150458.svg)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-0.13%2B-4c72b0.svg)](https://seaborn.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.8%2B-11557c.svg)](https://matplotlib.org/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/0xrizz/olist-ecommerce-eda/blob/main/main.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Academic Project](https://img.shields.io/badge/Coursework-FEB%20UNESA-003366.svg)](https://unesa.ac.id)

An end-to-end exploratory data analysis and data engineering pipeline investigating transaction profitability, supply chain efficiency, and freight fee disparities (*freight ratio*) across Brazilian marketplace aggregator **Olist**.

---

## Executive Project Overview

This repository hosts the official coursework project for **Big Data Analytics (Midterm Examination / UTS Gasal 2026/2027)** at the **Faculty of Economics and Business, Universitas Negeri Surabaya (FEB UNESA)**.

- **Supervising Lecturer**: **Anita Safitri, M. Kom.**
- **Research Team**:
  1. **Pramono Tirta Luhung** (NIM: 23081494340)
  2. **Achmad Azhar Abdullah** (NIM: 23081494303)
- **Academic Program**: S1 Bisnis Digital (Class of 2023 - Consultant Track)

---

## Quick Access & Artifact Links

| Resource | Target Link | Description |
| :--- | :--- | :--- |
| **Interactive Colab Session (Drive)** | [Open in Google Colab (Drive)](https://colab.research.google.com/drive/11_CaVUcowf4VQ6lwV51AMwz9EXbf082p) | Live cloud notebook instance stored in Google Drive |
| **Interactive Colab Session (GitHub)** | [Launch via GitHub](https://colab.research.google.com/github/0xrizz/olist-ecommerce-eda/blob/main/main.ipynb) | One-click instant cloud runtime with pre-executed cells |
| **Main Notebook File** | [Google Drive File](https://drive.google.com/file/d/11_CaVUcowf4VQ6lwV51AMwz9EXbf082p/view?usp=drive_link) | Direct access to `main.ipynb` (38 cells, 17 executed code cells) |
| **Raw Datasets Folder** | [Google Drive Data Raw](https://drive.google.com/drive/folders/1ThnaciQefpKZxkSeI9DAktUeAKCOuK2-?usp=drive_link) | Unprocessed CSV source datasets from Kaggle Olist |
| **Processed Datasets Folder** | [Google Drive Data Processed](https://drive.google.com/drive/folders/13pPoj6V8qU_oq20GbmbXqPdR2k9Hdt-g?usp=drive_link) | Cleaned, validated, and integrated transactional CSV |
| **Master Coursework Drive Folder** | [Google Drive Submission Folder](https://drive.google.com/drive/folders/1aWfUipbLlvZINFzDbY7F5TA2XWoIrIB1?usp=drive_link) | Complete project repository archive on Google Drive |
| **Formal Publication PDF** | [laporan-proyek-uts.pdf](./laporan-proyek-uts.pdf) | Formal 7-chapter FEB UNESA report rendered with newsletter typography |

---

## Business Problem & Research Questions

As an aggregator connecting independent merchants across Brazil's 8.5 million km² territory, Olist experiences substantial friction from continental-scale logistics costs (*freight fee*). These logistics charges often create severe disparities in customer checkout conversion, cart abandonment, and customer satisfaction.

### Primary Objectives & Research Questions
1. **Q1 (GMV & Volume Concentration)**: Which product categories drive the largest share of Gross Merchandise Value (GMV) and transaction volume, and how concentrated is platform revenue?
2. **Q2 (Freight Ratio Disparity)**: How does the freight burden ratio (`freight_ratio = freight_value / total_item_value * 100`) vary across product categories and price points? Do premium items benefit from disproportionately lower logistics burdens compared to commodity goods?
3. **Q3 (Logistics SLA & Delivery Delays)**: What is the correlation between physical product weight/dimensions and carrier delivery duration? What proportion of orders suffer from delivery delays against carrier service-level promises (*SLA breach*), and what is the typical delay magnitude?

---

## Relational Data Architecture

The pipeline ingests multi-table transactional data sourced from the public [Kaggle Brazilian E-Commerce Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce):

```
                   +-----------------------+
                   |      orders.csv       |
                   |-----------------------|
                   | PK: order_id          |
                   |     customer_id       |
                   |     order_status      |
                   |     timestamps...     |
                   +-----------+-----------+
                               | 1
                               |
                               | N
                   +-----------v-----------+               +-----------------------+
                   |    order_items.csv    |               |     products.csv      |
                   |-----------------------|               |-----------------------|
                   | PK: (order_id,        | N           1 | PK: product_id        |
                   |      order_item_id)   +--------------->     product_category  |
                   | FK: product_id        |               |     product_weight_g  |
                   | FK: order_id          |               |     dimensions...     |
                   |     price             |               +-----------------------+
                   |     freight_value     |
                   +-----------------------+
```

### Relational Schema Summary

| Dataset | File Path | Raw Rows | Clean Rows | Key Type & Role |
| :--- | :--- | :---: | :---: | :--- |
| **Order Items** | `data/raw/order_items.csv` | 800 | 763 | Composite Key: `(order_id, order_item_id)` |
| **Products** | `data/raw/products.csv` | 679 | 667 | Primary Key: `product_id` (12 missing categories removed) |
| **Orders** | `data/raw/orders.csv` | 790 | 772 | Primary Key: `order_id` (18 non-delivered orders filtered) |
| **Integrated Clean** | `data/processed/ecommerce_integrated_clean.csv` | - | 763 | Unified analysis table with 100% relational integrity |

---

## 8-Stage Data Engineering & Machine Learning Pipeline

The project is structured according to professional Data Engineering and ML Pipeline standards in [`main.ipynb`](./main.ipynb):

1. **Stage 1: Runtime & Configuration**: Environment initialization, dependency imports (`pandas`, `seaborn`, `matplotlib`, `numpy`), visual themes, and reproducibility seeds.
2. **Stage 2: Data Ingestion & Relational Schema Audit**: Loading source CSVs, structural verification, attribute typing, and full 24-column data dictionary.
3. **Stage 3: Data Integrity & Key Uniqueness Verification**: Empirical mathematical assertions verifying Composite Key uniqueness, Primary Key uniqueness, and Foreign Key referential integrity.
4. **Stage 4: Data Quality Auditing & Cleaning Pipeline**: Systematic detection and mitigation of missing values, anomalies, duplicates, and physical dimensional outliers.
5. **Stage 5: Relational Integration & Feature Engineering**: Two-stage relational joins (`order_items` $\bowtie$ `products` $\bowtie$ `orders`), unmapped key auditing, and creation of derived analytical features (`total_item_value`, `freight_ratio`, `delivery_duration_days`, `is_delayed`, `delay_days`).
6. **Stage 6: Exploratory Data Analysis & Analytical Aggregations**: Descriptive parametric statistics, IQR spread measures, and 3 structured aggregation tables answering Q1, Q2, and Q3.
7. **Stage 7: Production-Grade Visualizations & Econometric Diagnostics**:
   - **Figure 1**: Horizontal Bar Chart displaying Top 10 GMV Contributors.
   - **Figure 2**: Multivariate Scatter Plot with OLS linear trendline capturing Price vs. Freight Ratio dynamics.
   - **Figure 3**: Dual-Axis Grouped Bar Chart contrasting Mean Delivery Duration against SLA Delay Ratios.
8. **Stage 8: Business Intelligence Synthesis & Strategic Decision Engine**: Actionable insight formulation, quantitative KPIs, prioritised business interventions, and academic references.

---

## Key Empirical Findings

```
Metric                             Observed Value      Business Implication
--------------------------------------------------------------------------------------------------
Top 10 Categories GMV Share        67.14%              High revenue concentration; key driver of margins
Overall Mean Freight Ratio         24.19%              Nearly a quarter of checkout spend is logistics
Budget Products Freight Ratio      34.82%              High barrier to entry for low-cost goods (< R$ 50)
Premium Products Freight Ratio     12.65%              Economies of scale benefit high-ticket items (> R$ 150)
Carrier SLA Breach Rate            18.61%              Nearly 1 in 5 orders arrives after promised date
Mean Delay on Breached Orders      10.0 working days   Substantial operational volatility across carriers
```

---

## Repository Structure

```
.
├── README.md                      # Open-source project documentation and portfolio guide
├── Brief.md                       # Academic assignment specification & compliance checklist
├── main.ipynb                     # Production 8-stage DE/ML pipeline executed on Google Colab VM
├── laporan-proyek-uts.md          # Master 7-chapter FEB UNESA report (Markdown source)
├── laporan-proyek-uts.pdf         # Official report PDF with newsletter typography & vector graphics
├── data/
│   ├── raw/                       # Source Kaggle transactional extracts
│   │   ├── order_items.csv        # 800 transaction item records
│   │   ├── products.csv           # 679 product catalog records
│   │   └── orders.csv             # 790 order lifecycle records
│   └── processed/
│       └── ecommerce_integrated_clean.csv # 763 cleaned, fully joined records
├── figures/                       # High-resolution visual assets and chart exports
│   ├── colab-logo.svg             # Official Google Colab vector emblem
│   ├── colab-logo.png             # Rasterized Colab emblem
│   ├── unesa-logo.png             # Universitas Negeri Surabaya official emblem
│   ├── grafik_1.png               # Top 10 GMV horizontal bar chart
│   ├── grafik_2.png               # Price vs freight ratio OLS scatter plot
│   └── grafik_3.png               # SLA delay & delivery duration grouped bar chart
└── scripts/                       # Automated build, rendering, and post-processing tools
    ├── export-pdf.mjs             # Pandoc and headless Google Chrome PDF export engine
    ├── postprocess-pdf.py         # PyMuPDF bookmark outline and running header/footer stamper
    └── pdf-styles.css             # Newsletter typography styling rules and monochrome palettes
```

---

## Getting Started & Execution

### Option A: Cloud Execution via Google Colab (Recommended)
Click the badge below to run the notebook instantly in Google Colab without local setup:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/0xrizz/olist-ecommerce-eda/blob/main/main.ipynb)

### Option B: Local Environment Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/0xrizz/olist-ecommerce-eda.git
   cd olist-ecommerce-eda
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install pandas seaborn matplotlib numpy scipy
   ```

4. **Launch the notebook**:
   ```bash
   jupyter notebook main.ipynb
   ```

---

## Citations & Academic References

1. Harris, C. R., et al. (2020). Array programming with NumPy. *Nature*, 585(7825), 357-362.
2. Hunter, J. D. (2007). Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), 90-95.
3. McKinney, W. (2010). Data Structures for Statistical Computing in Python. *Proc. 9th Python in Science Conf.*, 56-61.
4. Olist, & Kaggle. (2021). *Brazilian E-Commerce Public Dataset by Olist*. Kaggle Datasets Repository.
5. The pandas development team. (2020). *pandas-dev/pandas: Pandas* (Version 2.2.3). Zenodo.
6. Waskom, M. L. (2021). seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021.

---

## License

This project is open-source under the [MIT License](LICENSE). Academic content and analysis are published for educational evaluation at Universitas Negeri Surabaya.
