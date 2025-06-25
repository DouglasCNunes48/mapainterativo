# app.py
from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
import mapa_gerador

app = FastAPI()

@app.get("/gerar_mapa")
def gerar_mapa(
    imovel: str = Query(..., description="Nome do imóvel"),
    latitude: float = Query(..., description="Latitude do local"),
    longitude: float = Query(..., description="Longitude do local")
):
    try:
        # Nome único para o arquivo HTML
        nome_arquivo = f"mapa_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
        print(f"[INFO] Requisição recebida - Imóvel: {imovel}, Latitude: {latitude}, Longitude: {longitude}")

        # Etapa 1: Restaurantes mais bem avaliados (raio 1km)
        melhores_1km = mapa_gerador.buscar_restaurantes(latitude, longitude, 1000)
        melhores = sorted(
            melhores_1km,
            key=lambda r: (-r.get("rating", 0), -r.get("user_ratings_total", 0))
        )[:10]
        melhores_ids = {r.get("place_id") for r in melhores}

        # Etapa 2: Restaurantes com melhor custo-benefício (raio 500m)
        todos_500m = mapa_gerador.buscar_restaurantes(latitude, longitude, 500)
        custo_beneficio = mapa_gerador.selecionar_custo_beneficio(todos_500m, melhores_ids)

        # Etapa 3: Gerar HTML e publicar no GitHub
        mapa_gerador.gerar_mapa_html(imovel, latitude, longitude, melhores, custo_beneficio, nome_arquivo)
        mapa_publicado = mapa_gerador.publicar_no_github(nome_arquivo)

        return {
            "mensagem": "Mapa publicado com sucesso!",
            "url": f"https://douglascnunes48.github.io/mapainterativo/{mapa_publicado}"
        }

    except Exception as e:
        print(f"[ERRO] Erro ao gerar mapa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar ou publicar o mapa.")
