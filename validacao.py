from dotenv import load_dotenv
from pydantic import BaseModel, Field
from guardrails import Guard

# Carregando variáveis de ambiente, se necessário
load_dotenv()


# Definição do modelo para um prato culinário
class Prato(BaseModel):
    cozinha: str = Field(description="tipo de")
    prato: str = Field(description="Nome do prato recomendado")


# prompt modificado para pedir uma recomendação e prato culinário
prompt = """
    Eu gosto de: pizza, churrasco, shushi,
    Com base nas minhas preferencias, qual tipo de culinaria voce recomenda.

    ${gr.complete_json_suffix_v2}
"""
guard = Guard.for_pydantic(output_class=Prato)

# Simulação de interação com o modelo de IA
res = guard(
    model="gpt-4o-mini-2024-07-18", message=[{"role": "user", "content": prompt}]
)

# Exibindo a saida validada
print(f"Recomendação de prato: {res.validated_output}")
