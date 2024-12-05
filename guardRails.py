from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard

# Carregando variáveis de ambiente, se necessário
load_dotenv()

# Definição do modelo
class Analista(BaseModel):
    CopaDoMundo: str = Field(description="Quem venceu a última Copa do Mundo?")
    SeleçãoArgentinaDeFutebol: str = Field(description="Pesquise na Web e destaque em um pequeno parágrafo quais os pontos fortes e fracos do time: Seleção Argentina de Futebol")
    SeleçãoBrasileiraDeFutebol: str = Field(description="Pesquise na Web e destaque em um pequeno parágrafo quais os pontos fortes e fracos do time: Seleção Brasileira de Futebol")

# prompt modificado para pedir uma análise de futebol
prompt = """

    Você é um técnico da seleção brasileira de futebol, formado em Educação Física e com uma rica experiência como atleta profissional de futebol. Após concluir seus estudos na área de educação física, você desenvolveu sua carreira como jogador por sete temporadas consecutivas, desempenhando papéis importantes em equipes de alta competição. Essa combinação única de formação acadêmica e experiência no futebol profissional proporcionou a você uma compreensão profunda do jogo, permitindo que você identifique e desenvolva estratégias eficazes para impulsionar os atletas da seleção brasileira.

    ${gr.complete_json_suffix_v2}
"""
guard = Guard.for_pydantic(output_class=Analista)

# Simulação de interação com o modelo de IA
res = guard(model="gpt-4o-mini", messages=[{"role": "user", "content":prompt}]
)

# Exibindo a saida validada
print(f"Análise técnica: {res.validated_output}")