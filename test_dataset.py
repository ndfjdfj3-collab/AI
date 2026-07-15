import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import openpyxl
from engine import forward_chaining

EXCEL_PATH = os.path.join(os.path.dirname(__file__), 'dataset_vetexpert.xlsx')

def parse_gejala(text):
    return [g.strip() for g in text.split(',') if g.strip()] if text else []

def test_all():
    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb['Tabel Diagnosa']

    total = 0
    passed = 0
    failed = []

    for row in ws.iter_rows(min_row=2, values_only=True):
        no, kode, rule_ref, diagnosis, hewan, gejala_kunci, gejala_umum = row
        total += 1

        gejala_input = parse_gejala(gejala_kunci) + parse_gejala(gejala_umum)

        # Excel has "Kucing, Anjing" - test with first animal type
        hewan_test = hewan.split(',')[0].strip().lower()

        hasil = forward_chaining(gejala_input, hewan_test)

        detected = {h['nama']: h['keyakinan'] for h in hasil}

        print(f"\n{'='*60}")
        print(f"Kasus #{no} ({kode}): {diagnosis}")
        print(f"  Hewan     : {hewan}")
        print(f"  Gejala    : {', '.join(gejala_input)}")
        print(f"  Detected  : {detected if detected else 'Tidak Ada'}")
        print(f"  Expected  : {diagnosis}")

        status = 'OK'
        if diagnosis == 'Tidak Terdiagnosa':
            if not detected:
                status = 'OK'
                passed += 1
            else:
                status = 'FAIL'
                failed.append((no, diagnosis, detected))
        elif diagnosis == 'Toxoplasmosis + Rabies':
            if 'Toxoplasmosis' in detected and 'Rabies' in detected and detected['Toxoplasmosis'] > 0 and detected['Rabies'] > 0:
                status = 'OK'
                passed += 1
            else:
                status = 'FAIL'
                failed.append((no, diagnosis, detected))
        else:
            if diagnosis in detected and detected[diagnosis] > 0:
                status = 'OK'
                passed += 1
            else:
                status = 'FAIL'
                failed.append((no, diagnosis, detected))

        print(f"  Status    : {status}")

    print(f"\n{'='*60}")
    print(f"HASIL: {passed}/{total} lulus")
    if failed:
        print(f"\nGAGAL ({len(failed)}):")
        for no, expected, got in failed:
            print(f"  #{no}: expected '{expected}', got {got}")
    else:
        print("Semua test lulus! OK")
    print(f"{'='*60}")

    return passed == total

if __name__ == '__main__':
    success = test_all()
    sys.exit(0 if success else 1)
