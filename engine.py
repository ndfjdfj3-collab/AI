from knowledge_base import PENYAKIT


def forward_chaining(gejala_input: list, jenis_hewan: str):
    hasil = []
    fakta = set(gejala_input)

    for pid, penyakit in PENYAKIT.items():
        if jenis_hewan.lower() not in penyakit["hewan"]:
            continue

        gk = set(penyakit["gejala_kunci"])
        gu = set(penyakit["gejala_umum"])

        cocok_kunci = fakta & gk
        cocok_umum  = fakta & gu

        if len(cocok_kunci) < penyakit["min_kunci"]:
            continue

        skor_dapat  = (len(cocok_kunci) * penyakit["bobot_kunci"] +
                       len(cocok_umum)  * penyakit["bobot_umum"])
        skor_maks   = (len(gk) * penyakit["bobot_kunci"] +
                       len(gu) * penyakit["bobot_umum"])
        keyakinan   = round((skor_dapat / skor_maks) * 100, 1) if skor_maks > 0 else 0

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

    hasil.sort(key=lambda x: x["keyakinan"], reverse=True)
    return hasil
