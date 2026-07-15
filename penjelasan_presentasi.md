# Penjelasan Presentasi: Sistem Pakar VetExpert

---

## 1. Apa itu VetExpert?

VetExpert adalah **Sistem Pakar Diagnosa Penyakit Hewan** yang menggunakan metode **Forward Chaining** untuk mendiagnosa penyakit **Toxoplasmosis** dan **Rabies** pada kucing dan anjing.

**Tujuan:** Membantu pemilik hewan peliharaan mengenali gejala awal penyakit berbahaya dan mendapatkan saran penanganan sebelum ke dokter hewan.

---

## 2. Metode yang Digunakan: Forward Chaining

**Forward Chaining** (Penalaran Maju) adalah metode inferensi yang dimulai dari **fakta-fakta yang diketahui**, kemudian mencocokkannya dengan **aturan** untuk menarik kesimpulan.

### Analogi Sederhana:
> Bayangkan dokter hewan bertanya: "Apakah hewan Anda demam? Apakah matanya merah?"
> Setiap jawaban "Ya" akan menambah bukti ke arah diagnosis tertentu.
> Ketika bukti cukup kuat, dokter menyimpulkan penyakitnya.

### Langkah Forward Chaining di VetExpert:

| Langkah | Penjelasan | Lokasi di Kode |
|---------|-----------|----------------|
| 1. Input Fakta | User memilih gejala yang dialami hewan | `app.py:88-91` |
| 2. Cocokkan Fakta & Aturan | Sistem membandingkan gejala input dengan aturan penyakit | `app.py:30-35` |
| 3. Hitung Skor | Setiap gejala punya bobot (kunci=4/5, umum=1) | `app.py:42-46` |
| 4. Tentukan Threshold | Keyakinan >= 75% = Sangat Tinggi, dst | `app.py:49-56` |
| 5. Urutkan Hasil | Diagnosis diurutkan dari keyakinan tertinggi | `app.py:73` |

---

## 3. Komponen Sistem (4 Pilar Utama)

### A. Basis Pengetahuan (Knowledge Base)
**File:** `knowledge_base.py`

Berisi data yang menjadi "otak" sistem:
- **24 Gejala** (G01-G24): 4 gejala umum + 10 gejala Toxoplasmosis + 10 gejala Rabies
- **2 Aturan Penyakit** (P01, P02): Setiap penyakit punya gejala kunci, bobot, dan ambang batas

### B. Memori Kerja (Working Memory)
**File:** `app.py:23`

Menyimpan sementara gejala yang dipilih user:
```python
fakta = set(gejala_input)  # Contoh: {"G01", "G05", "G13"}
```

### C. Mesin Inferensi (Inference Engine)
**File:** `app.py:10-74` (fungsi `forward_chaining`)

Logika utama yang menjalankan Forward Chaining:
1. Iterasi setiap penyakit
2. Cek apakah hewan sesuai
3. Cocokkan gejala
4. Hitung persentase keyakinan

### D. Antarmuka Pengguna (UI)
**File:** `templates/index.html` & `templates/home.html`

Halaman web interaktif dengan:
- Form checklist gejala
- Tombol "Diagnosa"
- Tampilan hasil dengan warna berdasarkan tingkat keyakinan

---

## 4. Rumus Perhitungan Skor

```
Skor Didapat = (Jumlah Gejala Kunci Cocok × Bobot Kunci) + (Jumlah Gejala Umum Cocok × Bobot Umum)

Skor Maksimal = (Total Gejala Kunci × Bobot Kunci) + (Total Gejala Umum × Bobot Umum)

Keyakinan (%) = (Skor Didapat / Skor Maksimal) × 100%
```

### Contoh Perhitungan:
**Kucing dengan gejala:** G01, G03, G05, G06, G13

**Untuk Toxoplasmosis (P01):**
- Gejala Kunci Cocok: G05, G06, G13 → 3 gejala × bobot 4 = **12**
- Gejala Umum Cocok: G01, G03 → 2 gejala × bobot 1 = **2**
- Skor Didapat = 12 + 2 = **14**
- Skor Maksimal = (10 × 4) + (4 × 1) = **44**
- Keyakinan = (14/44) × 100% = **31.8%** → Tingkat: **Sedang**

---

## 5. Visualisasi Alur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ Pilih Hewan  │ →  │ Pilih Gejala│ →  │  Klik       │ │
│  │ (Kucing/     │    │ (Checklist) │    │  Diagnosa   │ │
│  │  Anjing)     │    │             │    │             │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
└──────────────────────────┬──────────────────────────────┘
                           │ JSON API
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  FLASK BACKEND                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │         FORWARD CHAINING ENGINE                 │   │
│  │  ┌─────────────┐                                │   │
│  │  │ Fakta Input  │ ──┐                           │   │
│  │  └─────────────┘   │                           │   │
│  │                    ▼                           │   │
│  │  ┌─────────────────────────────────────┐       │   │
│  │  │  Cocokkan dengan Aturan Penyakit    │       │   │
│  │  │  • Toxoplasmosis (P01)              │       │   │
│  │  │  • Rabies (P02)                     │       │   │
│  │  └─────────────────────────────────────┘       │   │
│  │                    │                           │   │
│  │                    ▼                           │   │
│  │  ┌─────────────────────────────────────┐       │   │
│  │  │  Hitung Persentase Keyakinan        │       │   │
│  │  └─────────────────────────────────────┘       │   │
│  └─────────────────────────────────────────────────┘   │
│                           │                            │
└───────────────────────────┼────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    HASIL DIAGNOSA                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │  Toxoplasmosis: 31.8% (Sedang)  🟡             │   │
│  │  Rabies: 0% (Tidak Terdiagnosa)                 │   │
│  │                                                  │   │
│  │  Gejala Cocok: G01, G03, G05, G06, G13          │   │
│  │  Saran Penanganan: Segera ke dokter hewan...    │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 6. Keunggulan Sistem

| Aspek | Penjelasan |
|-------|-----------|
| **Modular** | Basis pengetahuan terpisah dari logika (knowledge_base.py vs app.py) |
| **Scalable** | Mudah menambah penyakit baru tinggal tambah di PENYAKIT dict |
| **Interaktif** | UI web responsif dengan hasil visual berwarna |
| **Akademis** | Menggunakan metode Forward Chaining yang diakui dalam AI |

---

## 7. Struktur File Proyek

```
sistem_pakar/
├── app.py                 ← Backend Flask + Forward Chaining Engine
├── knowledge_base.py      ← Basis Pengetahuan (Gejala & Aturan)
├── implementation_plan.md ← Rencana Pengembangan
├── penjelasan_presentasi.md ← Dokumen ini
├── requirements.txt       ← Dependensi Python
└── templates/
    ├── home.html          ← Halaman Beranda
    └── index.html         ← Halaman Diagnosa Utama
```

---

## 8. Cara Menjalankan

```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app.py

# Buka browser
http://localhost:5000
```

---

## 9. Kata Kunci untuk Presentasi

Saat presentasi, gunakan istilah berikut:
- **Forward Chaining**: Penalaran maju dari fakta ke kesimpulan
- **Knowledge Base**: Basis pengetahuan berisi gejala dan aturan
- **Working Memory**: Memori kerja menyimpan input user
- **Inference Engine**: Mesin inferensi menjalankan logika
- **Threshold**: Ambang batas untuk menentukan tingkat keyakinan
- **Bobot (Weight)**: Nilai kepentingan setiap gejala
- **Zoonosis**: Penyakit yang dapat menular dari hewan ke manusia
