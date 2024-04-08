import os
from PyQt5 import QtCore, QtWidgets

import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPixmap

import numpy as np

from dotenv import load_dotenv
load_dotenv()

import openai

import requests

import base

import difflib


dificuldade_escolhido = ''
tema_escolhido = ''
contagem_regressiva_ativa = False

linkFoto_gpt = ''
textoResposta_gpt = ''

class Janela(QtWidgets.QMainWindow, base.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Janela, self).__init__(parent)
        self.setupUi(self)
        
        # Define o tamanho mínimo e máximo da janela
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        
        #Primeira tela
        self.startGameButton.clicked.connect(self.proxima_pagina)
        
        #Segunda tela
        self.continueGame1Button.clicked.connect(self.verificarRadioButton)
        
        #Terceira tela
        #carregamento
        
        #Quarta tela
        self.resetGame1Button.clicked.connect(self.resetTema)
        self.valor_atual = 30
        self.lcdNumber.display(self.valor_atual)      
        self.continueGame2Button.clicked.connect(self.proximaPaginaResetTimer)
        
        #Quinta tela
        self.textRespostaUser.setPlaceholderText('Digite a sua resposta...')
        self.validarResposta.clicked.connect(self.similaridade)
        
        #Sexta tela
        self.restartButton.clicked.connect(self.restartGame)
        


       
        
        
#Funções dos botões       
        
          
    #Funções para passar a pagina e retornar    
    def proxima_pagina(self):
        indice_atual = self.stackedWidget.currentIndex()
            
        proximo_indice = (indice_atual + 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(proximo_indice)
       
       
    def pagina_anterior(self):
        indice_atual = self.stackedWidget.currentIndex()
        indice_anterior = (indice_atual - 1) % self.stackedWidget.count()
        self.stackedWidget.setCurrentIndex(indice_anterior)
    
    
    
    #Funções para o cronometro rodar e resetar
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
            
            #ajudar a testar o retorno
            #print('\nURL DA IMAGEM GERADA: ',responseImg["data"][0]["url"])
            
            linkFoto_gpt = responseImg["data"][0]["url"]
            #linkFoto_gpt = 'https://avatars.githubusercontent.com/u/58015799?s=96&v=4' #pegar alguma foto estatica inves do gpt
            
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

            #ajudar a testar o retorno
            ''' print(response.choices[0])
            print('\n\nRESPOSTAAA: ',response["choices"][0]["message"]["content"]) '''
            textoResposta_gpt = response["choices"][0]["message"]["content"]
            
            #textoResposta_gpt = 'Uma foto de perfil de um usuário com olhos verdes.'  #pegar uma descrição estatica inves do gpt
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
    
    
        #Função para cancelar a imagem gerada e mudar o tema
    
    
    def resetTema(self):
        self.resetTime()
        self.pagina_anterior()
        self.pagina_anterior()
    
    
    def proximaPaginaResetTimer(self):
        self.resetTime()
        self.proxima_pagina()      
    
    
    def get_embedding(self, text):
        try:
            #logica gpt
            openai.api_key = os.getenv("API_KEY_GPT")
            
            # Gera embeddings para o texto usando a API com um modelo atualizado
            response = openai.Embedding.create(
                input=[text],
                model="text-embedding-ada-002"  # Substitua por um modelo válido conforme sua necessidade
            )
            return response['data'][0]['embedding']
        except openai.error.RateLimitError:
            print("Limite de quota excedido. Verifique seu plano e o uso da API.")
            return None
        except openai.error.OpenAIError as e:
            print(f"Erro ao acessar a API da OpenAI: {e}")
            return None


    def calcular_similaridade(self, embedding1, embedding2):
        # Calcula a similaridade de cosseno entre dois embeddings
        if embedding1 is not None and embedding2 is not None:
            cos_sim = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
            return cos_sim
        else:
            return 0  # Retorna 0 se algum dos embeddings não puder ser gerado
    
                
    def similaridade(self):
        global textoResposta_gpt
        
        if self.textRespostaUser.toPlainText():
            self.resposta_usuario.setText(self.textRespostaUser.toPlainText())
            
            #fazer o teste de similaridade
            fraseUser = self.textRespostaUser.toPlainText()
            
            # Obter embeddings para as frases
            embedding1 = self.get_embedding(textoResposta_gpt)
            embedding2 = self.get_embedding(fraseUser)
            
            #VERSÃO ANTIGA PORÉM FUNCIONA MAIS!!!!
            #pontuacao = round(difflib.SequenceMatcher(None, textoResposta_gpt, fraseUser).ratio() * 10, 2)
            
            # Verificar se ambos embeddings foram gerados com sucesso antes de prosseguir
            if embedding1 and embedding2:
                similaridade = self.calcular_similaridade(embedding1, embedding2)

                # Normalização da similaridade para uma escala de 1 a 100
                nota_similaridade = (similaridade + 1) / 2 * 100
                
                # Converter a nota para uma escala de 0 a 10
                nota_0_10 = nota_similaridade / 10

                print(f"A nota de similaridade é: {nota_0_10:.2f}")
                self.lcdNumber_2.display(nota_0_10) 
            else:
                print("Não foi possível calcular a similaridade devido a um erro anterior.")
                msg = QMessageBox()
                msg.setWindowTitle('ERROR')
                msg.setText("Não foi pssível se conectar ao servidor.Tente novamente.")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.pagina_anterior()
            
            
            
            self.proxima_pagina()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('ERRO')
            msg.setText("Por favor, descreva a imagem observada.")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
    

    def restartGame(self):
        self.textRespostaUser.setText('')
        self.resetTime()
        self.proxima_pagina()
       
   
   
       
       
       
       
            
def main(): 
    
    app = QApplication(sys.argv)
    form = Janela()
    form.show()
    app.exec_()      

if __name__ == '__main__':
    main()