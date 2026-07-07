import pandas as pd
from pathlib import Path

PASTA_ENTRADA = Path(
    r"ref"
)

PASTA_SAIDA = Path("Projeto_integrador")
PASTA_SAIDA.mkdir(exist_ok=True)

arquivo_excel = PASTA_SAIDA / "censo_transportes.xlsx"

arquivos = list(PASTA_ENTRADA.glob("*.csv"))

with pd.ExcelWriter(arquivo_excel,engine="openpyxl") as writer:

    for arquivo in arquivos:

        try:
            df = pd.read_csv(arquivo, sep=";", encoding="utf-8")
        except:
            df = pd.read_csv(arquivo,sep=";",encoding="latin1")

        nome_aba = arquivo.stem[:31]
        nome_aba = (nome_aba.replace("Censo 2022 - ", "").replace("-", "_"))

        df.to_excel(writer,sheet_name=nome_aba,index=False)

print(f"Arquivo salvo em:\n{arquivo_excel}")