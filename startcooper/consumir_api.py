from dotenv import load_dotenv
import logging
import os
import pandas as pd
import requests
import sys
import plotly.express as px
import dash
from dash import dcc, html, Input, Output


GLOBAL_DATAFRAME_TO_DOWNLOAD = None 
def configurar_ambiente():

    pasta_dados = os.path.join("data", "privado")
    arquivo_csv = os.path.join(pasta_dados, "investimentos_marica_2025.csv")
    os.makedirs(pasta_dados, exist_ok=True) # Cria a pasta de dados, se não existir
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
    filename=os.path.join("logs", "consumir_api.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

    load_dotenv()
    logging.info("Iniciando execucao do script de investimentos")
    return arquivo_csv

def consumirAPI():

    url = "https://apicadprev.trabalho.gov.br/DAIR_CARTEIRA"
    load_dotenv()
    cnpj = os.getenv("CNPJ_ENTIDADE")
    uf = os.getenv("UF_ENTIDADE")
    ano = os.getenv("ANO_CONSULTA")
    if not (cnpj and uf and ano):

        logging.error(f"Variáveis de ambiente faltando: CNPJ={cnpj}, UF={uf}, ANO={ano}")
        sys.exit(1)

    parametros = {
        'nr_cnpj_entidade': cnpj,
        'sg_uf': uf,
        'dt_ano': ano
    }

    logging.info(f"Consultando API com parametros: {parametros}")

    try:
        response = requests.get(url, timeout=60, params=parametros, verify=True)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins
        return response
    except requests.exceptions.Timeout:
        logging.error("Timeout na requisicao da API")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na conexao: {e}")
        sys.exit(1)
    except Exception as e:
        logging.exception(f"Erro inesperado: {e}")
        sys.exit(1)
def processar_dados(response):

    if response is None or not getattr(response, "ok", False):
        logging.error("Resposta inválida ou requisição com erro.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    json_data = response.json()
    data = json_data.get("data", [])
    if not data:
        logging.warning("Nenhum dado retornado pela API.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    df = pd.DataFrame(data)
    df.drop(columns=['Unnamed: 0'], inplace=True,errors='ignore')
    df.nunique()
    df["no_segmento"].unique()

    novo_header = df.iloc[0]            
    df.columns = novo_header
    df = df.reset_index(drop=True)

    for col in ['vl_atual_ativo', 'vl_total_atual']:
        df[col] = (
            df[col].astype(str)
            .str.replace(r'[^0-9.,]', '', regex=True)
            .str.replace(',', '.', regex=False)
            .astype(float)
        )

    colunas_desejadas = ['no_segmento', 'dt_mes_bimestre', 'vl_atual_ativo', 'vl_total_atual']
    df = df[colunas_desejadas]

    df = df.sort_values('dt_mes_bimestre').reset_index(drop=True)

    df_grouped = df.groupby(['dt_mes_bimestre','no_segmento'])['vl_total_atual'].sum().reset_index()
    df_grouped = df_grouped.sort_values(by=['no_segmento', 'dt_mes_bimestre'])
    df_grouped['lag_vl_total'] = df_grouped.groupby('no_segmento')['vl_total_atual'].shift(1)
    df_grouped['lag_vl_total'].fillna(0)
    correlation_matrix = df.select_dtypes(include='float64').corr()

    return df, df_grouped, correlation_matrix

def gerar_graficos(df_grouped):

    fig2 = px.sunburst(df_grouped,
                   path=['dt_mes_bimestre','vl_total_atual','no_segmento'],
                   values='vl_total_atual',
                   title='Distribuição de Investimentos por Segmento e Bimestre',
                   color='no_segmento',
                   )

    fig2.update_traces(textinfo="label+percent parent")
    fig2.update_layout(margin=dict(l=20, r=20, t=80, b=20),height=800)
    return  fig2

def criar_layout(app, fig2):

    app.layout = html.Div(

        style={
            'backgroundColor': "#0f0c0c",
            'fontFamily': 'Arial, sans-serif',
            'padding': '20px'
        },
        children=[
            html.H1(
                'Dashboard de Análise de Investimentos',
                style={'textAlign': 'center', 'marginBottom': '40px'}
            ),
             html.Div(
                style={'textAlign': 'center', 'marginBottom': '40px'},
                children=[
                    html.Button(
                        "Baixar CSV",
                        id="btn-download",
                        style={
                            'backgroundColor': '#007BFF',
                            'color': 'white',
                            'border': 'none',
                            'padding': '10px 20px',
                            'borderRadius': '8px',
                            'cursor': 'pointer',
                            'fontSize': '16px'
                        }
                    ),
                    dcc.Download(id="download-dataframe-csv")
                ]
            ),

            html.Div(
                dcc.Graph(id='graph-sunburst', figure=fig2),
                style={
                    'width': '100%',
                    'display': 'flex',
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'marginBottom': '60px'
                }
            ),

            html.Hr(),
        ]
    )

def registrar_callbacks(app):
    global GLOBAL_DATAFRAME_TO_DOWNLOAD

    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("btn-download", "n_clicks"),
        prevent_initial_call=True
    )
    def download_csv(n_clicks):
        if GLOBAL_DATAFRAME_TO_DOWNLOAD is not None and not GLOBAL_DATAFRAME_TO_DOWNLOAD.empty:
            return dcc.send_data_frame(GLOBAL_DATAFRAME_TO_DOWNLOAD.to_csv, "dadoss.csv", index=False)
        else:
            logging.warning("Tentativa de download sem dados disponíveis.")
            return dcc.send_data_frame(pd.DataFrame({'Erro': ['Nenhum dado para download.']}).to_csv, "erro_dados.csv", index=False)

def executar_dashboard(df_grouped, df_table):
    global GLOBAL_DATAFRAME_TO_DOWNLOAD
    GLOBAL_DATAFRAME_TO_DOWNLOAD = df_table

    app = dash.Dash(__name__)
    fig2 = gerar_graficos(df_grouped)
    criar_layout(app, fig2)
    registrar_callbacks(app)
    app.run(debug=True)

if __name__ == "__main__":
    configurar_ambiente()
    response = consumirAPI()
    df, df_grouped, correlation_matrix = processar_dados(response)

    if df.empty:
        logging.error("O processamento de dados falhou ou a API retornou dados vazios. Encerrando.")
        sys.exit(1)

    executar_dashboard(df_grouped, df)