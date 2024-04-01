# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsView, QGraphicsScene
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap


from dotenv import load_dotenv
load_dotenv()

import openai



import requests
import json

import base

global_var = 0

dificuldade_escolhido = ''
tema_escolhido = ''
contagem_regressiva_ativa = False

linkFoto_gpt = ''
textoResposta_gpt = ''

class Janela(QtWidgets.QMainWindow, base.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Janela, self).__init__(parent)
        self.setupUi(self)
        #componentes qt designer
        self.startGameButton.clicked.connect(self.proxima_pagina)
        self.continueGame1Button.clicked.connect(self.verificarRadioButton)
        self.continueGame2Button.clicked.connect(self.proxima_pagina)
        self.resetGame1Button.clicked.connect(self.resetTema)
        self.testeButton_2.clicked.connect(self.testeFunction)
        
        # Define o tamanho mínimo e máximo da janela
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        
        self.valor_atual = 30  # Valor inicial do QLCDNumber
        self.lcdNumber.display(self.valor_atual) 
                
        #tema_escolhido
        

        # Carregar a imagem a partir do link da web
        #pixmap = QPixmap()
        #pixmap.loadFromData(requests.get('https://avatars.githubusercontent.com/u/58015799?s=96&v=4').content)
        
        #colocar essa imagem nessa label => imgLabel
        #self.imgLabel.setPixmap(pixmap)
        #self.setCentralWidget(self.imgLabel)

          
    
    def proxima_pagina(self):
        indice_atual = self.stackedWidget.currentIndex()
        proximo_indice = (indice_atual + 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(proximo_indice)
       
    def pagina_anterior(self):
        indice_atual = self.stackedWidget.currentIndex()
        indice_anterior = (indice_atual - 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(indice_anterior)
    
    
    
    def iniciar_contagem_regressiva(self):
        global contagem_regressiva_ativa
        contagem_regressiva_ativa = True
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.atualizar_lcd)
        self.timer.start(1000)  # 1000 ms = 1 segundo

    def atualizar_lcd(self):
        global contagem_regressiva_ativa
        if contagem_regressiva_ativa:
            self.valor_atual -= 1
            self.lcdNumber.display(self.valor_atual)
            if self.valor_atual == -1:
                self.timer.stop()
                self.proxima_pagina()

    def resetTema(self):
        global contagem_regressiva_ativa
        contagem_regressiva_ativa = False
        self.valor_atual = 30
        self.lcdNumber.display(10)
        self.pagina_anterior()
        self.pagina_anterior()
        
    
    def testeFunction(self):
        try:
            #saber quais são os apis disponiveis do openAI
            ''' headers = {"Authorization": f"Bearer {os.getenv('API_KEY_GPT')}"}
            link = "https://api.openai.com/v1/models"
            requisicao = requests.get(link, headers=headers)
            print(requisicao) 
            print(requisicao.text)  '''
            
            
            #Fazer um teste com o chatgpt 3.5
            ''' headers = {"Authorization": f"Bearer {os.getenv('API_KEY_GPT')}", "Content-Type": "application/json"}
            link = "https://api.openai.com/v1/chat/completions"
            id_modelo = "gpt-3.5-turbo"
            body_mensagem = {
                "model": id_modelo,
                "messages": [{"role": "user", "content": "Me fala a historia do time Vasco da Gama"}]
            }
            body_mensagem = json.dumps(body_mensagem)
            requisicao = requests.post(link, headers=headers, data=body_mensagem)
            print(requisicao) 
            print(requisicao.text)
            
            resposta = requisicao.json()
            mensagem = resposta['choices'][0]['message']['content']
            print('\nMENSAGEM: ', mensagem) '''
            
            
            # Defina a chave da API
            ''' openai.api_key = os.getenv("API_KEY_GPT")

            # Crie uma completude de chat usando a nova interface
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "Gerar tópicos com o que pode ser usado no OpenAI."}
                ]
            )
            
            print(response) 
            # Imprima a mensagem gerada
            print(response["choices"][0]["message"]["content"]) '''
            
            #pesquisa = 'Imagem com muitos detalhes de uma cena de filme famoso.'
            pesquisa = 'Uma cena icônica de um filme de aventura e fantasia, onde um grupo de heróis está em pé no topo de uma montanha alta e nebulosa. Eles estão em uma pose épica, olhando para o horizonte com determinação. O céu está dramático, com nuvens escuras se movendo rapidamente, sugerindo uma tempestade iminente. A paisagem ao redor é selvagem e desolada, com picos de montanhas afiados e rochosos. A luz do sol brilha através das nuvens, iluminando os heróis e criando um contraste dramático entre luz e sombra.'
            #openai.api_key = os.getenv("API_KEY_GPT")
            
            
            #GERAR O LINK DA IMAGEM CRIADA
            '''
            openai.api_key = os.getenv("API_KEY_GPT") 
            pesquisa = 'Uma cena icônica de um filme de aventura e fantasia, onde um grupo de heróis está em pé no topo de uma montanha alta e nebulosa. Eles estão em uma pose épica, olhando para o horizonte com determinação. O céu está dramático, com nuvens escuras se movendo rapidamente, sugerindo uma tempestade iminente. A paisagem ao redor é selvagem e desolada, com picos de montanhas afiados e rochosos. A luz do sol brilha através das nuvens, iluminando os heróis e criando um contraste dramático entre luz e sombra.'
            response = openai.Image.create(
                model="dall-e-3",
                prompt= pesquisa,
                n=1,
                #size="256x256",
            )
            print(response["data"][0]["url"]) '''
            
            
            
            
            
            #COMO PEGAR A URL DA IMAGEM E DESCREVE-LA
            openai.api_key = os.getenv("API_KEY_GPT")
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Descreva com poucos detalhes essa imagem"},
                            {
                                "type": "image_url",
                                "image_url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-a7nJnxol4sZg5gqJerbC0SbC/user-F3R37SBCEmWhMOx9ODh5pnWz/img-bIDPMdxQmQ8TChHhluRLP2Pz.png?st=2024-04-01T13%3A35%3A12Z&se=2024-04-01T15%3A35%3A12Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-04-01T01%3A35%3A39Z&ske=2024-04-02T01%3A35%3A39Z&sks=b&skv=2021-08-06&sig=0kZT591PYGbdm0N4mfBC42tPBO2%2BijsXGhECUV4Mj8A%3D",
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            
            #linkFoto_gpt = ''
            #textoResposta_gpt = ''

            print(response.choices[0])
            print('\n\nRESPOSTAAA: ',response["choices"][0]["message"]["content"])
            


            
            
        except Exception as e:
            print(f'Erro de conexão: ', {e})
    
    
    
    
    def verificarRadioButton(self):
        global dificuldade_escolhido
        global tema_escolhido
        
        global linkFoto_gpt
        global textoResposta_gpt
                
        dificuldade_escolhido = None
        tema_escolhido = None
        
        linkFoto_gpt = None
        textoResposta_gpt = None

        # Verifica a dificuldade escolhida
        if self.radioButton_facil.isChecked():
            dificuldade_escolhido = 'facil'
        elif self.radioButton_dificil.isChecked():
            dificuldade_escolhido = 'dificil'

        # Verifica o tema escolhido
        temas_radio_buttons = {
            'Futebol': self.radioButton_futebol,
            'Filme': self.radioButton_filme,
            'Alimento': self.radioButton_alimento,
            'Anime': self.radioButton_anime,
            'Bandeira': self.radioButton_bandeira,
            'Artista': self.radioButton_artista,
            'Ferramenta': self.radioButton_ferramenta,
            'Cor': self.radioButton_cor
        }

        for tema, radio_button in temas_radio_buttons.items():
            if radio_button.isChecked():
                tema_escolhido = tema
                break

        if dificuldade_escolhido is None or tema_escolhido is None:
            msg = QMessageBox()
            msg.setWindowTitle('ERRO')
            msg.setText("Selecione as opções corretamente.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            
        else:
            self.proxima_pagina()
            self.gptData()
            
            
    def gptData(self):
        try:
            #logica gpt
            openai.api_key = os.getenv("API_KEY_GPT")
            
            #pegar imagem
            if dificuldade_escolhido == 'facil':
                pesquisa = f"Gere uma imagem com pouco detalhe e fácil entendimento que tenha tema {tema_escolhido}, sem direitos autorais"
                print('facil')
            else:
                pesquisa = f"Gere uma imagem com muito detalhe que tenha tema {tema_escolhido}, sem direitos autorais"
                print('dificil') 
                
            responseImg = openai.Image.create(
                model="dall-e-3",
                prompt= pesquisa,
                n=1,
            )
            print('\nURL DA IMAGEM GERADA: ',responseImg["data"][0]["url"])
            linkFoto_gpt = responseImg["data"][0]["url"]
            
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(linkFoto_gpt).content)
            self.imgLabel.setPixmap(pixmap)
            
            
            #analisar a imagem e pegar a resposta do gpt
            if dificuldade_escolhido == 'facil':
                pesquisa = "Descreva as coisas concretas com pouco detalhe, sucinto e fácil entendimento essa imagem"
                print('facil')
            else:
                pesquisa = "Descreva as coisas concretas com muito detalhes"
                print('dificil') 
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Descreva com poucos detalhes essa imagem"},
                            {
                                "type": "image_url",
                                "image_url": linkFoto_gpt,
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )

            print(response.choices[0])
            print('\n\nRESPOSTAAA: ',response["choices"][0]["message"]["content"])
            textoResposta_gpt = response["choices"][0]["message"]["content"]
            
    
        
            self.tema_escolhido.setText('Tema escolhido: '+tema_escolhido)
            
            
            self.proxima_pagina()
            self.iniciar_contagem_regressiva()
                

        except Exception as e:
            print('EROOO GPT: ', e)
            msg = QMessageBox()
            msg.setWindowTitle('ERRO')
            msg.setText("Problemas ao se conectar ao gpt.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.pagina_anterior()
                

            
def main(): 
    
    app = QApplication(sys.argv)
    form = Janela()
    #form = HomePage()
    form.show()
    app.exec_()      

if __name__ == '__main__':
    main()