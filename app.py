from flask import Flask, render_template, request, jsonify, redirect, url_for
from engine import forward_chaining
from knowledge_base import GEJALA

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/diagnosa')
def diagnosa_page():
    return render_template('index.html', gejala=GEJALA)


@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Body harus JSON'}), 400
    gejala_input = data.get('gejala', [])
    jenis_hewan  = data.get('hewan', 'kucing')
    if not isinstance(gejala_input, list):
        return jsonify({'error': "'gejala' harus berupa array"}), 400
    if not isinstance(jenis_hewan, str):
        return jsonify({'error': "'hewan' harus berupa string"}), 400
    hasil = forward_chaining(gejala_input, jenis_hewan)

    return jsonify({
        'hasil'        : hasil,
        'total_gejala' : len(gejala_input),
        'hewan'        : jenis_hewan,
        'ada_diagnosa' : len(hasil) > 0,
    })


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='logo.png'))

@app.route('/gejala_info/<gid>')
def gejala_info(gid):
    return jsonify({
        'id'   : gid,
        'nama' : GEJALA.get(gid, 'Tidak diketahui'),
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
