from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard

import re
from collections import Counter

# Carregando variáveis de ambiente, se necessário
load_dotenv()


# Definição do modelo
class Analista(BaseModel):
    CopaDoMundo: str = Field(description="Quem venceu a Copa do Mundo de 2022?")
    SeleçãoArgentinaDeFutebol: str = Field(
        description="Pesquise na Web e destaque em um pequeno parágrafo quais os pontos fortes e fracos do time: Seleção Argentina de Futebol"
    )
    SeleçãoBrasileiraDeFutebol: str = Field(
        description="Pesquise na Web e destaque em um pequeno parágrafo quais os pontos fortes e fracos do time: Seleção Brasileira de Futebol"
    )


# Prompt modificado para pedir uma análise de futebol
prompt = """
    Você é um técnico da seleção brasileira de futebol, formado em Educação Física e com uma rica experiência como atleta profissional de futebol. Após concluir seus estudos na área de educação física, você desenvolveu sua carreira como jogador por sete temporadas consecutivas, desempenhando papéis importantes em equipes de alta competição. Essa combinação única de formação acadêmica e experiência no futebol profissional proporcionou a você uma compreensão profunda do jogo, permitindo que você identifique e desenvolva estratégias eficazes para impulsionar os atletas da seleção brasileira.

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
    }
    # Remove stop words e retorna palavras significativas
    palavras_significativas = [
        palavra for palavra in palavras if palavra not in stop_words
    ]
    return Counter(palavras_significativas).most_common(
        50
    )  # Retorna as 10 palavras mais frequentes


try:
    # Simulação de interação com o modelo de IA
    # raise ValueError("Simulação de erro para teste do bloco except")
    res = guard(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])

    if res.validated_output:
        print("Resultado gerado pelo modelo:")
        print(res.validated_output)

        # Combina textos dos campos para gerar palavras-chave
        texto_completo = (
            res.validated_output["CopaDoMundo"]
            + " "
            + res.validated_output["SeleçãoArgentinaDeFutebol"]
            + " "
            + res.validated_output["SeleçãoBrasileiraDeFutebol"]
        )

        # Gera palavras-chave
        palavras_chave = [
            palavra for palavra, _ in extrair_palavras_chave(texto_completo)
        ]
        print("Palavras-chave extraídas do contexto:", palavras_chave)

        # Loop contínuo para capturar entrada do usuário
        while True:
            user_input = input(
                "Por favor, insira um texto relacionado ao contexto ou digite 'sair' para encerrar: "
            )

            # Verifica se o usuário deseja sair
            if user_input.strip().lower() == "sair":
                print("Encerrando o programa. Obrigado!")
                break

            # Checar se o input do usuário contém palavras relacionadas ao contexto
            palavras_usuario = user_input.lower().split()
            contexto_relevante = any(
                palavra in palavras_usuario for palavra in palavras_chave
            )

            if not contexto_relevante:
                print(
                    "O assunto informado pelo usuário não está relacionado ao contexto do futebol."
                )
            else:
                print("Texto válido! O contexto está relacionado ao assunto gerado.")
    else:
        print("Os dados retornados não são válidos.")

except Exception as e:
    print(f"Você está no bloco Except: {e}")
