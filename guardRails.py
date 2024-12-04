from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard
#from guardrails_api_client import Guard

# Carregando variáveis de ambiente, se necessário
load_dotenv()


# Definição do modelo
class Analista(BaseModel):
    Vitórias: str = Field(description="Pesquise na Web e informe em um pequeno paragrafo quantas vitórias o atlético mineiro teve em 2024")
    Gols: str = Field(description="Pesquise na Web e informe quantos gols o jogador hulk do atlético mineiro fez em 2024")


# prompt modificado para pedir uma análise de futebol
prompt = """

    Você é um analista de desempenho de futebol da Universidade de Harvard, com doutorado em ciência do esporte e estatística. Você combina conhecimento avançado em estatísticas e análise de dados com experiência profissional na área de futebol, aplicando métodos quantitativos à análise do desempenho das equipes e jogadores, bem como ao desenvolvimento de estratégias táticas e de treinamento eficazes.

    ${gr.complete_json_suffix_v2}
"""
guard = Guard.for_pydantic(output_class=Analista)

# Simulação de interação com o modelo de IA
res = guard(model="gpt-4o-mini", messages=[{"role": "user", "content":prompt}]
)

# Exibindo a saida validada
print(f"Recomendação do analista: {res.validated_output}")
