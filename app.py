from fastapi import FastAPI, Query, HTTPException
import mapa_gerador
from datetime import datetime

app = FastAPI()

@app.get("/gerar_mapa")
def gerar_get(imovel: str = Query(...), latitude: float = Query(...), longitude: float = Query(...)):
    try:
        nome_arquivo = f"mapa_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"
        print(f"[INFO] GET recebido: imovel={imovel}, latitude={latitude}, longitude={longitude}")
        
        restaurantes_1km = mapa_gerador.buscar_restaurantes(latitude, longitude, 1000)
        melhores = sorted(restaurantes_1km, key=lambda r: (-r.get("rating", 0), -r.get("user_ratings_total", 0)))[:10]
        melhores_ids = {r.get("place_id") for r in melhores}

        restaurantes_500m = mapa_gerador.buscar_restaurantes(latitude, longitude, 500)
        custo_beneficio = mapa_gerador.selecionar_custo_beneficio(restaurantes_500m, melhores_ids)

        mapa_gerador.gerar_mapa_html(imovel, latitude, longitude, melhores, custo_beneficio, nome_arquivo)
        arquivo_publicado = mapa_gerador.publicar_no_github(nome_arquivo)

        return {
            "mensagem": "Mapa publicado com sucesso!",
            "url": f"https://douglascnunes48.github.io/mapainterativo/{arquivo_publicado}"
        }

    except Exception as e:
        print(f"[ERRO] Erro no GET /gerar_mapa: {e}")
        raise HTTPException(status_code=500, detail="Erro ao gerar e publicar o mapa.")
