from flask import Flask, request, jsonify
from mapa_gerador import gerar_mapa_por_coordenadas

app = Flask(__name__)

@app.route('/')
def home():
    return 'API de Mapas - OK'

@app.route('/mapa')
def mapa():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if not lat or not lng:
        return jsonify({'erro': 'Latitude e longitude obrigatórias'}), 400

    mapa_url = gerar_mapa_por_coordenadas(lat, lng)
    return jsonify({'url': mapa_url})

if __name__ == '__main__':
    app.run(debug=True)