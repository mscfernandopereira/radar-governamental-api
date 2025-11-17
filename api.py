import requests 
import logging

def consumir_api_previdencia_marica(url: str, parametros: dict) -> requests.Response | None:
    """
    Função para consumir a API da previdência de Maricá.
    
    Parâmetros:
    url (str): A URL da API a ser consumida.
    parametros (dict): Um dicionário contendo os parâmetros da requisição.
    
    Retorna:
    requests.Response: O objeto de resposta da requisição em caso de sucesso.
    None: Em caso de falha na requisição (Timeout, Erro de Conexão, etc.).
    """
    try:
        response = requests.get(url, timeout=60, params=parametros, verify=True)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins
        return response
    except requests.exceptions.Timeout:
        logging.error("Timeout na requisicao da API")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na conexao: {e}")
        return None
    except Exception as e:
        logging.exception(f"Erro inesperado: {e}")
        return None