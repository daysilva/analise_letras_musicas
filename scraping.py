import requests
from bs4 import BeautifulSoup
from random import randint
import pandas as pd
import pandas as pd

class Scraping:
    """
    esta classe realiza a raspagem de letas de musicas e armazena tudo em
    um dicionario que conterá as letras de musicas e os titulos
    """
    def __init__(self):
        self.letras = {
            "titulo": [],
            "estilo": [],
            "letra": []
        }

    def getLetras(self, link):
        """
        Essa função acessa a pagina que contem a letra de uma musica especifica.
        então fazemos a raspagem de dados dessa pagina e guardamos a letra e o titulo
        """

        url = f"https://www.letras.mus.br/{link}"

        response = requests.get(url)


        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')  

            div = soup.find_all('div', class_='lyric-original')

            title_music = soup.find("h1", class_="head-title")


            self.letras["titulo"].append(title_music.text)

            aray_letra = []
            for d in div:
                p = d.find_all('p')
                for txt in p:
                    aray_letra.append(txt.text)

            self.letras["letra"].append(aray_letra)



    def getStilosMusicais(self, page):
        """
        esta função é chamada acessando a pagina de cada estilo musical que
        lhe é passado como parametro.
        ela deve coletar os links que apontam para as musicas, 
        escolher um link de musica aleatoriamente 
        """

        self.letras["estilo"].append(page)

        url = f"https://www.letras.mus.br/estilos/{page}"

        response = requests.get(url)

        links_letras_musi = []


        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')   

            div = soup.find_all('div', class_='homeTops-content js-cnt-target')


            for d in range(len(div)):
                a = div[d].find_all('a')
                for link in a:
                    links_letras_musi.append(link.get('href'))
            

            # escolher uma letra de musica aleatoriamente
            rd = randint(0, len(links_letras_musi) -1)
            lin_letra = links_letras_musi[rd]


            # chamar função que pegará a letra da musica de sua respectiva pagina
            self.getLetras(lin_letra)

        else:
            print(f"error: {response.status_code}")


estilos = [
    "alternativo",
    "axe",
    "blues",
    "bolero",
    "bossa-nova",
    "brega",
    "classico",
    "corridos",
    "country",
    "cuarteto",
    "cumbia",
    "dance",
    "dancehall",
    "disco",
    "eletronica",
    "emocore",
    "fado",
    "flamenco-bulerias",
    "folk",
    "forro",
    "funk",
    "funk-internacional",
    "gospelreligioso",
    "grunge",
    "guarania",
    "gotico",
    "hard-rock",
    "hardcore",
    "heavy-metal",
    "hip-hop-rap",
    "house",
    "indie",
    "industrial",
    "infantil",
    "instrumental",
    "j-popj-rock",
    "jazz",
    "jovem-guarda",
    "k-pop",
    "mpb",
    "mambo",
    "marchas-hinos"
]



a = Scraping()

for estilo in estilos:
    a.getStilosMusicais(estilo)


df = pd.DataFrame(a.letras)
df.to_csv('letras.csv', index=False)



