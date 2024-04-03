import os
from PyQt5 import QtCore, QtGui, QtWidgets

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QGraphicsView, QGraphicsScene
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap


from dotenv import load_dotenv
load_dotenv()

import openai

import time

import requests
import json

import base

import difflib

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

        self.startGameButton.clicked.connect(self.proxima_pagina)
        self.continueGame1Button.clicked.connect(self.verificarRadioButton)
        self.continueGame2Button.clicked.connect(self.proxima_pagina)
        self.resetGame1Button.clicked.connect(self.resetTema)
        self.valor_atual = 30
        self.lcdNumber.display(self.valor_atual)      
        self.textRespostaUser.setPlaceholderText('Digite a sua resposta...')
        self.validarResposta.clicked.connect(self.similaridade)
        self.restartButton.clicked.connect(self.restartGame)


        # Define o tamanho mínimo e máximo da janela
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
       
        
        
        
        
          
    
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
        self.timer.start(1000)


    def atualizar_lcd(self):
        global contagem_regressiva_ativa
        if contagem_regressiva_ativa:
            self.valor_atual -= 1
            self.lcdNumber.display(self.valor_atual)
            if self.valor_atual == -1:
                self.timer.stop()
                self.proxima_pagina()


    def resetTime(self):
        global contagem_regressiva_ativa
        contagem_regressiva_ativa = False
        self.valor_atual = 30
        self.lcdNumber.display(30)


    def resetTema(self):
        self.resetTime()
        self.pagina_anterior()
        self.pagina_anterior()
     
     
    #função para testar algumas coisas
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
  
    
    def restartGame(self):
        self.textRespostaUser.setText('')
        self.resetTime()
        self.proxima_pagina()
    
    
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
            msg = QMessageBox()
            msg.setWindowTitle('Carregando as informações do gpt.')
            msg.setText("Por favor espere a imagem ser gerada.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.gptData()
            
            
    def gptData(self):
        try:
            global textoResposta_gpt
            
            #logica gpt
            openai.api_key = os.getenv("API_KEY_GPT")
            ''' if dificuldade_escolhido == 'facil':
                pesquisa_imagem = f"Gere uma imagem com poucos detalhes, bastante suncito , com elementos concretos e fácil entendimento que tenha o tema {tema_escolhido}, sem direitos autorais"
                pesquisa_descricao = "Descreva as coisas concretas com pouco detalhe, bastante sucinto, texto pequeno e fácil entendimento dessa imagem"
            else:
                pesquisa_imagem = f"Gere uma imagem com muitos detalhes, com elementos concretos e que tenha tema {tema_escolhido}, sem direitos autorais"
                pesquisa_descricao = "Descreva as coisas concretas com muito detalhes dessa imagem" '''
                
            if dificuldade_escolhido == 'facil':
                pesquisa_imagem = f"Gere uma imagem com um unico objeto que represente o tema {tema_escolhido}, sem direitos autorais"
                pesquisa_descricao = "Descreva essa imagem com poucos detalhes, texto pequeno e fácil entendimento dessa imagem. Esse texto tem que ser pequeno."
            else:
                pesquisa_imagem = f"Gere uma imagem com alguns objetos que represente o tema  {tema_escolhido}, sem direitos autorais"
                pesquisa_descricao = "Descreva essa imagem com muitos detalhes e fácil entendimento dessa imagem."
            

            #a pesquisa da imagem no gpt    
            responseImg = openai.Image.create(
                model="dall-e-3",
                prompt= pesquisa_imagem,
                n=1,
            )
            print('\nURL DA IMAGEM GERADA: ',responseImg["data"][0]["url"])
            linkFoto_gpt = responseImg["data"][0]["url"]
            #linkFoto_gpt = 'https://avatars.githubusercontent.com/u/58015799?s=96&v=4'
            
            #setar a imagem no programa
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(linkFoto_gpt).content)
            self.imgLabel.setPixmap(pixmap)
            
            
            #analisar a imagem e pegar a resposta do gpt   
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": pesquisa_descricao },
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
            
            #textoResposta_gpt = 'Uma foto de perfil de um usuário com olhos verdes.' 
            self.resposta_gpt.setText(textoResposta_gpt)
    
            self.tema_escolhido.setText('Tema escolhido: '+tema_escolhido)
            
            self.resetTime()
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
          
                
    def similaridade(self):
        global textoResposta_gpt
        
        if self.textRespostaUser.toPlainText():
            self.resposta_usuario.setText(self.textRespostaUser.toPlainText())
            
            #fazer o teste de similaridade
            fraseUser = self.textRespostaUser.toPlainText()
            pontuacao = round(difflib.SequenceMatcher(None, textoResposta_gpt, fraseUser).ratio() * 10, 2)
            self.lcdNumber_2.display(pontuacao) 
            
            
            self.proxima_pagina()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('ERRO')
            msg.setText("Por favor, descreva a imagem observada.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
    

       
   
   
       
       
       
       
            
def main(): 
    
    app = QApplication(sys.argv)
    form = Janela()
    #form = HomePage()
    form.show()
    app.exec_()      

if __name__ == '__main__':
    main()