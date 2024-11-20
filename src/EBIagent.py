import os
from typing import List, Literal
from pydantic import BaseModel, Field
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.schema.runnable import RunnablePassthrough
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.prompts import MessagesPlaceholder
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain.prompts import ChatPromptTemplate

from langchain.memory import ConversationBufferMemory

from src.tool import exibir_ebi


@st.cache_resource()
def memory():
    memory = ConversationBufferMemory(return_messages=True,memory_key="chat_history")
    return memory

class EBIagent:
    def __init__(self,params):

        self.OPENAI_API_KEY=os.getenv('OPEN_API_KEY') #pegar do .env
        self.model = ChatOpenAI(openai_api_key=self.OPENAI_API_KEY,temperature=0.5, model="gpt-4o")

        self.exibir_ebi = exibir_ebi

        self.model_with_tool = self.model.bind(functions=[convert_to_openai_function(self.exibir_ebi)])

        self.memory=memory()

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f""" Você é um especialista em teologia e em criação de estudo bíblico indutivo.
            Você constroe estudos bíblicos e exibe ao usuário por meio da ferramenta "exibir_ebi". Para construir o EBI você deve serguir as seguintes regras, e pense passo a passo:
            
            Regras gerais:
            1. Você deve auxilixar o usuário a construir um EBI com base num texto bíblico.
            2. O estudo bíblico deve ser bem completo, com texto de referência, e com no mínimo 10 perguntas (Observação, interpretação e aplicação).
            3. Você deve sempre exibir o estudo bíblico, por meio da ferramenta "exibir_ebi".
            4. Todo EBI deve ser escrito no formato markdonw.
            5. No final de cada quebra de linha, deve haver um espaço.
            6. Você deve colocar o trecho do texto base no EBI. O texto base deve ter entre 5 a 15 versículos. O texto base não pode passar de 15 versículos. 
            7. Importante: Você deve SEMPRE MOSTRAR A REFERÊNCIA DA PASSAGEM BÍBLICA, ASSIM COMO A NUMERAÇÃO DOS VERSÍCULOS. Ex.: João 3.16 16.porque Deus amou o mundo de tal maneira, que deu seu filho...
            8. Importante: TODO VERSÍCULO DEVE SER ENUMERADO.
            9. A cada pergunta numerada do EBI, deve haver uma quebra de linha.
            10. Caso o usuário solicite mudanças no EBI você deve executá-la e sempre exibir o estudo bíblico com a modificação
            11. Importante: Na conversa, você não pode repetir o EBI para o usuário. SEMPRE EXIBA O EBI POR MEIO DA FERRAMENTA "exibir_ebi" !!!
            12. Importante: Os caracteres do texto do EBI deve ser compatível com "latin-1". Caso não sejam, substitua por outro semelhante e compatível !!!
            
            Parâmetros do EBI:  
            1. Sua base bíblica é {params["base_fe"]}.
            2. As perguntas devem ser escrcitas em linguagem {params["lingagem"]}.
            3. Você cria estudo bíblicos voltados para {params["publico"]}.
            4. O texto base deve estar na versão da bíblia: {params["versao_biblia"]}
            
            """),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        self.agent_chain = RunnablePassthrough.assign(
            agent_scratchpad= lambda x: format_to_openai_functions(x["intermediate_steps"])
        ) | self.prompt | self.model_with_tool | OpenAIFunctionsAgentOutputParser()

        self.agent_executor = AgentExecutor(agent=self.agent_chain, tools=[self.exibir_ebi], verbose=True, memory=self.memory,handle_parsing_errors=True)

    def chat_agent(self,query):    
        response=self.agent_executor.invoke({'input':query})
        return response['output']
    