from dotenv import load_dotenv
import logging
import os
import os
import pandas as pd
import requests
import sys

pasta_dados = os.path.join("data", "privado") 
arquivo_csv = os.path.join(pasta_dados, "investimentos_marica_2025.csv")
os.makedirs(pasta_dados, exist_ok=True) # Cria a pasta de dados, se não existir

logging.basicConfig(
    filename=os.path.join("logs", "consumir_api.log"),
    level=logging.INFO, # Define o nível de log para INFO, pode ser WARNING, ERROR, etc.
    format="%(asctime)s - %(levelname)s - %(message)s"
)

url = "https://apicadprev.trabalho.gov.br/DAIR_CARTEIRA"

load_dotenv()

parametros = {
    'nr_cnpj_entidade': os.getenv("CNPJ_ENTIDADE"),
    'sg_uf': os.getenv("UF_ENTIDADE"),
    'dt_ano': os.getenv("ANO_CONSULTA")
}

logging.info("Iniciando execucao do script de investimentos")
logging.info(f"Consultando API com parametros: {parametros}")

# Garantir que a requisição seja feita com tratamento de erros
try:
    response = requests.get(url, timeout=60, params=parametros, verify=True)
    response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins
except requests.exceptions.Timeout:
    logging.error("Timeout na requisicao da API")
    sys.exit(1)
except requests.exceptions.RequestException as e:
    logging.error(f"Erro na conexao: {e}")
    sys.exit(1)
except Exception as e:
    logging.exception(f"Erro inesperado: {e}")
    sys.exit(1)

#-----------------código do pandas-----------------
if response.ok:
    logging.info(f"Requisicao bem-sucedida: Status {response.status_code}") # Log de sucesso
    data = response.json()["data"]

    mapa_meses = {1: '1° Bimestre', 2: '2° Bimestre', 3: '3° Bimestre', 4: '4° Bimestre', 5: '5° Bimestre', 6: '6° Bimestre'} # Mapeamento dos meses por bimestre

    df = pd.DataFrame(data)
    
    df['vl_total_atual'] = df['vl_total_atual'].astype(float) # Converte para float
    
    if df['vl_total_atual'].min() < 0:
        logging.warning("Valor negativo encontrado em 'vl_atual_ativo'") # Log de aviso para valores negativos
    
    if "apicadprev.trabalho.gov.br" not in response.url:
        logging.warning(f"URL inesperada na resposta da API: {response.url}") # Log de aviso para URL inesperada

    vl_total_por_mes = df.groupby('dt_mes_bimestre')['vl_total_atual'].sum() # Agrupa por mês/bimestre e soma os valores

    vl_total_por_mes = vl_total_por_mes.rename(mapa_meses) # Renomeia os índices para nomes dos meses

    vl_total_por_mes = vl_total_por_mes.round(2) # Arredonda para 2 casas decimais

    vl_total_por_mes.to_csv(arquivo_csv) # Salva o resumo em CSV

    print(f"Arquivo '{arquivo_csv}' salvo com sucesso!")
    print("\nResumo dos totais por mês:")
    print(vl_total_por_mes)

    # df.to_excel("rafael.xlsx")
    # df.head()
    # df.info()

else:
    logging.error(f"Falha na requisicao: Status {response.status_code} - {response.text}") # Log de erro com detalhes da resposta
    

