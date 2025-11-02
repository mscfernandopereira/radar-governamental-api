from dotenv import load_dotenv
import logging
import os
import pandas as pd
import requests
import sys
import plotly.express as px
import dash
from dash import dcc, html, Input, Output

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
url = "https://apicadprev.trabalho.gov.br/DAIR_CARTEIRA?nr_cnpj_entidade=29131075000193&sg_uf=RJ&dt_ano=2025"
nome_arquivo_csv = "dados_carteira_rpps.csv"
try:
    logging.info(f"Buscando dados da API: {url}")
    response = requests.get(url, timeout=60, verify=True)
    response.raise_for_status() 
    logging.info(f"Sucesso! Status Code: {response.status_code}")

    raw_response_data = response.json()

    # 2. Verificar se a API retornou dados
    if raw_response_data:
        # --- CORREÇÃO INICIADA ---
        # Os dados que queremos estão dentro da chave 'data' de CADA item na lista
        investment_data_list = raw_response_data["data"]
        
        # 3. Carregar os dados extraídos em um DataFrame
        df = pd.DataFrame(investment_data_list)
        # --- CORREÇÃO TERMINADA ---

        df['vl_total_atual'] = pd.to_numeric(df['vl_total_atual'], errors='coerce').fillna(0)

        df.to_csv(nome_arquivo_csv, index=False, encoding='utf-8')
        logging.info(f"Arquivo '{nome_arquivo_csv}' salvo com sucesso com {len(df)} linhas.")
    else:
        logging.warning("A API retornou resposta vazia ou formato inesperado.")
        sys.exit(1)

except Exception as e:
    logging.exception(f"Erro ao processar dados da API: {e}")
    sys.exit(1)
    # --- FIM DA ADIÇÃO ---

except requests.exceptions.Timeout:
    logging.error("Timeout na requisicao da API")
    sys.exit(1)
except requests.exceptions.HTTPError as e:
    # Erro HTTP (ex: 404 Not Found, 500 Internal Server Error)
    logging.error(f"Erro HTTP: {e} - Status Code: {e.response.status_code}")
    logging.error(f"Resposta da API: {e.response.text[:200]}...") # Mostra o início da resposta
    sys.exit(1)
except requests.exceptions.JSONDecodeError:
    # A API respondeu (Status 200), mas o conteúdo não era um JSON válido
    logging.error("Erro: A resposta da API não foi um JSON válido.")
    logging.error(f"Resposta recebida: {response.text[:200]}...") # Mostra o início da resposta
    sys.exit(1)
except requests.exceptions.RequestException as e:
    logging.error(f"Erro na conexao: {e}")
    sys.exit(1)
except Exception as e:
    logging.exception(f"Erro inesperado: {e}") # .exception() captura o stack trace
    sys.exit(1)

df = pd.read_csv(nome_arquivo_csv)
df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')

logging.info(f"Colunas encontradas no CSV: {df.columns.tolist()}")

df.nunique()
df["no_segmento"].unique()

logging.info("Contagem de valores únicos por coluna:")
logging.info(df.nunique())
logging.info("Segmentos únicos encontrados:")
logging.info(df["no_segmento"].unique())

df_grouped = df.groupby(['dt_mes_bimestre','no_segmento'])['vl_total_atual'].sum().reset_index()
df_grouped = df_grouped.sort_values(by=['no_segmento', 'dt_mes_bimestre'])
df_grouped['lag_vl_total'] = df_grouped.groupby('no_segmento')['vl_total_atual'].shift(1)
df_grouped['lag_vl_total'].fillna(0)

correlation_matrix = df.select_dtypes(include='float64').corr()

# Create the heatmap
fig1 = px.imshow(correlation_matrix,
                text_auto=True,  # Display correlation values on the heatmap
                color_continuous_scale='RdBu_r', # Red-Blue reversed color scale
                title='Matriz de Correlação'
                )
fig1.update_layout(margin=dict(l=20, r=20, t=80, b=20),height=800)
data_bar = df.groupby('no_segmento')["id_ativo"].nunique()
data_bar = data_bar.sort_values(ascending=False)

fig2 = px.sunburst(df_grouped,
                   path=['dt_mes_bimestre','vl_total_atual','no_segmento'],
                   values='vl_total_atual',
                   title='Distribuição de Investimentos por Segmento e Bimestre',
                   color='no_segmento',
                   )
fig2.update_traces(textinfo="label+percent parent")
fig2.update_layout(margin=dict(l=20, r=20, t=80, b=20),height=800)

# ======== App Dash ========
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#f9f9f9',
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px'
    },
    children=[
        html.H1(
            'Dashboard de Análise de Investimentos',
            style={'textAlign': 'center', 'marginBottom': '40px'}
        ),

        # Gráfico Sunburst (topo)
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
        html.Div(
            children=[
                html.Button("Baixar Dados Filtrados", id="btn-download", n_clicks=0,
                            style={'backgroundColor': '#007bff', 'color': 'white',
                                   'padding': '10px 20px', 'border': 'none',
                                   'borderRadius': '8px', 'cursor': 'pointer'}),
                dcc.Download(id="download-dataframe-csv")
            ],
            style={'textAlign': 'center', 'marginBottom': '40px'}
        ),

        html.Hr(),

        # Gráfico Heatmap (embaixo)
        html.Div(
            dcc.Graph(id='graph-heatmap', figure=fig1),
            style={
                'width': '100%',
                'margin': '0 auto',
                'marginTop': '60px'
            }
        )
    ]
)
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def baixar_csv(n_clicks):
    # Agrupa o total gasto por segmento (garante as 2 colunas desejadas)
    df_download = df_grouped.groupby("no_segmento", as_index=False)[["vl_total_atual"]].sum()
    df_download.columns = ["no_segmento", "Montante_Total_2025"]

    # Nome do arquivo
    filename = "montante_total_2025.csv"

    # Usa ; como separador e utf-8-sig para abrir corretamente no Excel (Windows)
    return dcc.send_data_frame(df_download.to_csv, filename,
                               index=False, sep=';', encoding='utf-8-sig')
if __name__ == '__main__':
    app.run(debug=True)