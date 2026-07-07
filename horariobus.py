# ==================================================
# IMPORTAÇÕES
# ==================================================
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
import urllib3
import re
import time

# ==================================================
# DESATIVAR AVISO SSL
# ==================================================

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================================================
# CRIAR PASTA
# ==================================================

pasta_destino = Path("Projeto_integrador")
pasta_destino.mkdir(parents=True, exist_ok=True)

arquivo_saida = pasta_destino / "riopretrans_completo.csv"

# ==================================================
# CONFIGURAÇÕES
# ==================================================

url_base = "https://www.riopretrans.com.br"
url_horarios = f"{url_base}/horarios"

headers = {"User-Agent": "Mozilla/5.0"}
dados = []

# ==================================================
# DICIONÁRIO DE IDS DAS LINHAS
# ==================================================

ids_linhas = {}
proximo_id = 1

print("\nIniciando coleta...\n")

# ==================================================
# ETAPA 1 - ABRIR SITE
# ==================================================

response = requests.get(url_horarios, headers=headers, verify=False, timeout=30)

if response.status_code != 200:
    print("Erro ao acessar o site")
    exit()

print("Site carregado")

# ==================================================
# ETAPA 2 - PEGAR TODAS AS LINHAS
# ==================================================

soup = BeautifulSoup(response.text, "html.parser")
select = soup.find("select")
links = []

if select:
    options = select.find_all("option")

    for option in options:
        valor = option.get("value")

        if valor:
            links.append(f"{url_base}/horarios/{valor}")

print(f"Linhas encontradas: {len(links)}")

# ==================================================
# ETAPA 3 - COLETAR DADOS
# ==================================================

for indice, link in enumerate(links):

    try:
        print(f"[{indice + 1}/{len(links)}]")

        pagina = requests.get(link, headers=headers, verify=False, timeout=30)

        if pagina.status_code != 200:
            continue

        soup = BeautifulSoup(pagina.text, "html.parser")

        texto = soup.get_text("\n", strip=True)

        linha = ""
        plataforma = ""
        tempo = ""
        percurso = ""

        # ----------------------
        # LINHA
        # ----------------------

        m = re.search(r"LINHA:\s*(.+)",texto)

        if m:linha = m.group(1).strip()

        if linha == "":
            continue

        # ----------------------
        # PLATAFORMA
        # ----------------------

        m = re.search(r"Plataforma de embarque:\s*(.+)",texto)

        if m:plataforma = m.group(1).strip()

        # ----------------------
        # TEMPO MÉDIO
        # ----------------------

        m = re.search(r"Tempo médio do percurso:\s*(.+)",texto)

        if m:tempo = m.group(1).strip()

        # ----------------------
        # PERCURSO
        # ----------------------

        m = re.search(r"Percurso:\s*(.*?)Obs:",texto,re.S)

        if m:percurso = (m.group(1).replace("\n", " ").strip())

        # ----------------------
        # NÚMERO E NOME DA LINHA
        # ----------------------

        numero = linha
        nome = linha

        if "-" in linha:

            partes = linha.split("-", 1)

            numero = partes[0].strip()
            nome = partes[1].strip()

        # ----------------------
        # ID DA LINHA
        # ----------------------

        if numero not in ids_linhas:

            ids_linhas[numero] = f"L{proximo_id:02d}"
            proximo_id += 1

        id_linha = ids_linhas[numero]

        # ----------------------
        # ITINERÁRIOS
        # ----------------------

        itinerarios = re.findall(r"Itinerário\s*(\d+)",texto)

        if not itinerarios:itinerarios = [1]

        # ----------------------
        # TIPOS DE DIA
        # ----------------------

        tipos = {
            "Seg-Sex": r"SEGUNDA A SEXTA(.*?)(SÁBADO|DOMINGOS E FERIADOS|$)",
            "Sabado": r"SÁBADO(.*?)(DOMINGOS E FERIADOS|$)",
            "Domingo": r"DOMINGOS E FERIADOS(.*)"
        }

        # ----------------------
        # HORÁRIOS
        # ----------------------

        for itinerario in itinerarios:
            for tipo, regex in tipos.items():

                m = re.search(regex,texto,re.S)

                if not m:continue

                horarios = re.findall(r"\d{2}:\d{2}",m.group(1))

                for ordem, horario in enumerate(horarios,start=1):

                    dados.append({
                        "id_linha": id_linha,
                        "linha": numero,
                        "nome_linha": nome,
                        "itinerario": itinerario,
                        "plataforma": plataforma,
                        "tempo_medio": tempo,
                        "tipo_dia": tipo,
                        "ordem_horario": ordem,
                        "horario": horario,
                        "percurso": percurso
                    })

        time.sleep(0.3)

    except Exception as erro:

        print(f"Erro ao processar: {link}")
        print(erro)

# ==================================================
# ETAPA 4 - DATAFRAME
# ==================================================

df = pd.DataFrame(dados)

print("\nPrévia:")
print(df.head())

print(f"\nRegistros coletados: {len(df)}")

# ==================================================
# ETAPA 5 - EXPORTAR CSV
# ==================================================

df.to_csv(arquivo_saida,index=False,sep=";",encoding="utf-8-sig")

print("\n========================")
print("CSV GERADO COM SUCESSO")
print("========================")
print(arquivo_saida.resolve())