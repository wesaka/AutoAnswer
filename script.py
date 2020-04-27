import requests
import urllib.parse
from bs4 import BeautifulSoup


def stripNonAlphaNum(text):
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
    answer = ''.join(filter(whitelist.__contains__, text)).lower()
    return answer


def findNewPage(look_for):
    # Primeiramente, normalizar o texto
    look_for = stripNonAlphaNum(look_for)

    # Essa é a função que usamos para achar uma página com o termo que queremos
    url = "https://www.googleapis.com/customsearch/v1/siterestrict?key=AIzaSyA-4u-TuTdp_bBSW7eLpEZHOF8OnOSnzFM&cx" \
          "=010610888733627239004:ebpsa1ezh80&q=\"%s\"" % urllib.parse.quote(look_for)

    response = requests.get(url=url)
    data = response.json()

    if data['searchInformation']['totalResults'] == '0':
        print("No data was found for this query")
        return -1

    for item in data['items']:
        normalized_snippet = stripNonAlphaNum(item['snippet'])
        found_index = normalized_snippet.find(look_for)

        if found_index > -1:
            # Achamos um match - entrar na página e obter as respostas que queremos
            # Retornamos o link da página
            return item['link']


def createListFromAnswers(text):
    # Criamos uma lista com todos os cards presentes na pagina para procurar pelas respostas
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html',
    }
    url = findNewPage(text)
    while url == -1 or url is None:
        try_again = input("Não foi encontrado nada para esse termo, deseja pesquisar novamente? (S ou N)\n")
        if try_again.lower() == "s":
            new_search = input("Digite o novo termo para pesquisar:\n")
            url = findNewPage(new_search)

        else:
            exit(0)

    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, features="html.parser")

    # Montamos uma lista vazia para os termos que acharemos nessa página
    cardslist = []

    for card in soup.find_all("div", attrs={"class": "SetPageTerm-content"}):
        per = card.find("a", attrs={"class": "SetPageTerm-wordText"}).text
        res = card.find("a", attrs={"class": "SetPageTerm-definitionText"}).text

        cardslist.append((per, res))

    return cardslist


def searchForAnswer(text, premade_list):
    # Essa é a função na qual realmente procuramos pela resposta dentro dos dados obtidos na pagina
    # Se achamos a resposta, retorna-la, senão, fazemos o processo novamente
    for item in premade_list:
        if text in stripNonAlphaNum(item[0]) or text in stripNonAlphaNum(item[1]):
            return item

    search_again = input("Essa resposta não foi encontrada nessa página, procurar novamente? (S ou N)\n")
    if search_again.lower() == 's':
        return -2

    else:
        return -1


# Ponto de entrada
def main():
    print("Falai pessoal, como ceis tão?\n\nEu criei esse programinha pra facilitar nossa vida, já que a gente não tá "
          "fazendo porra nenhuma certa mesmo, porque não deixar as coisas erradas mais fáceis?\n\nMODO DE USAR:\nO modo "
          "de uso é bem simples, copie a pergunta do cengage quando o programa pedir\nPra maximizar a probabilidade de "
          "achar a resposta, copie palavras inteiras apenas e evite copiar coisas como \"_\" que é quase certeza que vai "
          "dar merda.\nTente não colocar frases muito longas, que meu algoritmo de verificação tende a ficar confuso, "
          "pegue no máximo 15 ou 20 palavras.\nÉ MUITO IMPORTANTE que a frase seja contínua, não adianta nada pegar "
          "palavras do começo e do fim apenas por exemplo.\nIsso aqui depende da internet, então se você não estiver "
          "conectado também não vai achar nada.\n\nMuito sucesso pra você e que você consiga achar tudo o que está "
          "procurando.\n")

    termo = stripNonAlphaNum(input("Qual é o termo que se deseja procurar?\n"))
    lista = createListFromAnswers(termo)
    resposta = searchForAnswer(termo, lista)
    print(resposta[0])
    print(resposta[1])
    print("\n")

    while True:
        termo = stripNonAlphaNum(input("Qual é o termo que se deseja procurar?\n"))
        resposta = searchForAnswer(termo, lista)

        if resposta == -1:
            exit(0)

        elif resposta == -2:
            lista = createListFromAnswers(termo)
            resposta = searchForAnswer(termo, lista)

        print(resposta[0])
        print(resposta[1])
        print("\n")

main()