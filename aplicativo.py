from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard
from collections import Counter
import re


# Carregando variáveis de ambiente, se necessário
load_dotenv()


# Definição do modelo
class Analista(BaseModel):
    Carro: str = Field(description="Quais modelos de carros mais roubados em 2024?")
    Gênero: str = Field(
        description="Pesquise na Web e destaque em um pequeno parágrafo qual o gênero das pessoas que mais possuem carros furtados"
    )
    História: str = Field(
        description="Conte a história de um roubo em um parágrafo longo contento as informações dos campos: Carro e Gênero"
    )


# Prompt modificado para pedir uma análise de roubo
prompt = """
    Você é uma vítima de roubo de veículo quando teve sua propriedade pessoal, especificamente seu carro, levada sem o consentimento seu. Isso pode acontecer em qualquer lugar e a qualquer momento, tornando-se uma situação de grande estresse emocional para quem passa por isso. Você pode se sentir perdida e impotente diante da perda do veículo, que geralmente representa mais do que apenas um objeto material - é uma ferramenta essencial para a vida cotidiana, como meio de transporte, ferramenta de trabalho ou simplesmente uma parte importante da identidade pessoal. Além disso, o roubo de um carro pode também ter consequências práticas significativas, incluindo perda de tempo e esforço em tentar recuperar o veículo, possíveis danos financeiros decorrentes do furto (como seguro) e impacto na rotina diária.

    ${gr.complete_json_suffix_v2}
"""
guard = Guard.for_pydantic(output_class=Analista)


# Função para extrair palavras-chave do texto
def extrair_palavras_chave(texto):
    # Remove pontuações e converte para minúsculas
    palavras = re.findall(r"\b\w+\b", texto.lower())
    # Lista de palavras irrelevantes (stop words)
    stop_words = {
        "a",
        "de",
        "o",
        "e",
        "do",
        "da",
        "os",
        "as",
        "que",
        "é",
        "em",
        "um",
        "uma",
        "para",
        "com",
        "ao",
        "por",
        "se",
        "no",
        "na",
        "dos",
        "das",
        "mas",
        "foi",
    }
    # Remove stop words e retorna palavras significativas
    palavras_significativas = [
        palavra for palavra in palavras if palavra not in stop_words
    ]
    return Counter(palavras_significativas).most_common(
        50
    )  # Retorna as 50 palavras mais frequentes


try:
    # Simulação de interação com o modelo de IA
    res = guard(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])

    if res.validated_output:
        print("=" * 50)
        print("📋 Resultado Gerado pelo Modelo")
        print("=" * 50)

        # Exibição formatada dos resultados
        print("\n🔹 Modelos de Carros Mais Roubados:")
        print(f"   {res.validated_output['Carro']}\n")

        print("🔹 Gênero Mais Afetado:")
        print(f"   {res.validated_output['Gênero']}\n")

        print("🔹 História do Roubo:")
        print(f"   {res.validated_output['História']}\n")

        print("=" * 50)

        # Combina textos dos campos para gerar palavras-chave
        texto_completo = (
            res.validated_output["Carro"]
            + " "
            + res.validated_output["Gênero"]
            + " "
            + res.validated_output["História"]
        )

        # Gera palavras-chave
        palavras_chave = [
            palavra for palavra, _ in extrair_palavras_chave(texto_completo)
        ]
        print("📌 Palavras-chave Extraídas do Contexto:")
        print(", ".join(palavras_chave))
        print("=" * 50)

        # Loop contínuo para capturar entrada do usuário
        while True:
            user_input = input(
                "\n✏️ Por favor, insira o relato da testemunha ou digite 'sair' para encerrar: "
            )

            # Verifica se o usuário deseja sair
            if user_input.strip().lower() == "sair":
                print("🛑 Encerrando o programa. Obrigado!")
                break

            # Gera palavras do usuário
            palavras_usuario = [
                palavra for palavra, _ in extrair_palavras_chave(user_input)
            ]

            # Calcula palavras comuns
            palavras_comuns = set(palavras_chave) & set(palavras_usuario)

            # Calcula porcentagem de veracidade
            if len(palavras_chave) > 0:
                porcentagem_veracidade = (
                    len(palavras_comuns) / len(palavras_chave)
                ) * 100
            else:
                porcentagem_veracidade = 0

            print("\n✅ Palavras em Comum:")
            print(", ".join(palavras_comuns))
            print("\n📊 Porcentagem de Veracidade:")
            print(f"   {porcentagem_veracidade:.2f}%")

            if porcentagem_veracidade < 30:
                print(
                    "❌ O assunto informado pelo testemunha não está relacionado ao contexto da vítima."
                )
            else:
                print(
                    "✔️ Texto válido! O relato da testemunha está relacionado ao assunto gerado."
                )
    else:
        print("⚠️ Os dados retornados não são válidos.")

except Exception as e:
    print(f"⚠️ Você está no bloco Except: {e}")
