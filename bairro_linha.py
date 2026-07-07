import pandas as pd
from pathlib import Path
import unicodedata
import re

# ==================================================
# FUNÇÃO PARA LIMPAR TEXTO
# ==================================================

def limpar_texto(texto):
    texto = str(texto).upper().strip()

    # remover acentos
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )

    # remover espaços duplicados
    texto = " ".join(texto.split())

    return texto


# ==================================================
# CAMINHOS
# ==================================================

base = Path(__file__).parent
pasta = base / "Projeto_integrador"

arquivo_linhas = pasta / "riopretrans_completo.csv"
arquivo_bairros = pasta / "bairros_sjrp.csv"
arquivo_saida = pasta / "relacao_bairro_linha.csv"

# ==================================================
# LER CSVs
# ==================================================

df_linhas = pd.read_csv(
    arquivo_linhas,
    sep=";",
    encoding="utf-8-sig"
)

df_bairros = pd.read_csv(
    arquivo_bairros,
    sep=";",
    encoding="utf-8-sig"
)

# ==================================================
# LIMPAR NOMES DAS COLUNAS
# ==================================================

df_linhas.columns = df_linhas.columns.str.strip().str.lower()
df_bairros.columns = df_bairros.columns.str.strip().str.lower()

print("Colunas linhas:", list(df_linhas.columns))
print("Colunas bairros:", list(df_bairros.columns))

# ==================================================
# VALIDAR COLUNAS
# ==================================================

colunas_linhas = {"id_linha", "percurso"}
colunas_bairros = {"id_bairro", "bairro"}

if not colunas_linhas.issubset(df_linhas.columns):
    raise Exception(
        f"CSV de linhas precisa conter: {colunas_linhas}"
    )

if not colunas_bairros.issubset(df_bairros.columns):
    raise Exception(
        f"CSV de bairros precisa conter: {colunas_bairros}"
    )

# ==================================================
# LIMPAR PERCURSO
# ==================================================

df_linhas["percurso"] = df_linhas["percurso"].fillna("")
df_linhas["percurso_limpo"] = df_linhas["percurso"].apply(limpar_texto)

# ==================================================
# PALAVRAS IGNORADAS
# ==================================================

ignorar = {
    "JARDIM",
    "JD",
    "VILA",
    "PQ",
    "PARQUE",
    "RESIDENCIAL",
    "CONJUNTO",
    "LOTEAMENTO",
    "SETOR",
    "DISTRITO",
    "CHACARA",
    "CHÁCARA"
}

# ==================================================
# PROCESSAMENTO
# ==================================================

resultado = set()

total = len(df_linhas)

for i, linha in enumerate(df_linhas.itertuples(index=False), start=1):

    print(f"[{i}/{total}] Linha {linha.id_linha}")

    percurso = linha.percurso_limpo

    for bairro in df_bairros.itertuples(index=False):

        nome_bairro = limpar_texto(bairro.bairro)

        palavras = [
            p
            for p in nome_bairro.split()
            if p not in ignorar and len(p) > 2
        ]

        if not palavras:
            continue

        encontrou = all(
            re.search(rf"\b{re.escape(p)}\b", percurso)
            for p in palavras
        )

        if encontrou:
            resultado.add(
                (
                    bairro.id_bairro,
                    linha.id_linha
                )
            )

# ==================================================
# DATAFRAME FINAL
# ==================================================

df_relacao = pd.DataFrame(
    list(resultado),
    columns=[
        "id_bairro",
        "id_linha"
    ]
)

df_relacao = df_relacao.sort_values(
    by=[
        "id_bairro",
        "id_linha"
    ]
).reset_index(drop=True)

# ==================================================
# EXPORTAR
# ==================================================

df_relacao.to_csv(
    arquivo_saida,
    sep=";",
    encoding="utf-8-sig",
    index=False
)

# ==================================================
# RESULTADO
# ==================================================

print("\n==============================")
print("RELAÇÃO CRIADA COM SUCESSO")
print("==============================")
print(f"Total de relações: {len(df_relacao)}")

print("\nPrimeiras relações:")
print(df_relacao.head(20))