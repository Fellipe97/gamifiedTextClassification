import openai
import numpy as np

openai.api_key = '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'


def get_embedding(text):
    try:
        # Gera embeddings para o texto usando a API com um modelo atualizado
        response = openai.Embedding.create(
            input=[text],
            model="text-embedding-ada-002"  # Substitua por um modelo válido conforme sua necessidade
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"Erro ao acessar a API da OpenAI: {e}")
        return None

def calcular_similaridade(embedding1, embedding2):
    # Calcula a similaridade de cosseno entre dois embeddings
    if embedding1 is not None and embedding2 is not None:
        cos_sim = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return cos_sim
    else:
        return 0  # Retorna 0 se algum dos embeddings não puder ser gerado

# Solicitar ao usuário que digite duas frases
frase1 = input("Insira a primeira frase: ")
frase2 = input("Insira a segunda frase: ")

# Obter embeddings para as frases
embedding1 = get_embedding(frase1)
embedding2 = get_embedding(frase2)

# Verificar se ambos embeddings foram gerados com sucesso antes de prosseguir
if embedding1 and embedding2:
    similaridade = calcular_similaridade(embedding1, embedding2)

    print('SIMILARIDADE: ', similaridade)
    # Normalização da similaridade para uma escala de 1 a 100
    nota_similaridade = (similaridade + 1) / 2 * 100

    print(f"A nota de similaridade é: {nota_similaridade:.2f}")
else:
    print("Não foi possível calcular a similaridade devido a um erro anterior.")