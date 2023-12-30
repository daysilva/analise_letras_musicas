from random import randint
import pandas as pd
import numpy as np
from textblob import TextBlob
import pandas as pd
from collections import Counter
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

df_letras = pd.read_csv('./letras.csv')



def get_polarity():
    try:
        
        data = {
            "titulo": [],
            "estilo": [],
            "polarity": []
        }

       
        for l in range(0, len(df_letras["titulo"])):
          
            data["titulo"].append(df_letras["titulo"][l]) # guardar apenas o titulo na coluna do dataframe
                
            analise = TextBlob(df_letras["letra"][l])
            polaridade = analise.sentiment.polarity
            data['polarity'].append(polaridade) # guardar a polaridade
            data["estilo"].append(df_letras["estilo"][l])

            # data['phrase'].append(phrase[i][0]) # guardar a frase

        df = pd.DataFrame(data)

        return df
    
    except:
        print("Erro ao processar dataset")



def frequencia_palavra(texto):

    blob = TextBlob(texto)

    # Pré-processamento - remover pontuações e transformar para minúsculas
    palavras = [word.strip(string.punctuation).lower() for word in blob.words]

    stop_words_en = set(stopwords.words('english'))
    if stop_words_en is not None:
        palavras = [word for word in palavras if word not in stop_words_en]


    stop_words_pt = set(stopwords.words('portuguese'))
    if stop_words_pt is not None:
        palavras = [word for word in palavras if word not in stop_words_pt]

    # Contagem de palavras
    cont = Counter(palavras)

     # pegar as palavras mais frequentes
    frequen = cont.most_common(1)

    return frequen


def df_frequencia_palavra():

    palavras = {
        "palavra": [],
        "quanti": []
    }

    for c in df_letras["letra"]:
        p = frequencia_palavra(c)

        # vwrificar se alguns dados nao sao uma listas vazia
        # verificar se a palavra tem pelo menos 4 letras
        if len(p) > 0 and len(p[0][0]) > 3:

            palavras["palavra"].append(p[0][0])
            palavras["quanti"].append(p[0][1])
    

    df = pd.DataFrame(palavras)

    order = df.sort_values(by='quanti', ascending=False)
    top5 = order.head(6)

    return top5


# print(df_frequencia_palavra())