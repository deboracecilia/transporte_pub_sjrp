# ==================================================
# IMPORTAÇÕES
# ==================================================

import osmnx as ox
import pandas as pd
from pathlib import Path

# ==================================================
# DESATIVAR CACHE
# ==================================================

ox.settings.use_cache = False

# ==================================================
# PASTA
# ==================================================

pasta = Path("Projeto_integrador")
pasta.mkdir(parents=True, exist_ok=True)

arquivo_saida = pasta / "bairros_sjrp.csv"

# ==================================================
# CONFIGURAÇÃO
# ==================================================

cidade = "São José do Rio Preto, São Paulo, Brazil"

print("\nBuscando bairros...")

# ==================================================
# BUSCAR BAIRROS
# ==================================================

try:
    bairros = ox.features_from_place(
        cidade,
        tags={"place": ["suburb", "neighbourhood"]}
    )

except Exception as erro:
    print(f"Erro ao buscar bairros: {erro}")
    exit()

# ==================================================
# FILTRAR COLUNAS
# ==================================================

colunas = ["name", "geometry"]
colunas_existentes = [c for c in colunas if c in bairros.columns]

df = bairros[colunas_existentes].copy()

# ==================================================
# RENOMEAR
# ==================================================

df = df.rename(columns={"name": "bairro"})

# ==================================================
# EXTRAIR COORDENADAS
# ==================================================

df["longitude"] = df.geometry.centroid.x
df["latitude"] = df.geometry.centroid.y

# ==================================================
# ADICIONAR CIDADE E ENDEREÇO
# ==================================================

df["cidade"] = "São José do Rio Preto"

df["endereco"] = (
    df["bairro"]
    + ", São José do Rio Preto, SP, Brasil"
)

# ==================================================
# MANTER APENAS AS COLUNAS FINAIS
# ==================================================

df = df[
    [
        "bairro",
        "cidade",
        "endereco",
        "longitude",
        "latitude",
    ]
]

# ==================================================
# LIMPEZA
# ==================================================

df = df.dropna(subset=["bairro"])
df = df.drop_duplicates(subset=["bairro"])
df = df.sort_values(by="bairro")
df = df.reset_index(drop=True)

# ==================================================
# CRIAR ID DOS BAIRROS
# ==================================================

df.insert(
    0,
    "id_bairro",
    [f"B{i:03d}" for i in range(1, len(df) + 1)]
)

# ==================================================
# EXPORTAR CSV
# ==================================================

df.to_csv(
    arquivo_saida,
    sep=";",
    encoding="utf-8-sig",
    index=False
)

# ==================================================
# RESULTADO
# ==================================================

print("\n==============================")
print("CSV GERADO COM SUCESSO")
print("==============================")

print(f"Total de bairros: {len(df)}")
print(f"Arquivo: {arquivo_saida.resolve()}")

print("\nPrévia:")
print(df.head())