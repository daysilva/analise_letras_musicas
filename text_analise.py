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
from googletrans import Translator

df_letras = pd.read_csv('./letras.csv')

df_letras_en = pd.read_csv('./letras_en.csv')



def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language)
    return translated_text.text


def letra_en():
    """
    Fazer uma cópia do dataset para o inglês - apenas as letras das músicas
    """
    letras_en = {
        "titulo": [],
        "estilo": [],
        "letra": []
    }

    for l in range(0, len(df_letras["titulo"])):
        if len(df_letras["letra"][l]) > 10:
            letras_en["titulo"].append(df_letras["titulo"][l])
            letras_en["estilo"].append(df_letras["estilo"][l])

            letra_pt = df_letras["letra"][l]
            letra_ingles = translate_text(letra_pt)
            letras_en["letra"].append(letra_ingles)
        else:
            print("Dado faltante")

    df = pd.DataFrame(letras_en)
    df.to_csv('letras_en.csv', index=False)


def get_polarity():
    try:
        
        data = {
            "titulo": [],
            "estilo": [],
            "polarity": [],
            "letra": []
        }

       
        for l in range(0, len(df_letras_en["titulo"])):
          
            data["titulo"].append(df_letras_en["titulo"][l]) # guardar apenas o titulo na coluna do dataframe

            # text_analize = df_letras_en["letra"][l].replace("[", "").replace("]", "")
            # text_split = text_analize[0: len(text_analize) // 2]

            
                
            analise = TextBlob(df_letras_en["letra"][l])

            polaridade = analise.sentiment.polarity
            data['polarity'].append(polaridade) # guardar a polaridade
            data["estilo"].append(df_letras_en["estilo"][l])
            data["letra"].append(df_letras_en["letra"][l])

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
        "quanti": [],
        "estilo_titulo": []
    }

    for l in range(0, len(df_letras["letra"])):
        p = frequencia_palavra(df_letras["letra"][l])

        # vwrificar se alguns dados nao sao uma listas vazia
        # verificar se a palavra tem pelo menos 4 letras
        if len(p) > 0 and len(p[0][0]) > 3:

            palavras["palavra"].append(p[0][0])
            palavras["quanti"].append(p[0][1])
            titulo = df_letras["titulo"][l]
            estilo = df_letras["estilo"][l]

            tit_est = titulo + " | " + estilo

            palavras["estilo_titulo"].append(tit_est)
    

    df = pd.DataFrame(palavras)

    order = df.sort_values(by='quanti', ascending=False)
    top5 = order.head(6)

    return top5



def df_frequencia_palavra_polari(df_polari):
    """
    pegar as palavras mais repetidas das letras com maior ou menor polaridade
     data = {
            "titulo": [],
            "estilo": [],
            "polarity": [],
            "letra": []
        }
    """
    palavras = {
        "palavra": [],
        "quanti": [],
        "estilo_titulo": []
    }
    for index, row in df_polari.iterrows():
        p = frequencia_palavra(row["letra"])

         # verificar se alguns dados nao sao uma listas vazia
        # verificar se a palavra tem pelo menos 4 letras
        if len(p) > 0 and len(p[0][0]) > 3:

            palavras["palavra"].append(p[0][0])
            palavras["quanti"].append(p[0][1])
            titulo = row["titulo"]
            estilo = row["estilo"]

            tit_est = titulo + " | " + estilo

            palavras["estilo_titulo"].append(tit_est)
            

    df = pd.DataFrame(palavras)

    return df



def len_musica():
    """
    verificar a quantidade de palavras em uma letra de musica
    """

    musicas = {
        "titulo": [],
        "estilo":[],
        "tamanho": []
    } 

    for l in range(0, len(df_letras["titulo"])):
        titulo = df_letras["titulo"][l]
        estilo = df_letras["estilo"][l]

        refrao_unico = "" 
        musicas["titulo"].append(titulo)
        musicas["estilo"].append(estilo)
        for refrao in df_letras["letra"][l]:
           refrao_unico += refrao.replace(" ", "").replace(",", "").replace(".", "").replace(";", "").replace("`", "").replace("'", "")
           
        musicas["tamanho"].append(len(refrao_unico))
    
    df = pd.DataFrame(musicas)

    return df


def tratar_palavras():

    musicas = {
        "titulo": [],
        "estilo":[],
        "letras": []
    } 
   

    for l in range(0, len(df_letras["titulo"])):
        titulo = df_letras["titulo"][l]
        estilo = df_letras["estilo"][l]

        musicas["titulo"].append(titulo)
        musicas["estilo"].append(estilo)

        refrao_unico = "" 

        for refrao in df_letras["letra"][l]:
           refrao_unico += refrao.replace(",", " ").replace(".", " ").replace(";", " " ).replace("!", " " ).replace("(", " " ).replace(")", " " )
   
        musicas["letras"].append(refrao_unico)

    return musicas



def count_palavras():
    """
        contar a quantidadede palavras distintas que uma letrade musica pode ter
    """

    total_palavras = {
        "palavra": [],
        "quant": [],
        "titulo": [],
        "estilo": []
    }

    dict_palavra = tratar_palavras()

    for p in range(0, len(dict_palavra["letras"])):
        palavras = dict_palavra["letras"][p].split()

        # contar a ocorrência de cada palavra
        count = Counter(palavras)

        key_palavras = count.keys()
      
        for k in key_palavras:
            # apenas palavras com mais de 3 letras
            if len(k) > 3:
                total_palavras["palavra"].append(k)
                total_palavras["quant"].append(count[k])
                total_palavras["titulo"].append(dict_palavra["titulo"][p])
                total_palavras["estilo"].append(dict_palavra["estilo"][p])


    df = pd.DataFrame(total_palavras)
    df.to_csv('quant_palavras.csv', index=False)


# print(df_frequencia_palavra())
# get_polarity()
# print(len_musica())
        
# print(count_palavras())
        
# count_palavras()


# df_quant_palavras = pd.read_csv('./quant_palavras.csv')

# count_pal = df_quant_palavras.pivot_table(
#     index="palavra",
#     values="quant",
#     aggfunc="sum")

# total_quant_order = count_pal.sort_values(by="quant", ascending=False)
# top10_palavras = total_quant_order.head(15)

# print(top10_palavras)
    
# letra_en()