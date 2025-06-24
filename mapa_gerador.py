# -- coding: utf-8 --
"""
Created on Tue Jun 24 09:25:08 2025

@author: douglas.nunes
"""

import folium
import requests
import os
from github import Github
from datetime import datetime

API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "DouglasCNunes48/mapainterativo"
BRANCH = "gh-pages"

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
        if r.get('rating') and r.get('price_level') and r.get('place_id') not in excluidos_ids
    ]
    ordenados = sorted(
        filtrados,
        key=lambda x: (-x['rating'], x['price_level'], -x.get('user_ratings_total', 0))
    )
    return ordenados[:10]

def gerar_mapa_html(imovel, lat, lng, melhores, custo_beneficio, nome_arquivo):
    mapa = folium.Map(location=[lat, lng], zoom_start=16)
    bounds = [[lat, lng]]
    
    folium.Marker([lat, lng], tooltip='Imóvel', popup=imovel,
                  icon=folium.Icon(color='blue', icon='home')).add_to(mapa)

    for r in melhores:
        pos = r['geometry']['location']
        folium.Marker([pos['lat'], pos['lng']],
                      tooltip=r['name'],
                      popup=f"Melhor Avaliado<br>{r['name']}<br>Nota: {r.get('rating')}",
                      icon=folium.Icon(color='red', icon='cutlery', prefix='fa')).add_to(mapa)
        bounds.append([pos['lat'], pos['lng']])

    for r in custo_beneficio:
        pos = r['geometry']['location']
        folium.Marker([pos['lat'], pos['lng']],
                      tooltip=r['name'],
                      popup=f"Custo Benefício<br>{r['name']}<br>Nota: {r.get('rating')}",
                      icon=folium.Icon(color='green', icon='cutlery', prefix='fa')).add_to(mapa)
        bounds.append([pos['lat'], pos['lng']])

    mapa.fit_bounds(bounds)
    mapa.get_root().html.add_child(folium.Element("""
    <div style="position: fixed; bottom: 50px; left: 50px; background: white; 
        border:1px solid gray; padding: 10px; font-size: 14px; z-index:9999;">
        <b>Legenda</b><br>🔵 Imóvel<br>🔴 Melhores Avaliados (1km)<br>🟢 Custo Benefício (500m)
    </div>
    """))

    # ✅ Agora salvando com o nome_arquivo corretamente
    mapa.save(nome_arquivo)

def publicar_no_github(nome_arquivo):
    g = Github(GITHUB_TOKEN)
    repo = g.get_user().get_repo(REPO_NAME)

    with open(nome_arquivo, "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        existing = repo.get_contents(nome_arquivo, ref=BRANCH)
        repo.update_file(existing.path, "Atualização do mapa", content, existing.sha, branch=BRANCH)
    except:
        repo.create_file(nome_arquivo, "Criação do mapa", content, branch=BRANCH)
    
    return nome_arquivo

