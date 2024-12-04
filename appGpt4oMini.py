# Importação das bibliotecas necessárias
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurar a chave da API da OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError(
        "A chave da API 'OPENAI_API_KEY' não foi encontrada. Verifique o arquivo .env."
    )

# Inicializar o cliente da OpenAI
client = OpenAI(api_key=api_key)

# Histórico da conversa
conversation_history = [
    {
        "role": "system",
        "content": "Você é um técnico da seleção brasileira de futebol, formado em Educação Física e com uma rica experiência como atleta profissional de futebol. Após concluir seus estudos na área de educação física, você desenvolveu sua carreira como jogador por sete temporadas consecutivas, desempenhando papéis importantes em equipes de alta competição. Essa combinação única de formação acadêmica e experiência no futebol profissional proporcionou a você uma compreensão profunda do jogo, permitindo que você identifique e desenvolva estratégias eficazes para impulsionar os atletas da seleção brasileira.",
    }
]


def interact_with_gpt(user_input):
    """
    Função que interage com o GPT-4o-mini, enviando o histórico de conversas atualizado e recebendo a resposta.
    """
    # Adicionar a entrada do usuário ao histórico
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Solicitar uma conclusão do modelo
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=conversation_history
        )

        # Extrair a resposta do modelo
        response = completion.choices[0].message.content

        # Adicionar a resposta ao histórico
        conversation_history.append({"role": "assistant", "content": response})

        return response
    except Exception as e:
        return f"Ocorreu um erro ao interagir com o analista: {e}"


# Loop principal para interação do usuário
print(
    "Bem-vindo ao seu analista de desempenho de futebol! Digite suas perguntas ou 'sair' para finalizar."
)
while True:
    user_input = input("Usuário: ")
    if user_input.lower() == "Sair":
        print("Encerrando a conversa. Até logo!")
        break

    # Obter resposta do GPT-4o-mini
    response = interact_with_gpt(user_input)
    print(f"GPT: {response}")
