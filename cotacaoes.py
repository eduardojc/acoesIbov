# Autor: Eduaro José Christofoletti
# Data da Criação: 17/11/2020
# Email: duh19rc@gmail.com

from urllib.request import urlopen
from datetime import datetime
from pandas import DataFrame
import json
import os.path


# array de ações a serem avaliadas
aval = ['BCFF11','BRCR11','HGRU11','ENAT3','ITSA4','KNRI11','MXRF11','SAPR4','TAEE4','TIET4','XPML11']

# inicia uma lista.    
acao = []

# percorrer as ações coletando os JSON's
print("Atualizando: \n")
for res in range(len(aval)):
    url = urlopen('http://cotacao.b3.com.br/mds/api/v1/instrumentQuotation/'+aval[res])
    result = url.read()
    data = json.loads(result)
    
    if(data['BizSts']['cd'] == 'OK'):
        # Ramos do JSON a serem analisados.
        ramo1 = data['Trad'][0]['scty']
        ramo2 = ramo1['SctyQtn']
        print(ramo1['symb'])
    # Verifica se tem cotação para a ação selecionada

        
        # Pega a data do DIC do JSON da ação.
        dia = data['Msg']['dtTm']
        # Converter str em data e mudar o formato para Brasileiro
        dia = datetime.strptime(dia, "%Y-%m-%d %H:%M:%S").strftime('%d/%m/%Y %H:%M:%S')
        
        # Percorrer o DIC e atribuir as variáveis:
        # name = Nome da Ação, minPr = Preço Min
        # maxPr = Preço Max, avrPr = Preço Médio
        # curPr = Preço Atual
        name = ramo1['symb'] 
        minPr = ramo2['minPric']
        maxPr = ramo2['maxPric']
        avrPr = ramo2['avrgPric']
        curPr = ramo2['curPrc']
        
        #depois do loop adiciona a busca ao array de 'acao' pelo método append
        acao.append([dia,name,minPr,maxPr,avrPr,curPr])
        
## Transformamos os dados em um DATAFRAME para inserir o Header
## Em Seguida verificamos se o Arquivo analise.txt Existe,
## Se não existir ele cria um nova arquivo com as cotações "hora atual"
## Caso existir ele atualiza o arquivo com as cotações da "hora atual"

df = DataFrame(acao,columns=['Data','Acao','Min','Max','Med','Atual'])
file = 'D:\\Analise\\analise.csv' #caminho onde será salvo o arquivo.

print('\n')
if os.path.isfile(file):
    # Abre o arquivo e salva em TXT
    df.to_csv(file, header=None, index=None, sep=',', mode='a')
    print("Arquivo Atualizado!")
else: 
    df.to_csv(file, header=True, index=None, sep=',', mode='w+')
    print("Arquivo Criado!")


