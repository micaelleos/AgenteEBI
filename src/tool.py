from typing import Optional, Type, List
from pydantic import  Field
from pydantic import BaseModel
from langchain_core.tools import BaseTool
from langchain.agents import tool
import streamlit as st


class ExibirEBI(BaseModel):
    title: str = Field(description="Título do EBI, relevante e resumido em poucas palavras")
    plaintext_base: str = Field(description="Texto base corrido, com versículos e referências.")
    description: str = Field(description="10 Perguntas de observação, interpretação e aplicação, listadas em ordem numérica")
    footer: str = Field(description="Versículos de reflexão final, em texto corrido")
    

@tool(args_schema=ExibirEBI)
def exibir_ebi(**dict:ExibirEBI) -> dict:
    """Chame essa função para exibir o EBI ao usuário"""
    try:
        st.session_state.ebi = dict
        print(dict)
        return "exibido com sucesso"
    except:
        return "aconteceu um erro ao exibir o EBI"
    


if __name__=="__main__":
    pass