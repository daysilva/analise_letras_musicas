# Sobre:
Projeto da faculdade da matéria de análise de dados. Nesse trabalho é utilizada a tecnica de raspagem de dados para capturar frases de um site.
Após isso, faço uma analise de sentimentos dessa frase, sobre o quão positiva ou o quão negativa uma frase é. Para isso, a biblioteca TextBlob
é bem util. Utilizando ela podemos fazer o processamento de textos e obter o valor de polaridade de um texto.
Para cada texto que é processado, ela retorna um valor que pode ser negativo ou positivo. Frases de caráter positivo, tem valores a sima de 0.
E frases de caráter negativo, tem valores menores que 0:
<br>
  "lute por seus sonhos" -> 0.5
<br>
  "a vida é sem graça" -> -0.5

## como usar:
- instale as bibliotecas necessárias
- pip install bs4
- pip install pandas
- pip install textblob
- pip install dash
- pip install plotly

### depois execute no seu terminal:
- python3 main.py
- Acesse o link em seu navegador para ver os dashboards dessa análise
