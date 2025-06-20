from flask import Flask, request, jsonify
from mapa_gerador import gerar_mapa_por_latlng

app = Flask(_name_)

@app.route('/')
def home():
    return 'API de Mapas ativa.'

@app.route('/mapa')
def mapa():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not lat or not lng:
        return jsonify({'erro': 'Latitude e longitude obrigatórias'}), 400

    try:
        mapa_url = gerar_mapa_por_latlng(float(lat), float(lng))
        return jsonify({'url': mapa_url})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True)
