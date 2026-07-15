import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

wb = openpyxl.Workbook()

# ── STYLES ──────────────────────────────────────────────────
header_font = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
header_fill = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)

data_font = Font(name='Calibri', size=11)
data_align = Alignment(horizontal='left', vertical='center', wrap_text=True)
center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)

thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)

# Alternating row fills
fill_genap = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
fill_ganjil = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')

# Diagnosis colors
fill_toxo = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')
fill_rabies = PatternFill(start_color='FCE4EC', end_color='FCE4EC', fill_type='solid')
fill_campuran = PatternFill(start_color='E8F5E9', end_color='E8F5E9', fill_type='solid')
fill_negatif = PatternFill(start_color='F5F5F5', end_color='F5F5F5', fill_type='solid')


def apply_header(ws, headers, row=1):
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border


def apply_data(ws, data, start_row=2, center_cols=None):
    if center_cols is None:
        center_cols = []
    for r, row_data in enumerate(data):
        row_num = start_row + r
        fill = fill_genap if r % 2 == 0 else fill_ganjil
        for c, val in enumerate(row_data, 1):
            cell = ws.cell(row=row_num, column=c, value=val)
            cell.font = data_font
            cell.alignment = center_align if c in center_cols else data_align
            cell.border = thin_border
            cell.fill = fill


# ══════════════════════════════════════════════════════════════
# SHEET 1: TABEL GEJALA
# ══════════════════════════════════════════════════════════════
ws1 = wb.active
ws1.title = 'Tabel Gejala'

headers_gejala = ['Kode', 'Nama Gejala', 'Kategori']
apply_header(ws1, headers_gejala)

gejala_data = [
    ('G01', 'Demam tinggi (suhu tubuh > 39°C)', 'Umum'),
    ('G02', 'Nafsu makan menurun drastis', 'Umum'),
    ('G03', 'Lemas dan tidak aktif bergerak', 'Umum'),
    ('G04', 'Perubahan perilaku yang tidak biasa', 'Umum'),
    ('G05', 'Mata merah atau berair (konjungtivitis)', 'Toxoplasmosis'),
    ('G06', 'Gangguan penglihatan / mata tampak kabur', 'Toxoplasmosis'),
    ('G07', 'Kejang atau tremor (gemetar)', 'Toxoplasmosis'),
    ('G08', 'Diare atau muntah-muntah', 'Toxoplasmosis'),
    ('G09', 'Sesak napas atau napas berat', 'Toxoplasmosis'),
    ('G10', 'Pembengkakan kelenjar getah bening', 'Toxoplasmosis'),
    ('G11', 'Penurunan berat badan drastis', 'Toxoplasmosis'),
    ('G12', 'Icterus / kulit/mata tampak kuning', 'Toxoplasmosis'),
    ('G13', 'Gangguan saraf (berjalan tidak seimbang, berputar-putar)', 'Toxoplasmosis'),
    ('G14', 'Kotoran berbau sangat menyengat', 'Toxoplasmosis'),
    ('G15', 'Agresif tiba-tiba / menyerang tanpa alasan', 'Rabies'),
    ('G16', 'Takut air atau cahaya (hydrophobia / photophobia)', 'Rabies'),
    ('G17', 'Air liur berlebihan / berbusa di mulut', 'Rabies'),
    ('G18', 'Kelumpuhan rahang / sulit menelan', 'Rabies'),
    ('G19', 'Menggigit atau mencakar tanpa provokasi', 'Rabies'),
    ('G20', 'Suara gonggong/meong berubah aneh', 'Rabies'),
    ('G21', 'Bersembunyi di tempat gelap terus-menerus', 'Rabies'),
    ('G22', 'Kelumpuhan anggota tubuh (kaki / tungkai)', 'Rabies'),
    ('G23', 'Disorientasi / terlihat sangat bingung', 'Rabies'),
    ('G24', 'Riwayat gigitan hewan liar / tidak divaksin', 'Rabies'),
]

apply_data(ws1, gejala_data, center_cols=[1, 3])
ws1.column_dimensions['A'].width = 10
ws1.column_dimensions['B'].width = 55
ws1.column_dimensions['C'].width = 18


# ══════════════════════════════════════════════════════════════
# SHEET 2: TABEL RULES (ATURAN)
# ══════════════════════════════════════════════════════════════
ws2 = wb.create_sheet('Tabel Rules')

headers_rules = ['No', 'Kode Rule', 'Kombinasi Gejala', 'Keterangan', 'Bobot Kunci', 'Bobot Umum', 'Min Kunci']
apply_header(ws2, headers_rules)

rules_data = [
    (1,  'R01', 'G05, G06',                                   'Gejala ringan Toxoplasmosis',     4, 1, 2),
    (2,  'R02', 'G05, G06, G07',                               'Gejala sedang Toxoplasmosis',     4, 1, 2),
    (3,  'R03', 'G05, G06, G07, G08, G13',                     'Gejala berat Toxoplasmosis',      4, 1, 2),
    (4,  'R04', 'G08, G09, G10, G11, G12',                     'Gejala sistemik Toxoplasmosis',   4, 1, 2),
    (5,  'R05', 'G01, G02, G03, G05, G06, G13',                'Toxoplasmosis komplit',           4, 1, 2),
    (6,  'R06', 'G15, G19',                                    'Gejala ringan Rabies',            5, 1, 2),
    (7,  'R07', 'G15, G16, G17',                               'Gejala sedang Rabies',            5, 1, 2),
    (8,  'R08', 'G15, G16, G17, G18, G19, G24',                'Gejala berat Rabies',             5, 1, 2),
    (9,  'R09', 'G17, G18, G22, G23, G24',                     'Rabies stadium lanjut',           5, 1, 2),
    (10, 'R10', 'G01, G02, G03, G15, G17, G19, G24',           'Rabies komplit',                  5, 1, 2),
    (11, 'R11', 'G01, G05, G15, G17',                          'Campuran Toxoplasmosis + Rabies', 4, 1, 2),
    (12, 'R12', 'G01, G02, G03, G04',                          'Hanya gejala umum',               0, 0, 0),
]

apply_data(ws2, rules_data, center_cols=[1, 2, 5, 6, 7])
ws2.column_dimensions['A'].width = 8
ws2.column_dimensions['B'].width = 14
ws2.column_dimensions['C'].width = 40
ws2.column_dimensions['D'].width = 35
ws2.column_dimensions['E'].width = 14
ws2.column_dimensions['F'].width = 13
ws2.column_dimensions['G'].width = 11


# ══════════════════════════════════════════════════════════════
# SHEET 3: TABEL DIAGNOSA
# ══════════════════════════════════════════════════════════════
ws3 = wb.create_sheet('Tabel Diagnosa')

headers_diag = ['No', 'Kode Diagnosa', 'Rule Ref', 'Diagnosis', 'Jenis Hewan', 'Gejala Kunci', 'Gejala Umum']
apply_header(ws3, headers_diag)

diag_data = [
    (1,  'D01', 'R01', 'Toxoplasmosis',             'Kucing, Anjing', 'G05, G06',                    'G01, G02, G03, G04'),
    (2,  'D02', 'R02', 'Toxoplasmosis',             'Kucing, Anjing', 'G05, G06, G07',               'G01, G02, G03, G04'),
    (3,  'D03', 'R03', 'Toxoplasmosis',             'Kucing, Anjing', 'G05, G06, G07, G08, G13',     'G01, G02, G03, G04'),
    (4,  'D04', 'R04', 'Toxoplasmosis',             'Kucing, Anjing', 'G08, G09, G10, G11, G12',     'G01, G02, G03, G04'),
    (5,  'D05', 'R05', 'Toxoplasmosis',             'Kucing, Anjing', 'G05, G06, G13',               'G01, G02, G03'),
    (6,  'D06', 'R06', 'Rabies',                    'Kucing, Anjing', 'G15, G19',                    'G01, G02, G03, G04'),
    (7,  'D07', 'R07', 'Rabies',                    'Kucing, Anjing', 'G15, G16, G17',               'G01, G02, G03, G04'),
    (8,  'D08', 'R08', 'Rabies',                    'Kucing, Anjing', 'G15, G16, G17, G18, G19, G24','G01, G02, G03, G04'),
    (9,  'D09', 'R09', 'Rabies',                    'Kucing, Anjing', 'G17, G18, G22, G23, G24',    'G01, G02, G03, G04'),
    (10, 'D10', 'R10', 'Rabies',                    'Kucing, Anjing', 'G15, G17, G19',               'G01, G02, G03'),
    (11, 'D11', 'R11', 'Toxoplasmosis + Rabies',    'Kucing, Anjing', 'G05, G15, G17',               'G01'),
    (12, 'D12', 'R12', 'Tidak Terdiagnosa',          'Kucing, Anjing', '-',                           'G01, G02, G03, G04'),
]

for r, row_data in enumerate(diag_data):
    row_num = r + 2
    diagnosis = row_data[3]
    if 'Toxoplasmosis' in diagnosis and 'Rabies' in diagnosis:
        fill = fill_campuran
    elif 'Toxoplasmosis' in diagnosis:
        fill = fill_toxo
    elif 'Rabies' in diagnosis:
        fill = fill_rabies
    else:
        fill = fill_negatif

    for c, val in enumerate(row_data, 1):
        cell = ws3.cell(row=row_num, column=c, value=val)
        cell.font = data_font
        cell.alignment = center_align if c in [1, 2, 3, 5] else data_align
        cell.border = thin_border
        cell.fill = fill

ws3.column_dimensions['A'].width = 8
ws3.column_dimensions['B'].width = 16
ws3.column_dimensions['C'].width = 10
ws3.column_dimensions['D'].width = 28
ws3.column_dimensions['E'].width = 18
ws3.column_dimensions['F'].width = 40
ws3.column_dimensions['G'].width = 25


# ── SAVE ────────────────────────────────────────────────────
output_path = r'D:\ai\sistem_pakar\dataset_vetexpert.xlsx'
wb.save(output_path)
print(f'Dataset berhasil dibuat: {output_path}')
