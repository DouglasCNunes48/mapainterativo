# app.py
from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
import mapa_gerador

app = FastAPI(
    title="API Geradora de Mapas Interativos",
    description="Gera mapas com os melhores restaurantes e opções de custo-benefício próximos a um imóvel.",
    version="1.0.0"
)

@app.get("/gerar_mapa", summary="Gera o mapa interativo e publica no GitHub Pages")
def gerar_mapa(
    imovel: str = Query(..., description="Nome do imóvel (ex: Infinity Tower)"),
    latitude: float = Query(..., description="Latitude do local"),
    longitude: float = Query(..., description="Longitude do local")
):
    """
    Gera um mapa com restaurantes mais bem avaliados e com melhor custo-benefício
    nos arredores de um imóvel e publica o HTML no GitHub Pages.
    """
    try:
        nome_arquivo = f"mapa_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
        print(f"[INFO] Requisição recebida: imovel={imovel}, lat={latitude}, lng={longitude}")

        # Restaurantes mais bem avaliados (1km)
        melhores_1km = mapa_gerador.buscar_restaurantes(latitude, longitude, 1000)
        melhores = sorted(
            melhores_1km,
            key=lambda r: (-r.get("rating", 0), -r.get("user_ratings_total", 0))
        )[:10]
        melhores_ids = {r.get("place_id") for r in melhores}

        # Restaurantes com bom custo-benefício (500m)
        todos_500m = mapa_gerador.buscar_restaurantes(latitude, longitude, 500)
        custo_beneficio = mapa_gerador.selecionar_custo_beneficio(todos_500m, melhores_ids)

        # Geração e publicação
        mapa_gerador.gerar_mapa_html(imovel, latitude, longitude, melhores, custo_beneficio, nome_arquivo)
        url_publicada = mapa_gerador.publicar_no_github(nome_arquivo)

        return {
            "mensagem": "Mapa publicado com sucesso!",
            "url": f"https://douglascnunes48.github.io/mapainterativo/{url_publicada}"
        }

    except Exception as e:
        print(f"[ERRO] Erro ao gerar mapa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao gerar ou publicar o mapa.")
