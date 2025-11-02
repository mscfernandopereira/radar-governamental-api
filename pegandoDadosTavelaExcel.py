import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html

df = pd.read_excel('rafael.xlsx')
df.drop(columns=['Unnamed: 0'], inplace=True)
df.nunique()

df["no_segmento"].unique()

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

if __name__ == '__main__':
    app.run(debug=True)