from scraping import get_polarity
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback, Input, Output
import plotly.express as px

df = get_polarity()

parte1 = df.iloc[:len(df)//2, :]
parte2 = df.iloc[len(df)//2:, :]

# maior valor de polaridade
linha_max_pol = df.loc[df['polarity'].idxmax()]

# menor valor de polaridade 
linha_min_pol = df.loc[df['polarity'].idxmin()]

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
     html.A('Clique aqui', href='https://quotes.toscrape.com/', target='_blank'),

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
    # quem mais positivo 
    html.H2(children='Qual autor é mais positivo:'),
    html.P(f"Autor: {linha_max_pol['author']}"),
    html.P(f"Polaridade: {linha_max_pol['polarity']}"),
    html.P(f'Frase: {linha_max_pol["phrase"]}'),
    # mais negativo
    html.H2(children='Qual autor é mais negativo:'),
    html.P(f"Autor: {linha_min_pol['author']}"),
    html.P(f"Polaridade: {linha_min_pol['polarity']}"),
    html.P(f'Frase: {linha_min_pol["phrase"]}'),
    ])


@callback(
    Output(component_id='controle-grafico', component_property='figure'),
    Input(component_id='exib-partes', component_property='value')
)
def exib_parte1(parte):
    if parte == "parte1":
        fig = px.histogram(parte1, x='author', y='polarity', histfunc='avg')
        return fig
    
    elif parte == "parte2":
        fig = px.histogram(parte2, x='author', y='polarity', histfunc='avg')
        return fig



if __name__ == "__main__":
    app.run(debug=True)

