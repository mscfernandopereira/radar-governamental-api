from dotenv import load_dotenv
import logging
import os
import sys

# 1. IMPORTAÇÕES SIMPLIFICADAS
from api import consumir_api_previdencia_marica
from processing import tratar_dados_bruto, vl_total_por_mes, salvar_resumo_em_csv

#----------------Configurações iniciais-----------------
pasta_dados = os.path.join("data", "privado")
arquivo_mes = os.path.join(pasta_dados, "investimentos_marica_2025_por_mes.csv") 
os.makedirs(pasta_dados, exist_ok=True)

logging.basicConfig(
    filename=os.path.join("logs", "consumir_api.log"),
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

url = "https://apicadprev.trabalho.gov.br/DAIR_CARTEIRA"

load_dotenv() 

parametros = {
    'nr_cnpj_entidade': os.getenv("CNPJ_ENTIDADE"),
    'sg_uf': os.getenv("UF_ENTIDADE"),
    'dt_ano': os.getenv("ANO_CONSULTA")
}

#----------------Início da execução do script-----------------
logging.info("Iniciando execucao do script de investimentos (versao simplificada)")
logging.info(f"Consultando API com parametros: {parametros}")

response = consumir_api_previdencia_marica(url, parametros)

if response and response.ok:
    logging.info(f"Requisicao bem-sucedida: Status {response.status_code}")

    try:
        df_tratado = tratar_dados_bruto(response)
        
        # Análise: Valor Total por Mês
        df_valores_mes = vl_total_por_mes(df_tratado)
        
        salvar_resumo_em_csv(df_valores_mes, arquivo_mes)
        logging.info(f"Relatorio de valor total por mes salvo com sucesso em {arquivo_mes}")

        
        logging.info("Valores totais por mes calculados com sucesso:")
        for mes, valor in df_valores_mes.itertuples(index=False):
            logging.info(f"{mes}: {valor}")
        

    except Exception as e:
        logging.exception(f"Erro ao processar ou salvar os dados: {e}")
        sys.exit(1)

else:
    logging.error("Falha ao obter dados da API.")
    if response is not None:
        logging.error(f"Status: {response.status_code} - {response.text}")
    sys.exit(1)