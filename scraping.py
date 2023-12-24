import requests
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
from textblob import TextBlob


def getphrases(num_page):
    url = f"https://quotes.toscrape.com/page/{num_page}"

    response = requests.get(url)

    phrases = []

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')   

        span = soup.find_all('span', class_='text')
        author = soup.find_all('small', class_='author')


        for sp in range(len(span)):
            # print(span[sp].text, "\n", author[sp].text, "\n")
            phrases.append([span[sp].text, author[sp].text])
            
        return phrases

    else:
        print(f"error: {response.status_code}")


def get_polarity():

    data = {
        "author": [],
        "polarity": [],
        "phrase": []
    }

    # percorrer todas as paginas coletando as frases e seus autores
    for p in range(1, 11):
        phrase = getphrases(p)
        for i in range(0, len(phrase)):
            data["author"].append(phrase[i][1]) # guardar apenas o autor na coluna do dataframe
            
            analise = TextBlob(phrase[i][0])
            polaridade = analise.sentiment.polarity
            data['polarity'].append(polaridade) # guardar a polaridade
            data['phrase'].append(phrase[i][0]) # guardar a frase

    df = pd.DataFrame(data)

    return df

