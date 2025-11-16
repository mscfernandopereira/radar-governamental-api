import pandas as pd
import requests
import numpy as np 

def tratar_dados_bruto(response: requests.Response) -> pd.DataFrame:
    """
    Função para tratar os dados brutos obtidos da API.
    
    Parâmetros:
    response (requests.Response): O objeto de resposta da requisição.
    
    Retorna:
    pd.DataFrame: DataFrame contendo os dados tratados.
    """
    data = response.json()["data"]

    mapa_meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'} 
    ordem_meses_cronologica = list(mapa_meses.values())

    df = pd.DataFrame(data)
    
    # Mapeia os numeros para nomes dos meses
    df['dt_mes_bimestre'] = df['dt_mes_bimestre'].map(mapa_meses) 
    
    df['dt_mes_bimestre'] = pd.Categorical(
        df['dt_mes_bimestre'],
        categories=ordem_meses_cronologica,
        ordered=True
    )

    # Converte colunas para tipos numéricos
    df['vl_total_atual'] = pd.to_numeric(df['vl_total_atual'], errors='coerce')
    
    df['qt_rpps'] = pd.to_numeric(df['qt_rpps'], errors='coerce')

    df['vl_atual_ativo'] = pd.to_numeric(df['vl_atual_ativo'], errors='coerce')
    
    df['vl_patrimonio'] = pd.to_numeric(df['vl_patrimonio'], errors='coerce')

    df['pc_cmn'] = pd.to_numeric(df['pc_cmn'], errors='coerce')

    df['pc_rpps'] = pd.to_numeric(df['pc_rpps'], errors='coerce')

    df['pc_patrimonio'] = pd.to_numeric(df['pc_patrimonio'], errors='coerce')
    
    return df

def vl_total_por_mes(df_tratado: pd.DataFrame) -> pd.DataFrame:
    """
    Função para calcular o valor total por bimestre.
    
    Parâmetros:
    df (pd.DataFrame): DataFrame contendo os dados tratados.
    
    Retorna:
    pd.Series: Série contendo o valor total por bimestre.
    """
    vl_total_por_mes = df_tratado.groupby('dt_mes_bimestre')['vl_total_atual'].sum() # Agrupa por mês e soma os valores
    vl_total_por_mes = vl_total_por_mes.round(2) # Arredonda para 2 casas decimais
    df_mensal = vl_total_por_mes.reset_index()
    return df_mensal

def salvar_resumo_em_csv(df: pd.DataFrame, caminho_arquivo: str, index: bool = False) -> None:
    """
    Função para salvar o resumo dos dados em um arquivo CSV.
    
    Parâmetros:
    ...
    index (bool): Se True, salva o índice do DataFrame. Padrão é False.
    """
    df.to_csv(caminho_arquivo, index=index, sep=';', decimal=',')