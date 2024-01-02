from text_analise import get_polarity, df_frequencia_palavra, len_musica
import pandas as pd
from dash import Dash, html, dcc, dash_table, callback, Input, Output
import plotly.express as px


# DATAFRAMES UTILIZADOS
df = get_polarity()

df_freq = df_frequencia_palavra()

df_len_musica = len_musica()

df_quant_palavras = pd.read_csv('./quant_palavras.csv')

count_pal = df_quant_palavras.pivot_table(
    index="palavra",
    values="quant",
    aggfunc="sum")

total_quant_order = count_pal.sort_values(by="quant", ascending=False)
top10_palavras = total_quant_order.head(10)


# order_polaridade = df.sort_values(by='polarity', ascending=False)
# top5 = order_polaridade.head(5)

# df_palvras_posi_polari = df_frequencia_palavra(top5)

# print(df_palvras_posi_polari)
# GRAFICOS

# fig_palvras_posi_polari = px.scatter(df_freq, x="estilo_titulo", y="quanti", color="palavra", size="quanti",
#                  title="Dispersão da Quantidade de Palavras Repetidas em Cada Música",
#                  labels={"quanti": "Quantidade de Palavras Repetidas", "palavra": "Palavra", "titulo": "Título da Música"},
#                  height=400)


fig_quant_palav = px.scatter(df_freq, x="estilo_titulo", y="quanti", color="palavra", size="quanti",
                 title="Dispersão da Quantidade de Palavras Repetidas em Cada Música",
                 labels={"quanti": "Quantidade de Palavras Repetidas", "palavra": "Palavra", "titulo": "Título da Música"},
                 height=400)



len_musica_titulo = px.scatter(df_len_musica,
                    x='titulo', y='tamanho', 
                    color='titulo', title='Tamanho das letras e seus titulos')


len_musica_estilo = px.scatter(df_len_musica,
                    x='estilo', y='tamanho', 
                    color='titulo', title='Tamanho das letras e seus estilos')


hist_quant_pal = px.bar(
    top10_palavras,
    x=top10_palavras.index,  
    y='quant',              
    labels={'x': 'Palavra', 'quant': 'Quantidade'},
    title='Top 10'
)



# o dataset com a polaridade das musicas é muito grande
# então vamos divi-lo em duas partes
parte1 = df.iloc[:len(df)//2, :]
parte2 = df.iloc[len(df)//2:, :]

# criar umanoca loluna que mostre o estilo e o titulo em apenas uma string
parte1['estilo_titulo'] = parte1['estilo'] + ' | ' + parte1['titulo']
parte2['estilo_titulo'] = parte2['estilo'] + ' | ' + parte2['titulo']

INFO_PROCED = False

app = Dash(__name__)

app.layout = html.Div([
    html.Div(
        style={'textAlign': 'center', 'margin-bottom': '20px', 'font-family': "Gill Sans", "padding-left": "30px"},
        className='my-header',
        children=[
            html.H1(children='RASPAGEM DE DADOS | ANÁLISE DE TEXTOS'),
            html.Div(
                 style={'textAlign': 'left', 'font-family': "Gill Sans"},
                 children=[
                    html.P([
                            """Analise feita em um site de letras de musicas. 
                            Esta analise obtem varias letras de musicas de estilos diferentes a fim de
                            analisar o conteudo de suas letras. """,
                    html.A('Fonte', href='https://www.letras.mus.br/', target='_blank'),
                    ]),
                 ]
            )
           
        ]
    ),
     html.Hr(),
    #  MAIN
    #  "background-color": "#C4D0F2",
    html.Div(
        style={'padding': '20px'},
        children=[
        html.H2(style={'font-family': "Gill Sans"}, children="Como os dados foram estraidos?"),
       html.Button(
            style={
                "background-color": "#fff",
                "color": "#000",
                "font-size": "20px", 
                "font-whegth": "bold",
                "border": "0", 
                },
            children='^ detalhar', id='btn-detalhar-proced'
                ),
         html.Div(
            id='info_procedimento',
            style={
                'margin-top': '10px',
                'margin-bottom': '20px',
                "padding": "5px",
                "background-color": "#E4EAF2",
                "border-radius": "10px"
                },
            children=[
                html.P(style={},
                       id="info-ocult",
                       children="..."),
                 html.Ul(
                      style={"display": "none"},
                      id="lista_procedimento",
                      children=[
                        html.Li(style={'margin-top': '10px', 'font-family': "Gill Sans"}, children="Apos definirmos o tema que queriamos invertigar, demos inicio a coleta dos dados"),
                        html.Li(style={'margin-top': '10px', 'font-family': "Gill Sans"}, children="Para isso, utilizamos a tecnica de Web Scraping"),
                        html.Li(style={'margin-top': '10px', 'font-family': "Gill Sans"}, children="Extração complicada - Informações muito dispersas nos conteudos das paginas"),
                        html.Li(style={'margin-top': '10px', 'font-family': "Gill Sans"}, children="""Para facilitar, criamos uma classe para coletar os dados, 
                                criando metodos responsavéis por cada conteudo a ser extraido"""),
                        html.Li(style={'margin-top': '10px', "list-style-type": "none"}, children=[
                            html.Img(style={'width': '35%'}, src=app.get_asset_url("foto.png"), alt="Descrição da Imagem")
                        ]),
                        html.Li(style={'margin-top': '10px',  "list-style-type": "none"}, children=[
                            html.Img(style={'width': '35%'}, src=app.get_asset_url("obter_letras_diag.png"), alt="diagrama - obter letra")
                        ]),
                          html.Li(
                              style={'margin-top': '10px', 'font-family': "Gill Sans"},
                            children="Na pagina que contem os links de letras de música, escolhemos uma música aleatoriamente para adicionar ao dataset"),
                         html.Li(style={'margin-top': '10px', 'font-family': "Gill Sans"}, children="Extraimos o conteudo de cada pagina e salvamos tudo em um arquivo csv"),
                ])
            ]),
        html.H2(children='Analise de polaridade das letras'),
        html.Button(
            style={
                "background-color": "#fff",
                "color": "#000",
                "font-size": "20px", 
                "font-whegth": "bold",
                "border": "0", 
                },
            children='^ detalhar', id='btn-detalhar-polarid'
                ),
        html.Div(
            id='info_polaridade',
            style={
                'margin-top': '10px',
                'margin-bottom': '20px',
                "padding": "5px",
                "background-color": "#E4EAF2",
                "border-radius": "10px"
                },
            children=[
                html.P(style={},
                       id="info-polari-ocult",
                       children="..."),
                 html.Ul(
                      style={"display": "none"},
                      id="lista_polari",
                      children=[
                        html.Li(
                            style={'margin-top': '10px', 'font-family': "Gill Sans"}, 
                            children="Analisamos o dataset que foi criado a partir das letras de músicas extraidas do site"),
                        html.Li(
                            style={'margin-top': '10px', 'font-family': "Gill Sans"}, 
                            children="""Para cada letra presente no dataset, fazemos a análise de polaridade a fim de verificar o quao 
                                        positivo é o seu conteudo"""),
                        html.Li(
                            style={'margin-top': '10px', 'font-family': "Gill Sans"}, 
                            children="Biblioteca TextBlob"),
                        html.Li(
                        style={'margin-top': '10px', 'font-family': "Gill Sans"}, 
                        children="""
                        A biblioteca TextBlob não oferece suporte para textos em portuges. Então fizemos 
                        uma cópia do dataser traduzindo as letras para o ingles"""),
                ])
            ]),
                # ######
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
            html.H2(children='As 6 palavras mais repetidas em cada música'),
        dcc.Graph(
            id="grafico-radar",
            figure=fig_quant_palav
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
        html.Hr(),
        html.H2(children='As 10 palavras mais utilizadas nas letras de musicas'),
        dcc.Graph(
            id="grafico-hist-top10",
            figure=hist_quant_pal
        ),
        ])
    ])


# exibir informação sobre procedimento
@callback(
    [Output("lista_procedimento", "style"), Output("info-ocult", "style")],
    [Input("btn-detalhar-proced", "n_clicks")]
)
def exib_info_proced(n_clicks):
   
    if n_clicks is None or n_clicks % 2 == 0:
        return {"display": "none"}, {"display": "block", "margin-left": "10px"}
    else:
        return {"display": "block"}, {"display": "none"}
    

# exibir informação sobre o grafico de polaridade
@callback(
    [Output("lista_polari", "style"), Output("info-polari-ocult", "style")],
    [Input("btn-detalhar-polarid", "n_clicks")]
)
def exib_info_polari(n_clicks):
   
    if n_clicks is None or n_clicks % 2 == 0:
        return {"display": "none"}, {"display": "block", "margin-left": "10px"}
    else:
        return {"display": "block"}, {"display": "none"}


@callback(
    Output(component_id='controle-grafico', component_property='figure'),
    Input(component_id='exib-partes', component_property='value')
)
def exib_parte1(parte):
    if parte == "parte1":
        fig = px.histogram(parte1, x='estilo_titulo', y='polarity', histfunc='avg')
        fig.update_layout(
        xaxis_title='Estilo - Título',
        yaxis_title='Polaridade',
        showlegend=False, 
        xaxis=dict(
        tickangle=90,
         )
        )

        return fig
    
    elif parte == "parte2":
        fig = px.histogram(parte2, x='estilo_titulo', y='polarity', histfunc='avg')
        fig.update_layout(
        xaxis_title='Estilo - Título',
        yaxis_title='Polaridade',
        showlegend=False, 
        xaxis=dict(
        tickangle=90,
         )
        )
        return fig



if __name__ == "__main__":
    app.run(debug=True)

