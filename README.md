# 🚌 Análise de Transporte Público - São José do Rio Preto/SP

Projeto desenvolvido com o objetivo de **coletar, organizar e relacionar dados do transporte público de São José do Rio Preto - SP**, utilizando técnicas de Web Scraping, processamento de dados e geolocalização.

O projeto realiza a extração automática das informações das linhas de ônibus, coleta dos bairros da cidade e cria uma relação entre bairros atendidos e linhas disponíveis.

---

# 🎯 Objetivo do Projeto

- Automatizar a coleta de dados do transporte público.
- Obter informações completas das linhas de ônibus.
- Identificar quais bairros são atendidos por cada linha.
- Criar uma base estruturada para análises.
- Desenvolver uma visualização dos dados utilizando Power BI.

---

# 🛠️ Tecnologias utilizadas

- Python
- Pandas
- Requests
- BeautifulSoup
- Regex
- OSMnx
- OpenStreetMap
- GeoPandas
- Shapely
- NetworkX
- Power BI

---

# 📌 Etapas do Projeto

## 1. Coleta dos bairros

O script utiliza a biblioteca **OSMnx**, que permite acessar dados geográficos do **OpenStreetMap**, para buscar automaticamente os bairros cadastrados de São José do Rio Preto.

Os dados coletados incluem:

- Nome do bairro;
- Cidade;
- Endereço;
- Latitude;
- Longitude;
- Identificador único do bairro.

Arquivo gerado:

```
bairros_sjrp.csv
```

---

## 2. Web Scraping das linhas de ônibus

O projeto realiza a coleta automática das informações disponíveis no site da **RioPretrans**.

Utilizando `Requests` e `BeautifulSoup`, o código acessa as páginas das linhas e extrai:

- Código da linha;
- Número da linha;
- Nome da linha;
- Plataforma de embarque;
- Tempo médio do percurso;
- Itinerário;
- Dias de funcionamento;
- Horários;
- Percurso completo.

Arquivo gerado:

```
riopretrans_completo.csv
```

---

## 3. Relacionamento entre bairros e linhas

Após coletar os bairros e os percursos das linhas, o código realiza o cruzamento entre essas informações.

O processo utiliza:

- Limpeza e padronização dos textos;
- Remoção de acentos;
- Tratamento de nomes semelhantes;
- Remoção de palavras genéricas como "Jardim", "Vila" e "Parque";
- Busca por correspondência utilizando Expressões Regulares (Regex).

O resultado é uma tabela indicando quais linhas atendem cada bairro.

Arquivo gerado:

```
relacao_bairro_linha.csv
```

---

# 🔄 Fluxo do Projeto

```
OpenStreetMap
      │
      ▼
Coleta dos bairros
      │
      ▼
Arquivo bairros_sjrp.csv


RioPretrans
      │
      ▼
Web Scraping das linhas
      │
      ▼
Arquivo riopretrans_completo.csv


Bairros + Linhas
      │
      ▼
Processamento e relacionamento
      │
      ▼
Arquivo relacao_bairro_linha.csv


      │
      ▼
Power BI
```

---

# 📊 Dashboard Power BI

Os dados processados foram utilizados para criação de um dashboard interativo contendo análises sobre o transporte público.

O dashboard apresenta informações como:

- Quantidade de linhas;
- Distribuição das linhas por bairros;
- Horários de operação;
- Frequência de atendimento;
- Percursos;
- Indicadores das linhas de ônibus.

## Visualização online:

🔗 https://app.powerbi.com/view?r=eyJrIjoiZjMzNTdhOTgtZDJlMS00YjU2LWI5OWUtZjAxNDU4MWM3ZDQwIiwidCI6ImZlODc4N2JjLWM5MTQtNDY2NS04NTQ3LTI2OGUxNWNiMGQ5YSJ9&pageName=a9e015ebc30334300cb9

---

# 📄 Arquivos principais

| Arquivo | Descrição |
|---|---|
| `bairros_sjrp.csv` | Base geográfica dos bairros de São José do Rio Preto |
| `riopretrans_completo.csv` | Dados completos das linhas de ônibus coletadas |
| `relacao_bairro_linha.csv` | Relacionamento entre bairros e linhas de transporte |

---

# 👩‍💻 

Projeto desenvolvido para análise de dados de transporte público, utilizando coleta automatizada de informações, geoprocessamento e Business Intelligence.