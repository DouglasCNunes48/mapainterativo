import folium
import os
import requests

API_KEY = 'AIzaSyCPvECzMlL0etMn7s4X_SVXBRA2c4ypXEE'

def buscar_restaurantes(lat, lng, raio):
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lng}&radius={raio}&type=restaurant&key={API_KEY}"
    )
    res = requests.get(url).json()
    return res.get('results', [])

def selecionar_custo_beneficio(restaurantes, excluidos_ids):
    filtrados = [
        r for r in restaurantes
        if r.get('rating') is not None and r.get('price_level') is not None and r.get('place_id') not in excluidos_ids
    ]
    ordenados = sorted(filtrados, key=lambda x: (-x['rating'], x['price_level'], -x.get('user_ratings_total', 0)))
    return ordenados[:10]

def gerar_mapa_por_latlng(lat, lng):
    restaurantes_1km = buscar_restaurantes(lat, lng, raio=1000)
    melhores = sorted(restaurantes_1km, key=lambda x: (-x.get('rating', 0), -x.get('user_ratings_total', 0)))[:10]
    melhores_ids = {r.get('place_id') for r in melhores}

    restaurantes_500m = buscar_restaurantes(lat, lng, raio=500)
    custo_beneficio = selecionar_custo_beneficio(restaurantes_500m, melhores_ids)

    mapa = folium.Map(location=[lat, lng], zoom_start=16)
    bounds = [[lat, lng]]

    folium.Marker(
        [lat, lng],
        tooltip='Você está aqui',
        icon=folium.Icon(color='blue', icon='home')
    ).add_to(mapa)

    for r in melhores:
        coord = r['geometry']['location']
        folium.Marker(
            [coord['lat'], coord['lng']],
            tooltip=r['name'],
            popup=f"Melhor Avaliado<br>{r['name']}<br>Nota: {r.get('rating')}",
            icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
        ).add_to(mapa)
        bounds.append([coord['lat'], coord['lng']])

    for r in custo_beneficio:
        coord = r['geometry']['location']
        folium.Marker(
            [coord['lat'], coord['lng']],
            tooltip=r['name'],
            popup=f"Custo Benefício<br>{r['name']}<br>Nota: {r.get('rating')}",
            icon=folium.Icon(color='green', icon='cutlery', prefix='fa')
        ).add_to(mapa)
        bounds.append([coord['lat'], coord['lng']])

    mapa.fit_bounds(bounds)

    legenda = """
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; width: 220px; height: 100px; 
        background-color: white; 
        border:2px solid grey; 
        z-index:9999; 
        font-size:14px;
        padding: 10px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
    ">
      <b>Legenda</b><br>
      🔵 Você<br>
      🔴 Melhores Avaliados (1km)<br>
      🟢 Custo Benefício (500m)
    </div>
    """
    mapa.get_root().html.add_child(folium.Element(legenda))

    os.makedirs("static", exist_ok=True)
    filename = f"mapa_{lat}_{lng}.html"
    filepath = os.path.join("static", filename)
    mapa.save(filepath)

    return f"https://mapainterativo-ku2t.onrender.com/static/{filename}"
