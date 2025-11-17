import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output 
import os
import dash_bootstrap_components as dbc 

# --- 1. Carregando os Dados (Apenas 1 CSV) ---
pasta_dados = os.path.join("data", "privado")

# Usamos o novo arquivo gerado pelo 'main.py' simplificado
arquivo_mes = os.path.join(pasta_dados, "investimentos_marica_2025_por_mes.csv")

# Carrega o DataFrame
try:
    df_mes = pd.read_csv(arquivo_mes, sep=';', decimal=',')

except FileNotFoundError as e:
    print(f"ERRO: Arquivo CSV não encontrado: {e.filename}")
    print(f"Execute o 'main.py' primeiro para gerar o arquivo 'investimentos_marica_2025_por_mes.csv'.")
    exit()

# --- 2. Criando o Gráfico (Apenas 1 Figura) ---

TEMPLATE_GRAFICO = "plotly_white" 

# Gráfico renomeado para 'Mês'
fig_total_mes = px.line(
    df_mes, 
    x='dt_mes_bimestre',  # A coluna do CSV (pode manter o nome)
    y='vl_total_atual',
    title="Evolução do Patrimônio Total por Mês (2025)",
    labels={'dt_mes_bimestre': 'Mês', 'vl_total_atual': 'Valor Total (R$)'},
    markers=True, 
    template=TEMPLATE_GRAFICO
)
# Ajustes de layout para o gráfico
fig_total_mes.update_layout(
    yaxis_title="Valor (em R$)", 
    paper_bgcolor='rgba(0,0,0,0)', # Fundo transparente
    plot_bgcolor='rgba(0,0,0,0)',  # Fundo transparente
    title_x=0.5 # Centraliza o título do gráfico
)

# --- 3. Montando o Layout do Dashboard (Versão Simplificada) ---
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Navbar (Barra de Título)
navbar = dbc.NavbarSimple(
    brand="📈 Evolução Patrimonial - RPPS Maricá (2025)",
    brand_href="#",
    color="primary", 
    dark=True, 
    sticky="top", 
)

# Layout principal
app.layout = html.Div([ 
    dcc.Download(id="download-csv"), 
    navbar, 
    
    # Container principal que centraliza o conteúdo
    dbc.Container(className="mt-4", children=[
        
        # Uma linha...
        dbc.Row(
            # ...com uma coluna centralizada
            dbc.Col(
                [
                    # Card 1: O Gráfico
                    dbc.Card(
                        dbc.CardBody(
                            dcc.Graph(
                                id='grafico-total-mes', 
                                figure=fig_total_mes
                            )
                        ),
                        className="shadow-sm border-0 mb-3" # Sombra leve, sem borda, margem embaixo
                    ),
                    
                    # Card 2: O Botão de Download
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Download dos Dados", className="card-title"),
                                html.P(
                                    "Baixe o arquivo CSV com os totais consolidados por mês.",
                                    className="card-text"
                                ),
                                dbc.Button(
                                    "Baixar .CSV (Dados por Mês)",
                                    id="btn-download-csv", 
                                    color="primary", 
                                    className="w-100" # Botão ocupa 100% da largura do card
                                )
                            ]
                        ),
                        className="shadow-sm border-0" # Sombra leve, sem borda
                    )
                ],
                width=12, md=10, lg=8 # Ocupa 8 de 12 colunas em telas grandes (centralizado)
            ),
            justify="center" # Comando para centralizar a coluna na linha
        )
    ]) 
]) 


# --- 4. Callbacks (Interatividade) ---
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True 
)
def func_download_csv(n_clicks):
    # Envia o dataframe 'df_mes' com o novo nome de arquivo
    return dcc.send_data_frame(
        df_mes.to_csv, 
        "investimentos_marica_2025_por_mes.csv", 
        index=False, 
        sep=';', 
        decimal=','
    )

# --- 5. Rodando o Servidor ---
if __name__ == '__main__':
    app.run(debug=True)