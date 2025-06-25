# mapa_gerador.py
import folium
import requests
import os
import re
from github import Github

# === CONFIGURAÇÕES ===
API_KEY = os.getenv("GOOGLE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "DouglasCNunes48/mapainterativo"
BRANCH = "gh-pages"

# === VALIDAÇÃO INICIAL ===
if not API_KEY:
    raise EnvironmentError("❌ Variável GOOGLE_API_KEY não está definida.")
if not GITHUB_TOKEN:
    raise EnvironmentError("❌ Variável GITHUB_TOKEN não está definida.")
if not REPO_NAME:
    raise EnvironmentError("❌ Variável REPO_NAME não está definida.")

# === FUNÇÕES ===

def buscar_restaurantes(lat, lng, raio):
    try:
        url = (
            f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
            f"location={lat},{lng}&radius={raio}&type=restaurant&key={API_KEY}"
        )
        response = requests.get(url, timeout=10)  # ← timeout evita travamento
        dados = response.json()

        if dados.get("status") != "OK":
            print(f"[ERRO] Google Places retornou erro: {dados.get('status')}")
            return []

        print(f"[INFO] Restaurantes encontrados no raio {raio}m: {len(dados['results'])}")
        return dados['results']

    except Exception as e:
        print(f"[ERRO] buscar_restaurantes: {e}")
        return []

def selecionar_custo_beneficio(restaurantes, ids_excluidos):
    try:
        candidatos = [
            r for r in restaurantes
            if r.get("rating") and r.get("price_level") and r.get("place_id") not in ids_excluidos
        ]

        ordenados = sorted(
            candidatos,
            key=lambda r: (-r["rating"], r["price_level"], -r.get("user_ratings_total", 0))
        )

        print(f"[INFO] Restaurantes custo-benefício selecionados: {len(ordenados[:10])}")
        return ordenados[:10]

    except Exception as e:
        print(f"[ERRO] selecionar_custo_beneficio: {e}")
        return []

def gerar_mapa_html(imovel, lat, lng, melhores, custo_beneficio, nome_arquivo):
    try:
        nome_arquivo = re.sub(r"[^\w\.-]", "_", nome_arquivo)

        mapa = folium.Map(location=[lat, lng], zoom_start=16)
        bounds = [[lat, lng]]

        # Imóvel
        folium.Marker(
            [lat, lng],
            tooltip="Imóvel",
            popup=imovel,
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(mapa)

        # Melhores avaliados
        for r in melhores:
            pos = r["geometry"]["location"]
            folium.Marker(
                [pos["lat"], pos["lng"]],
                tooltip=r["name"],
                popup=f"Melhor Avaliado<br>{r['name']}<br>Nota: {r.get('rating')}",
                icon=folium.Icon(color="red", icon="cutlery", prefix="fa")
            ).add_to(mapa)
            bounds.append([pos["lat"], pos["lng"]])

        # Custo-benefício
        for r in custo_beneficio:
            pos = r["geometry"]["location"]
            folium.Marker(
                [pos["lat"], pos["lng"]],
                tooltip=r["name"],
                popup=f"Custo Benefício<br>{r['name']}<br>Nota: {r.get('rating')}",
                icon=folium.Icon(color="green", icon="cutlery", prefix="fa")
            ).add_to(mapa)
            bounds.append([pos["lat"], pos["lng"]])

        mapa.fit_bounds(bounds)

        legenda_html = """
        <div style="position: fixed; bottom: 50px; left: 50px; background: white;
            border: 1px solid gray; padding: 10px; font-size: 14px; z-index:9999;">
            <b>Legenda</b><br>
            🔵 Imóvel<br>
            🔴 Melhores Avaliados (1km)<br>
            🟢 Custo Benefício (500m)
        </div>
        """
        mapa.get_root().html.add_child(folium.Element(legenda_html))

        mapa.save(nome_arquivo)
        print(f"[INFO] Mapa salvo localmente: {nome_arquivo}")

    except Exception as e:
        print(f"[ERRO] gerar_mapa_html: {e}")
        raise

def publicar_no_github(nome_arquivo):
    try:
        print(f"[INFO] Publicando no GitHub: {nome_arquivo}")
        g = Github(GITHUB_TOKEN)
        repo = g.get_user().get_repo(REPO_NAME)

        with open(nome_arquivo, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            existing = repo.get_contents(nome_arquivo, ref=BRANCH)
            repo.update_file(
                existing.path,
                "Atualização do mapa",
                content,
                existing.sha,
                branch=BRANCH
            )
            print(f"[INFO] Arquivo atualizado no GitHub Pages: {nome_arquivo}")
        except Exception as e:
            print(f"[INFO] Criando novo arquivo: {e}")
            repo.create_file(
                nome_arquivo,
                "Criação do mapa",
                content,
                branch=BRANCH
            )
            print(f"[INFO] Arquivo criado no GitHub Pages: {nome_arquivo}")

        return nome_arquivo

    except Exception as e:
        print(f"[ERRO] publicar_no_github: {e}")
        raise
