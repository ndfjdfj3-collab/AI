# ================================================================
#   BASIS PENGETAHUAN (KNOWLEDGE BASE) - VETEXPERT
#   Sistem Pakar Diagnosa Toxoplasmosis & Rabies
# ================================================================

# ── DAFTAR GEJALA ─────────────────────────────────────────────
GEJALA = {
    # ── GEJALA UMUM (bisa muncul di kedua penyakit) ──
    "G01": "Demam tinggi (suhu tubuh > 39°C)",
    "G02": "Nafsu makan menurun drastis",
    "G03": "Lemas dan tidak aktif bergerak",
    "G04": "Perubahan perilaku yang tidak biasa",

    # ── GEJALA TOXOPLASMOSIS ──
    "G05": "Mata merah atau berair (konjungtivitis)",
    "G06": "Gangguan penglihatan / mata tampak kabur",
    "G07": "Kejang atau tremor (gemetar)",
    "G08": "Diare atau muntah-muntah",
    "G09": "Sesak napas atau napas berat",
    "G10": "Pembengkakan kelenjar getah bening",
    "G11": "Penurunan berat badan drastis",
    "G12": "Icterus / kulit/mata tampak kuning",
    "G13": "Gangguan saraf (berjalan tidak seimbang, berputar-putar)",
    "G14": "Kotoran berbau sangat menyengat",

    # ── GEJALA RABIES ──
    "G15": "Agresif tiba-tiba / menyerang tanpa alasan",
    "G16": "Takut air atau cahaya (hydrophobia / photophobia)",
    "G17": "Air liur berlebihan / berbusa di mulut",
    "G18": "Kelumpuhan rahang / sulit menelan",
    "G19": "Menggigit atau mencakar tanpa provokasi",
    "G20": "Suara gonggong/meong berubah aneh",
    "G21": "Bersembunyi di tempat gelap terus-menerus",
    "G22": "Kelumpuhan anggota tubuh (kaki / tungkai)",
    "G23": "Disorientasi / terlihat sangat bingung",
    "G24": "Riwayat gigitan hewan liar / tidak divaksin",
}

# ── ATURAN PENYAKIT (RULES) ───────────────────────────────────
PENYAKIT = {
    "P01": {
        "nama"      : "Toxoplasmosis",
        "hewan"     : ["kucing", "anjing"],
        "deskripsi" : (
            "Toxoplasmosis adalah penyakit infeksi yang disebabkan oleh parasit "
            "Toxoplasma gondii. Kucing adalah inang definitif utama, sementara anjing "
            "dapat terinfeksi sebagai inang perantara. Parasit ini dapat menular ke manusia "
            "melalui kontak dengan feses hewan yang terinfeksi, sehingga sangat berbahaya "
            "bagi ibu hamil dan penderita imunokompromais."
        ),
        "penanganan": [
            "Segera bawa ke dokter hewan untuk konfirmasi diagnosis (tes darah / feses)",
            "Pemberian antibiotik: Clindamycin atau Trimethoprim-Sulfamethoxazole sesuai resep dokter",
            "Isolasi hewan dari anggota keluarga terutama ibu hamil dan anak kecil",
            "Bersihkan kotak pasir/tempat buang air setiap hari menggunakan sarung tangan",
            "Cuci tangan menyeluruh setelah memegang hewan atau kotorannya",
            "Berikan makanan yang dimasak matang, hindari daging mentah",
            "Pantau kondisi hewan secara rutin setiap minggu",
        ],
        "gejala_kunci": ["G05", "G06", "G07", "G08", "G09", "G10", "G11", "G12", "G13", "G14"],
        "gejala_umum" : ["G01", "G02", "G03", "G04"],
        "bobot_kunci" : 4,   # bobot per gejala kunci
        "bobot_umum"  : 1,   # bobot per gejala umum
        "min_kunci"   : 2,   # minimal gejala kunci untuk terdiagnosa
    },
    "P02": {
        "nama"      : "Rabies",
        "hewan"     : ["kucing", "anjing"],
        "deskripsi" : (
            "Rabies adalah penyakit virus fatal yang menyerang sistem saraf pusat, disebabkan "
            "oleh Lyssavirus. Rabies menular melalui gigitan atau cakaran hewan yang terinfeksi. "
            "Penyakit ini hampir selalu berakibat fatal jika tidak ditangani sebelum gejala muncul. "
            "Rabies termasuk zoonosis berbahaya yang wajib dilaporkan ke otoritas kesehatan hewan."
        ),
        "penanganan": [
            "DARURAT: Segera hubungi dokter hewan atau Dinas Peternakan setempat",
            "Karantina ketat hewan selama minimal 10–14 hari di bawah pengawasan dokter hewan",
            "JANGAN mendekati hewan tanpa alat pelindung (sarung tangan tebal, masker)",
            "Laporkan ke puskesmas / dinas kesehatan jika ada anggota keluarga yang digigit",
            "Korban gigitan harus segera mendapat VAR (Vaksin Anti Rabies) dalam 24 jam",
            "Bersihkan luka gigitan dengan sabun dan air mengalir selama 15 menit",
            "Hewan TIDAK boleh dilepas atau dipindahkan sebelum mendapat izin otoritas",
            "Pastikan vaksinasi rabies hewan dilakukan secara rutin setiap tahun",
        ],
        "gejala_kunci": ["G15", "G16", "G17", "G18", "G19", "G20", "G21", "G22", "G23", "G24"],
        "gejala_umum" : ["G01", "G02", "G03", "G04"],
        "bobot_kunci" : 5,
        "bobot_umum"  : 1,
        "min_kunci"   : 2,
    },
    "P03": {
        "nama"      : "Feline Panleukopenia",
        "hewan"     : ["kucing"],
        "deskripsi" : (
            "Feline Panleukopenia (FP) adalah penyakit virus sangat menular yang disebabkan "
            "oleh Feline Parvovirus. Penyakit ini menyerang sel-sel darah putih dan saluran "
            "pencernaan kucing, dengan angka kematian tinggi terutama pada anak kucing."
        ),
        "penanganan": [
            "Segera bawa ke dokter hewan untuk tes darah (leukopenia parah indikasi kuat FP)",
            "Terapi suportif: infus cairan untuk dehidrasi, elektrolit, dan nutrisi parenteral",
            "Pemberian antibiotik spektrum luas untuk mencegah infeksi sekunder",
            "Isolasi ketat karena virus sangat menular melalui feses, urin, dan fomites",
            "Desinfeksi lingkungan dengan pemutih (bleach) karena virus sangat resisten",
            "Vaksinasi FPV pada semua kucing sehat sebagai pencegahan utama",
            "Karantina minimal 2 minggu untuk kucing baru sebelum diperkenalkan",
        ],
        "gejala_kunci": ["G07", "G08", "G11", "G13", "G14"],
        "gejala_umum" : ["G01", "G02", "G03"],
        "bobot_kunci" : 4,
        "bobot_umum"  : 1,
        "min_kunci"   : 2,
    },
    "P04": {
        "nama"      : "Canine Parvovirus",
        "hewan"     : ["anjing"],
        "deskripsi" : (
            "Canine Parvovirus (CPV) adalah penyakit virus sangat menular yang menyerang "
            "saluran pencernaan anjing, terutama anak anjing usia 6 minggu–6 bulan. "
            "CPV menyebabkan muntah hebat, diare berdarah, dan dehidrasi berat."
        ),
        "penanganan": [
            "DARURAT: Segera bawa ke dokter hewan untuk hospitalisasi",
            "Terapi cairan intravena agresif untuk mengatasi dehidrasi dan syok hipovolemik",
            "Pemberian antiemetik (maropitant) untuk menghentikan muntah",
            "Antibiotik spektrum luas untuk mencegah sepsis bakteri sekunder",
            "Isolasi ketat karena virus sangat menular melalui feses",
            "Desinfeksi lingkungan dengan pemutih atau desinfektan khusus parvovirus",
            "Vaksinasi CPV pada anak anjing mulai usia 6–8 minggu, booster rutin",
        ],
        "gejala_kunci": ["G08", "G09", "G10", "G11", "G22"],
        "gejala_umum" : ["G01", "G02", "G03"],
        "bobot_kunci" : 4,
        "bobot_umum"  : 1,
        "min_kunci"   : 2,
    },
}
