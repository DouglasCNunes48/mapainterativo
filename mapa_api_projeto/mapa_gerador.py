import folium
import os

def gerar_mapa_por_coordenadas(lat, lng):
    lat = float(lat)
    lng = float(lng)
    mapa = folium.Map(location=[lat, lng], zoom_start=16)
    folium.Marker([lat, lng], tooltip='Você está aqui', icon=folium.Icon(color='blue')).add_to(mapa)

    os.makedirs("static", exist_ok=True)
    filename = f"mapa_{lat}_{lng}.html"
    filepath = os.path.join("static", filename)
    mapa.save(filepath)

    return f"https://SEU_APP.onrender.com/static/{filename}"