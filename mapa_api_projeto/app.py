from fastapi import FastAPI
from pydantic import BaseModel
from mapa_api_projeto import mapa_gerador

app = FastAPI()

class Localizacao(BaseModel):
    imovel: str
    latitude: float
    longitude: float

@app.get("/")
def home():
    return {"mensagem": "API de geração de mapa funcionando."}

@app.post("/gerar-mapa")
def gerar(localizacao: Localizacao):
    lat, lng = localizacao.latitude, localizacao.longitude
    imovel = localizacao.imovel

    restaurantes_1km = mapa_gerador.buscar_restaurantes(lat, lng, 1000)
    melhores = sorted(restaurantes_1km, key=lambda r: (-r.get('rating', 0), -r.get('user_ratings_total', 0)))[:10]
    melhores_ids = {r.get('place_id') for r in melhores}

    restaurantes_500m = mapa_gerador.buscar_restaurantes(lat, lng, 500)
    custo_beneficio = mapa_gerador.selecionar_custo_beneficio(restaurantes_500m, melhores_ids)

    mapa_gerador.gerar_mapa_html(imovel, lat, lng, melhores, custo_beneficio)
    mapa_gerador.publicar_no_github()

    return {
        "mensagem": "Mapa publicado com sucesso!",
        "url": "https://douglascnunes48.github.io/mapainterativo/mapa.html"}
