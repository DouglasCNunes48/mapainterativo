# -- coding: utf-8 --
"""
Atualizado para debug em 25/06/2025
@author: douglas.nunes
"""

import folium
import requests
import os
from github import Github


API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "DouglasCNunes48/mapainterativo"
BRANCH = "gh-pages"

def buscar_restaurantes(lat, lng, raio):
    url = (
        f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        f"location={lat},{lng}&radius={raio}&type=restaurant&key={API_KEY}"
    )
    print(f"[DEBUG] Requisição Google Places: {url}")
    try:
        res = requests.get(url)
        data = res.json()
        print("[DEBUG] Resposta da API Google Places recebida com sucesso.")
        return data.get('results', [])
    except Exception as e:
        print(f"[ERRO] Falha ao buscar restaurantes: {e}")
        return []

def selecionar_custo_beneficio(restaurantes, excluidos_ids):
    print("[DEBUG] Filtrando restaurantes custo-benefício...")
    try:
        filtrados = [
            r for r in restaurantes
            if r.get('rating') and r.get('price_level') and r.get('place_id') not in excluidos_ids
        ]
        ordenados = sorted(
            filtrados,
            key=lambda x: (-x['rating'], x['price_level'], -x.get('user_ratings_total', 0))
        )
        return ordenados[:10]
    except Exception as e:
        print(f"[ERRO] Erro ao filtrar custo-benefício: {e}")
        return []

def gerar_mapa_html(imovel, lat, lng, melhores, custo_beneficio, nome_arquivo):
    print(f"[DEBUG] Gerando mapa HTML: {nome_arquivo}")
    try:
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

        mapa.save(nome_arquivo)
        print(f"[DEBUG] Mapa salvo em {nome_arquivo}")
    except Exception as e:
        print(f"[ERRO] Erro ao gerar mapa: {e}")
        raise

def publicar_no_github(nome_arquivo):
    print(f"[DEBUG] Publicando no GitHub: {nome_arquivo}")
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(REPO_NAME)

        with open(nome_arquivo, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            existing = repo.get_contents(nome_arquivo, ref=BRANCH)
            repo.update_file(existing.path, "Atualização do mapa", content, existing.sha, branch=BRANCH)
            print("[DEBUG] Arquivo atualizado no GitHub.")
        except Exception as e:
            print(f"[DEBUG] Arquivo não encontrado para update. Criando novo. Detalhes: {e}")
            repo.create_file(nome_arquivo, "Criação do mapa", content, branch=BRANCH)
            print("[DEBUG] Arquivo criado no GitHub.")
        
        return nome_arquivo
    except Exception as e:
        print(f"[ERRO] Erro ao publicar no GitHub: {e}")
        raise
