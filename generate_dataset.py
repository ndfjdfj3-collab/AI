import os
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from knowledge_base import GEJALA, PENYAKIT

wb = openpyxl.Workbook()

header_font = Font(name='Calibri', bold=True, size=11, color='FFFFFF')
header_fill = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
header_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
data_font = Font(name='Calibri', size=11)
data_align = Alignment(horizontal='left', vertical='center', wrap_text=True)
center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
thin_border = Border(
    left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin')
)
fill_genap = PatternFill(start_color='D6E4F0', end_color='D6E4F0', fill_type='solid')
fill_ganjil = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
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


# ── Deret kategori dari GEJALA ──
kategori_map = {}
for gid in list(GEJALA.keys())[:4]:
    kategori_map[gid] = 'Umum'
for pid, info in PENYAKIT.items():
    for gid in info['gejala_kunci']:
        kategori_map[gid] = info['nama']

gejala_data = [(k, GEJALA[k], kategori_map.get(k, '-')) for k in GEJALA]

# ── SHEET 1: TABEL GEJALA ──
ws1 = wb.active
ws1.title = 'Tabel Gejala'
apply_header(ws1, ['Kode', 'Nama Gejala', 'Kategori'])
apply_data(ws1, gejala_data, center_cols=[1, 3])
ws1.column_dimensions['A'].width = 10
ws1.column_dimensions['B'].width = 55
ws1.column_dimensions['C'].width = 22

# ── SHEET 2: TABEL RULES ──
ws2 = wb.create_sheet('Tabel Rules')
headers_rules = ['No', 'Kode Rule', 'Kombinasi Gejala', 'Keterangan', 'Bobot Kunci', 'Bobot Umum', 'Min Kunci']
apply_header(ws2, headers_rules)

# Mapping nama penyakit ke info penting
nama_map = {p['nama']: (p['bobot_kunci'], p['bobot_umum'], p['min_kunci']) for p in PENYAKIT.values()}

rules_data = [
    (1,  'R01', 'G05, G06',                                   'Gejala ringan Toxoplasmosis',              4, 1, 2),
    (2,  'R02', 'G05, G06, G07',                               'Gejala sedang Toxoplasmosis',              4, 1, 2),
    (3,  'R03', 'G05, G06, G07, G08, G13',                     'Gejala berat Toxoplasmosis',               4, 1, 2),
    (4,  'R04', 'G08, G09, G10, G11, G12',                     'Gejala sistemik Toxoplasmosis',            4, 1, 2),
    (5,  'R05', 'G01, G02, G03, G05, G06, G13',                'Toxoplasmosis komplit',                    4, 1, 2),
    (6,  'R06', 'G15, G19',                                    'Gejala ringan Rabies',                     5, 1, 2),
    (7,  'R07', 'G15, G16, G17',                               'Gejala sedang Rabies',                     5, 1, 2),
    (8,  'R08', 'G15, G16, G17, G18, G19, G24',                'Gejala berat Rabies',                      5, 1, 2),
    (9,  'R09', 'G17, G18, G22, G23, G24',                     'Rabies stadium lanjut',                    5, 1, 2),
    (10, 'R10', 'G01, G02, G03, G15, G17, G19, G24',           'Rabies komplit',                           5, 1, 2),
    (11, 'R11', 'G05, G06, G15, G17',                          'Campuran Toxoplasmosis + Rabies',          4, 1, 2),
    (12, 'R12', 'G01, G02, G03, G04',                          'Hanya gejala umum',                        0, 0, 0),
]
apply_data(ws2, rules_data, center_cols=[1, 2, 5, 6, 7])
for col, w in [('A', 8), ('B', 14), ('C', 40), ('D', 35), ('E', 14), ('F', 13), ('G', 11)]:
    ws2.column_dimensions[col].width = w

# ── SHEET 3: TABEL DIAGNOSA ──
ws3 = wb.create_sheet('Tabel Diagnosa')
headers_diag = ['No', 'Kode Diagnosa', 'Rule Ref', 'Diagnosis', 'Jenis Hewan', 'Gejala Kunci', 'Gejala Umum']
apply_header(ws3, headers_diag)

diag_data = [
    (1,  'D01', 'R01', 'Toxoplasmosis',              'Kucing, Anjing', 'G05, G06',                    'G01, G02, G03, G04'),
    (2,  'D02', 'R02', 'Toxoplasmosis',              'Kucing, Anjing', 'G05, G06, G07',               'G01, G02, G03, G04'),
    (3,  'D03', 'R03', 'Toxoplasmosis',              'Kucing, Anjing', 'G05, G06, G07, G08, G13',     'G01, G02, G03, G04'),
    (4,  'D04', 'R04', 'Toxoplasmosis',              'Kucing, Anjing', 'G08, G09, G10, G11, G12',     'G01, G02, G03, G04'),
    (5,  'D05', 'R05', 'Toxoplasmosis',              'Kucing, Anjing', 'G05, G06, G13',               'G01, G02, G03'),
    (6,  'D06', 'R06', 'Rabies',                     'Kucing, Anjing', 'G15, G19',                    'G01, G02, G03, G04'),
    (7,  'D07', 'R07', 'Rabies',                     'Kucing, Anjing', 'G15, G16, G17',               'G01, G02, G03, G04'),
    (8,  'D08', 'R08', 'Rabies',                     'Kucing, Anjing', 'G15, G16, G17, G18, G19, G24','G01, G02, G03, G04'),
    (9,  'D09', 'R09', 'Rabies',                     'Kucing, Anjing', 'G17, G18, G22, G23, G24',    'G01, G02, G03, G04'),
    (10, 'D10', 'R10', 'Rabies',                     'Kucing, Anjing', 'G15, G17, G19',               'G01, G02, G03'),
    (11, 'D11', 'R11', 'Toxoplasmosis + Rabies',     'Kucing, Anjing', 'G05, G06, G15, G17',           'G01'),
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

for col, w in [('A', 8), ('B', 16), ('C', 10), ('D', 28), ('E', 18), ('F', 40), ('G', 25)]:
    ws3.column_dimensions[col].width = w

output_path = os.path.join(os.path.dirname(__file__), 'dataset_vetexpert.xlsx')
wb.save(output_path)
print(f'Dataset berhasil dibuat: {output_path}')
