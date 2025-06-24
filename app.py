# -- coding: utf-8 --
"""
Created on Fri Jun 20 11:33:36 2025

@author: douglas.nunes
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel
import mapa_gerador
from datetime import datetime

app = FastAPI()

class Localizacao(BaseModel):
    imovel: str
    latitude: float
    longitude: float

@app.get("/")
def home():
    return {"mensagem": "API de geração de mapa funcionando."}

@app.post("/gerar_mapa")
def gerar(localizacao: Localizacao):
    nome_arquivo = f"mapa_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    lat, lng = localizacao.latitude, localizacao.longitude
    imovel = localizacao.imovel

    restaurantes_1km = mapa_gerador.buscar_restaurantes(lat, lng, 1000)
    melhores = sorted(restaurantes_1km, key=lambda r: (-r.get('rating', 0), -r.get('user_ratings_total', 0)))[:10]
    melhores_ids = {r.get('place_id') for r in melhores}

    restaurantes_500m = mapa_gerador.buscar_restaurantes(lat, lng, 500)
    custo_beneficio = mapa_gerador.selecionar_custo_beneficio(restaurantes_500m, melhores_ids)

    mapa_gerador.gerar_mapa_html(imovel, lat, lng, melhores, custo_beneficio, nome_arquivo)
    arquivo_publicado = mapa_gerador.publicar_no_github(nome_arquivo)

    return {
        "mensagem": "Mapa publicado com sucesso!",
        "url": f"https://douglascnunes48.github.io/mapainterativo/{arquivo_publicado}"
    }

@app.get("/gerar_mapa")
def gerar_mapa_get(imovel: str = Query(...),
                   latitude: float = Query(...),
                   longitude: float = Query(...)):
    nome_arquivo = f"mapa_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
    lat, lng = latitude, longitude

    restaurantes_1km = mapa_gerador.buscar_restaurantes(lat, lng, 1000)
    melhores = sorted(restaurantes_1km, key=lambda r: (-r.get('rating', 0), -r.get('user_ratings_total', 0)))[:10]
    melhores_ids = {r.get('place_id') for r in melhores}

    restaurantes_500m = mapa_gerador.buscar_restaurantes(lat, lng, 500)
    custo_beneficio = mapa_gerador.selecionar_custo_beneficio(restaurantes_500m, melhores_ids)

    mapa_gerador.gerar_mapa_html(imovel, lat, lng, melhores, custo_beneficio, nome_arquivo)
    arquivo_publicado = mapa_gerador.publicar_no_github(nome_arquivo)

    return {
        "mensagem": "Mapa publicado com sucesso!",
        "url": f"https://douglascnunes48.github.io/mapainterativo/{arquivo_publicado}"}
