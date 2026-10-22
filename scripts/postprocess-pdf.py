#!/usr/bin/env python3
"""
Post-processing pipeline for Big Data UTS EDA Project Report PDF.

Capabilities:
1. Dynamic page scanning for sections 1 to 10 and subheadings.
2. Generates hierarchical interactive PDF Bookmarks (TOC Outline).
3. Stamps running headers and footers on all pages (except Cover Page 1) with hairline dividers.
4. Optimizes PDF stream and structure with garbage collection and deflation.
"""

import argparse
import os
import re
import sys
from pathlib import Path
import pymupdf

SCRIPT_DIR = Path(__file__).resolve().parent
WEEK6_ROOT = SCRIPT_DIR.parent
DEFAULT_PDF = WEEK6_ROOT / "laporan-proyek-uts.pdf"

TARGET_HEADINGS = [
    (1, "Halaman Judul & Identitas Proyek", r"LAPORAN RESMI PROYEK UJIAN TENGAH SEMESTER", 1),
    (1, "1. Permasalahan Bisnis dan Data Collection", r"1\.\s*Permasalahan Bisnis dan Data Collection", 2),
    (2, "1.1 Konteks Usaha dan Organisasi", r"1\.1\s*Konteks Usaha dan Organisasi", 2),
    (2, "1.2 Permasalahan Bisnis Utama", r"1\.2\s*Permasalahan Bisnis Utama", 2),
    (2, "1.3 Keputusan Bisnis yang Ingin Didukung", r"1\.3\s*Keputusan Bisnis yang Ingin Didukung", 2),
    (2, "1.4 Pertanyaan Analisis", r"1\.4\s*Pertanyaan Analisis", 2),
    (2, "1.5 Tabel Dokumentasi Pengumpulan Data", r"1\.5\s*Tabel Dokumentasi Pengumpulan Data", 2),
    (2, "1.6 Izin Penggunaan dan Perlindungan Data Pribadi", r"1\.6\s*Izin Penggunaan", 2),
    (2, "1.7 Keterbatasan Cakupan Data", r"1\.7\s*Keterbatasan Cakupan Data", 2),
    (1, "2. Data Loading dan Data Understanding", r"2\.\s*Data Loading dan Data Understanding", 2),
    (2, "2.1 Lokasi dan Cara Memuat CSV di Google Colab", r"2\.1\s*Lokasi dan Cara Memuat CSV", 2),
    (2, "2.2 Struktur Awal Dataset", r"2\.2\s*Struktur Awal Dataset", 2),
    (2, "2.3 Tabel Kamus Data Lengkap (24 Atribut)", r"2\.3\s*Tabel Kamus Data Lengkap", 2),
    (2, "2.4 Identifikasi Kunci dan Pembuktian Relasional", r"2\.4\s*Identifikasi Kunci dan Pembuktian", 2),
    (1, "3. Data Preprocessing", r"3\.\s*Data Preprocessing", 2),
    (2, "3.1 Hasil Audit Awal Kualitas Data", r"3\.1\s*Hasil Audit Awal", 2),
    (2, "3.2 Tabel Dokumentasi Masalah dan Tindakan Perbaikan", r"3\.2\s*Tabel Dokumentasi Masalah", 2),
    (2, "3.3 Tabel Komparasi Jumlah Baris Sebelum dan Sesudah", r"3\.3\s*Tabel Komparasi Jumlah Baris", 2),
    (1, "4. Data Integration dan Data Transformation", r"4\.\s*Data Integration dan Data Transformation", 2),
    (2, "4.1 Logika dan Kriteria Integrasi Data", r"4\.1\s*Logika dan Kriteria Integrasi", 2),
    (2, "4.2 Tabel Audit Evaluasi Join", r"4\.2\s*Tabel Audit Evaluasi Join", 2),
    (2, "4.3 Pembentukan Variabel Turunan (Feature Engineering)", r"4\.3\s*Pembentukan Variabel Turunan", 2),
    (1, "5. Data Analysis", r"5\.\s*Data Analysis", 2),
    (2, "5.1 Ringkasan Statistik Deskriptif Numerik", r"5\.1\s*Ringkasan Statistik Deskriptif", 2),
    (2, "5.2 Analisis 1: Kontributor Utama GMV dan Volume (Q1)", r"5\.2\s*Analisis 1", 2),
    (2, "5.3 Analisis 2: Profil Beban Ongkos Kirim per Kategori (Q2)", r"5\.3\s*Analisis 2", 2),
    (2, "5.4 Analisis 3: Evaluasi Performa SLA Pengiriman (Q3)", r"5\.4\s*Analisis 3", 2),
    (1, "6. Data Visualization dan Interpretasi", r"6\.\s*Data Visualization dan Interpretasi", 2),
    (2, "6.1 Grafik 1: Horizontal Bar Chart — Top 10 GMV", r"6\.1\s*Grafik 1", 2),
    (2, "6.2 Grafik 2: Multivariate Scatter Plot — Harga vs Ongkir", r"6\.2\s*Grafik 2", 2),
    (2, "6.3 Grafik 3: Dual-Axis Bar Chart — Evaluasi SLA Logistik", r"6\.3\s*Grafik 3", 2),
    (1, "7. Insight Bisnis, Rekomendasi, dan Pengumpulan", r"7\.\s*Insight Bisnis, Rekomendasi", 2),
    (2, "7.1 Tabel Perumusan Insight dan Rekomendasi Tindakan", r"7\.1\s*Tabel Perumusan Insight", 2),
    (2, "7.2 Rekomendasi yang Paling Diprioritaskan", r"7\.2\s*Rekomendasi yang Paling Diprioritaskan", 2),
    (2, "7.3 Kesimpulan Akhir", r"7\.3\s*Kesimpulan Akhir", 2),
    (2, "7.4 Data Tambahan yang Diperlukan", r"7\.4\s*Data Tambahan yang Diperlukan", 2),
    (1, "8. Daftar Pustaka dan Rujukan", r"8\.\s*Daftar Pustaka dan Rujukan", 2),
    (1, "9. Manifest Pengumpulan Berkas", r"9\.\s*Manifest Pengumpulan Berkas", 2),
    (1, "10. Checklist Akhir Kepatuhan Spesifikasi", r"10\.\s*Checklist Akhir Kepatuhan", 2),
]


def scan_headings(doc):
    """Scan PDF pages to find exact page occurrences for each section and chapter."""
    toc = []
    for level, title, pattern, min_pno in TARGET_HEADINGS:
        found_page = None
        for pno in range(min_pno - 1, len(doc)):
            page_text = doc[pno].get_text()
            if re.search(pattern, page_text, re.IGNORECASE):
                found_page = pno + 1
                break

        if found_page:
            toc.append([level, title, found_page])
            print(f"[postprocess:scan] Level {level} | '{title}' -> Page {found_page}")
        else:
            print(f"[postprocess:scan:warning] Heading not found: '{title}'")

    return toc


def stamp_headers_and_footers(doc):
    """
    Stamp running header & footer on all pages except Page 1 (Cover):
    - Top running header:
      - Hairline divider at y ≈ 38 pt
      - Left: 'LAPORAN PROYEK UTS • BIG DATA ANALYTICS (FEB UNESA)'
      - Right: 'Pramono Tirta L. & Achmad Azhar A.'
    - Bottom running footer:
      - Hairline divider at y ≈ 806 pt
      - Left: UNESA icon (11x11 pt) + 'S1 BISNIS DIGITAL 2023 • E-COMMERCE OLIST EDA'
      - Right: 'Halaman {pno} dari {total_pages}'
    """
    total_pages = len(doc)
    left_margin = 56.7   # 20mm
    header_line_y = 36.0
    header_text_y = 30.0
    footer_line_y = 806.0
    footer_text_y = 818.0

    divider_color = (0.75, 0.82, 0.90)   # subtle soft blue
    header_color = (0.35, 0.42, 0.52)    # slate blue
    footer_color = (0.25, 0.32, 0.42)
    font_size = 7.2
    font_name = "helv"

    header_left = "LAPORAN PROYEK UTS • BIG DATA ANALYTICS (FEB UNESA)"
    header_right = "Pramono Tirta L. & Achmad Azhar A."
    footer_left_text = "S1 BISNIS DIGITAL 2023 • E-COMMERCE OLIST EDA"

    unesa_icon_path = WEEK6_ROOT / "figures" / "unesa-logo.png"
    rect_unesa = pymupdf.Rect(56.7, 808.5, 68.7, 820.5)
    xref_unesa = None

    stamped_count = 0
    # Skip page 0 (Cover)
    for pno in range(1, total_pages):
        page = doc[pno]
        page_width = page.rect.width
        right_margin = page_width - left_margin

        # 1. Top Running Header
        # Hairline
        p_h1 = pymupdf.Point(left_margin, header_line_y)
        p_h2 = pymupdf.Point(right_margin, header_line_y)
        page.draw_line(p_h1, p_h2, color=divider_color, width=0.5)

        # Header Left Text
        page.insert_text(
            pymupdf.Point(left_margin, header_text_y),
            header_left,
            fontsize=font_size,
            fontname=font_name,
            color=header_color,
        )

        # Header Right Text
        hw = pymupdf.get_text_length(header_right, fontname=font_name, fontsize=font_size)
        page.insert_text(
            pymupdf.Point(right_margin - hw, header_text_y),
            header_right,
            fontsize=font_size,
            fontname=font_name,
            color=header_color,
        )

        # 2. Bottom Running Footer
        # Hairline
        p_f1 = pymupdf.Point(left_margin, footer_line_y)
        p_f2 = pymupdf.Point(right_margin, footer_line_y)
        page.draw_line(p_f1, p_f2, color=divider_color, width=0.5)

        # Footer Left Logo + Text
        text_x = left_margin
        if unesa_icon_path.exists():
            if xref_unesa is None:
                xref_unesa = page.insert_image(rect_unesa, filename=str(unesa_icon_path))
            else:
                page.insert_image(rect_unesa, xref=xref_unesa)
            text_x = 73.0

        page.insert_text(
            pymupdf.Point(text_x, footer_text_y),
            footer_left_text,
            fontsize=font_size,
            fontname=font_name,
            color=footer_color,
        )

        # Footer Right Page Number Text
        right_text = f"Halaman {pno + 1} dari {total_pages}"
        text_w = pymupdf.get_text_length(right_text, fontname=font_name, fontsize=font_size)
        page.insert_text(
            pymupdf.Point(right_margin - text_w, footer_text_y),
            right_text,
            fontsize=font_size,
            fontname=font_name,
            color=footer_color,
        )

        stamped_count += 1

    print(f"[postprocess:stamp] Stamped running headers & footers on {stamped_count} pages (Page 2 to {total_pages}).")


def main():
    parser = argparse.ArgumentParser(description="Post-process UTS EDA Report PDF.")
    parser.add_argument("--pdf", type=str, default=str(DEFAULT_PDF), help="Path to input/output PDF")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    if not pdf_path.exists():
        print(f"[postprocess:error] Target PDF not found: {pdf_path}")
        sys.exit(1)

    print(f"[postprocess] Opening PDF: {pdf_path}")
    doc = pymupdf.open(str(pdf_path))
    total_pages = len(doc)
    print(f"[postprocess] Total pages: {total_pages}")

    # 1. Scan headings and set TOC Bookmarks
    toc = scan_headings(doc)
    if toc:
        doc.set_toc(toc)
        print(f"[postprocess:toc] PDF Bookmarks outline set ({len(toc)} entries).")

    # 2. Stamp running headers and footers
    stamp_headers_and_footers(doc)

    # 3. Save optimized PDF
    temp_pdf = pdf_path.with_name(f"{pdf_path.stem}.tmp.pdf")
    print(f"[postprocess] Saving optimized PDF: {temp_pdf}")
    doc.save(str(temp_pdf), garbage=3, deflate=True)
    doc.close()

    # Atomic replace
    temp_pdf.replace(pdf_path)
    file_size_mb = pdf_path.stat().st_size / (1024 * 1024)
    print(f"[postprocess] Successfully updated {pdf_path} ({file_size_mb:.2f} MB, {total_pages} pages).")


if __name__ == "__main__":
    main()
