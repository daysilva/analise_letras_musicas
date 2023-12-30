from text_analise import get_polarity, df_frequencia_palavra
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback, Input, Output
import plotly.express as px

df = get_polarity()

df_freq = df_frequencia_palavra()

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
        """Nessa analise iremos ver frases de pessoas 
        famosas bem como sua polaridade. Ou seja, veremos a positividade de uma
        frase dita por alguém. Frases positivas/bonitas tem um valor a sima de 0.
        e frases negativas tem um valor a baixo de 0."""
    ]),
    html.P(["""As frases foram obtidas do site quotes, onde utilizamos a 
            técnica de scraping - raspagem de dados, para extrair essas frases.
            Link do site onde retiramos as frases:
            """]),
     html.A('Clique aqui', href='https://www.letras.mus.br/', target='_blank'),

     html.Hr(),
    dcc.RadioItems(
                options=['parte1', 'parte2'],
                value='parte1',
                id='exib-partes'
            ),
    dcc.Graph(
                id="controle-grafico",
                figure={}
            ),
    html.Hr(),
        html.H2(children='As 5 palavras mais repetidas'),
    dcc.Graph(
        id="grafico-radar",
        figure=fig_radar
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

