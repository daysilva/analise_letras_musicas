from text_analise import get_polarity, df_frequencia_palavra, len_musica
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback, Input, Output
import plotly.express as px


df = get_polarity()

df_freq = df_frequencia_palavra()

df_len_musica = len_musica()



# montar um grafico de radar
fig_radar = px.line_polar(df_freq, r='quanti', theta='palavra', line_close=True)
fig_radar.update_traces(fill='toself')
fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(df_freq['quanti'])]
        )
    ),
    showlegend=False
)



len_musica_titulo = px.scatter(df_len_musica,
                    x='titulo', y='tamanho', 
                    color='titulo', title='Tamanho das letras e seus titulos')


len_musica_estilo = px.scatter(df_len_musica,
                    x='estilo', y='tamanho', 
                    color='titulo', title='Tamanho das letras e seus estilos')



# o dataset com a polaridade das musicas é muito grande
# então vamos divi-lo em duas partes
parte1 = df.iloc[:len(df)//2, :]
parte2 = df.iloc[len(df)//2:, :]


app = Dash(__name__)

app.layout = html.Div([
    html.Div(
        className='my-header',
        children=[
            html.H1(children='Media de polaridade das frases de pessoas famosas')
             ]
    ),
    html.P([
        """Analise feita em um site de letras de musicas. 
        Esta analise obtem varias letras de musicas de estilos diferentes a fim de
        analisar o conteudo de suas letras."""
    ]),
     html.A('Site de onde foram obtidas as letras de músicas', href='https://www.letras.mus.br/', target='_blank'),

     html.Hr(),
    dcc.RadioItems(
                options=['parte1', 'parte2'],
                value='parte1',
                id='exib-partes'
            ),
    html.H2(children='Analise de polaridade das letras'),
    dcc.Graph(
                id="controle-grafico",
                figure={}
            ),
    html.Hr(),
        html.H2(children='As 6 palavras mais repetidas'),
    dcc.Graph(
        id="grafico-radar",
        figure=fig_radar
    ),
    html.Hr(),
    html.H2(children='Tamanho da letra das musicas em quantidade de caracteres'),
    dcc.Graph(
        id="grafico-scater-titulo",
        figure=len_musica_titulo
    ),
     dcc.Graph(
        id="grafico-scater-estilo",
        figure=len_musica_estilo
    ),
    ])


@callback(
    Output(component_id='controle-grafico', component_property='figure'),
    Input(component_id='exib-partes', component_property='value')
)
def exib_parte1(parte):
    if parte == "parte1":
        fig = px.histogram(parte1, x='estilo', y='polarity', histfunc='avg')
        return fig
    
    elif parte == "parte2":
        fig = px.histogram(parte2, x='estilo', y='polarity', histfunc='avg')
        return fig



if __name__ == "__main__":
    app.run(debug=True)

