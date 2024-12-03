from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard

# Carregando variáveis de ambiente, se necessário
load_dotenv()


# Definição do modelo para um prato culinário
class analista_Futebol(BaseModel):
    Vitórias: str = Field(description="Quantas vitórias o jogador teve em 2024")
    Gols: str = Field(description="Quantos gols o jogador fez em 2024")


# prompt modificado para pedir uma recomendação e prato culinário
prompt = """
    Você é um analista de desempenho de futebol da Universidade de Harvard, com doutorado em ciência do esporte e estatística. Você combina conhecimento avançado em estatísticas e análise de dados com experiência profissional na área de futebol, aplicando métodos quantitativos à análise do desempenho das equipes e jogadores, bem como ao desenvolvimento de estratégias táticas e de treinamento eficazes.


    ${gr.complete_json_suffix_v2}
"""
guard = Guard.for_pydantic(output_class=analista_Futebol)

# Simulação de interação com o modelo de IA
res = guard(
    model="gpt-4o-mini-2024-07-18", message=[{"role": "user", "content": prompt}]
)

# Exibindo a saida validada
print(f"Recomendação do analista: {res.validated_output}")
