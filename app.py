# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from knowledge_base import GEJALA, PENYAKIT

# ── FORWARD CHAINING ENGINE ───────────────────────────────────

def forward_chaining(gejala_input: list, jenis_hewan: str):
    """
    Mesin inferensi Forward Chaining.

    Alur:
    1. Fakta awal = gejala yang dicentang user
    2. Cocokkan fakta dengan setiap aturan penyakit
    3. Hitung skor & persentase keyakinan
    4. Tentukan diagnosis berdasarkan threshold

    Returns: list hasil diagnosis (terurut dari keyakinan tertinggi)
    """
    hasil = []
    fakta = set(gejala_input)

    for pid, penyakit in PENYAKIT.items():
        # Cek apakah penyakit relevan untuk jenis hewan ini
        if jenis_hewan.lower() not in penyakit["hewan"]:
            continue

        gk = set(penyakit["gejala_kunci"])
        gu = set(penyakit["gejala_umum"])

        # Gejala yang cocok
        cocok_kunci = fakta & gk
        cocok_umum  = fakta & gu

        # Tidak memenuhi syarat minimum
        if len(cocok_kunci) < penyakit["min_kunci"]:
            continue

        # Hitung skor
        skor_dapat  = (len(cocok_kunci) * penyakit["bobot_kunci"] +
                       len(cocok_umum)  * penyakit["bobot_umum"])
        skor_maks   = (len(gk) * penyakit["bobot_kunci"] +
                       len(gu) * penyakit["bobot_umum"])
        keyakinan   = round((skor_dapat / skor_maks) * 100, 1) if skor_maks > 0 else 0

        # Tentukan tingkat
        if keyakinan >= 75:
            tingkat, warna = "Sangat Tinggi", "#dc2626"
        elif keyakinan >= 50:
            tingkat, warna = "Tinggi",         "#f97316"
        elif keyakinan >= 30:
            tingkat, warna = "Sedang",          "#eab308"
        else:
            tingkat, warna = "Rendah",          "#84cc16"

        hasil.append({
            "id"            : pid,
            "nama"          : penyakit["nama"],
            "deskripsi"     : penyakit["deskripsi"],
            "penanganan"    : penyakit["penanganan"],
            "keyakinan"     : keyakinan,
            "tingkat"       : tingkat,
            "warna"         : warna,
            "gejala_cocok"  : sorted(list(cocok_kunci | cocok_umum)),
            "gejala_tidak"  : sorted(list((gk | gu) - fakta)),
            "jumlah_cocok"  : len(cocok_kunci) + len(cocok_umum),
            "jumlah_kunci"  : len(cocok_kunci),
        })

    # Urutkan berdasarkan keyakinan tertinggi
    hasil.sort(key=lambda x: x["keyakinan"], reverse=True)
    return hasil


# ── ROUTES ────────────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/diagnosa')
def diagnosa_page():
    return render_template('index.html', gejala=GEJALA)

@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    data         = request.get_json()
    gejala_input = data.get('gejala', [])
    jenis_hewan  = data.get('hewan', 'kucing')
    hasil        = forward_chaining(gejala_input, jenis_hewan)

    return jsonify({
        'hasil'        : hasil,
        'total_gejala' : len(gejala_input),
        'hewan'        : jenis_hewan,
        'ada_diagnosa' : len(hasil) > 0,
    })

@app.route('/gejala_info/<gid>')
def gejala_info(gid):
    return jsonify({
        'id'   : gid,
        'nama' : GEJALA.get(gid, 'Tidak diketahui'),
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
