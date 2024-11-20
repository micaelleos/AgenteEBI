
import streamlit as st
from src.EBIagent import EBIagent
from styles import *
import os
from gerador_pdf import *
from textos import info

styles()


@st.dialog("Assistente de EBI")
def modal():
    tab1, tab2 = st.tabs([":gear: Configurações",":bulb: Informações"])
    with tab2:
        st.markdown(info)
    with tab1:
        st.markdown("## Configurações")
        
        base_fe = st.radio(
            "Qual a base de fé?",
            ["Batista","Presbiteriana","Pentecostal","Católico"],
            horizontal=True,
            index=("Batista","Presbiteriana","Pentecostal","Católico").index(st.session_state.params["base_fe"])  # mantém o valor anterior
        )
        versao_biblia = st.selectbox("Qual a versão da bíblia?",
                                     ("Nova Versão Internacional (NVI)",
                                      "Almeida Revista e Corrigida (ARC)",
                                      "Nova Tradução na Linguagem de Hoje (NTLH)",
                                      "Bíblia Viva",
                                      "King James"),
                                      placeholder="Escoha uma opção...",
                                      index=("Nova Versão Internacional (NVI)",
                                      "Almeida Revista e Corrigida (ARC)",
                                      "Nova Tradução na Linguagem de Hoje (NTLH)",
                                      "Bíblia Viva",
                                      "King James").index(st.session_state.params["versao_biblia"])
                                      )
        colz = st.columns([0.5,0.5])
        with colz[0]:
            publico = st.radio(
            "Qual o público-alvo?",
            ["Jovens",
            "Adultos",
            "Novos Convertidos",
            "Líderes de Grupos",
            "Crianças",
            "Família"],
            index=("Jovens",
            "Adultos",
            "Novos Convertidos",
            "Líderes de Grupos",
            "Crianças",
            "Família").index(st.session_state.params["publico"])
             )
        with colz[1]:
            lingagem = st.radio(
            "Qual o tipo de linguagem?",
            ["Simples e direta",
             "Formal",
            "Informal",
            "Poética",
            "Acadêmica",],
            index=("Simples e direta",
             "Formal",
            "Informal",
            "Poética",
            "Acadêmica").index(st.session_state.params["lingagem"])
             )
            
        if st.button("Salvar"):
            st.session_state.params["base_fe"] = base_fe
            st.session_state.params["versao_biblia"] = versao_biblia
            st.session_state.params["publico"] = publico
            st.session_state.params["lingagem"] = lingagem
            st.rerun()

@st.fragment
def atualizar_chat(chat_container,prompt=None):
    with chat_container:
        if not prompt:
            initial_message = st.chat_message("assistant")
            initial_message.write("Olá, como posso ajudá-lo hoje?")
        messages = st.session_state.messages

        for i in range(0,len(messages)):
            message = messages[i]       
                                
            if message['role'] == "assistant":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])    

        if prompt:
            with st.chat_message("assistant"):
                with st.spinner(""): 
                    response=chat.chat_agent(prompt)
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


if "messages" not in st.session_state:
    st.session_state.messages = []

if "ebi" not in st.session_state:
    st.session_state.ebi = None

if "params" not in st.session_state:
    st.session_state.params = {}
    st.session_state.params["base_fe"] = "Batista"
    st.session_state.params["versao_biblia"] = "Nova Versão Internacional (NVI)"
    st.session_state.params["publico"] = "Jovens"
    st.session_state.params["lingagem"] = "Simples e direta"

chat = EBIagent(st.session_state.params)

with st.container():
    
    with st.container():
        col1, col2 = st.columns([0.8,0.2])
        with col1:
            st.title("Assistente de EBI")
        with col2:
            subcol =st.columns([0.9,0.3]) 
            with subcol[1]:
                if st.button(":gear:",use_container_width=True): #:information_source: :receipt:
                    modal()

    
    col11, col22 = st.columns([0.5,0.5])
    with col22:
        with st.container(border=False):
            chat_container = st.container(height=400,border=False)
            atualizar_chat(chat_container)

            if prompt:= st.chat_input("Faça um estudo bíblico sobre ...",key="user_input"):
        
                st.session_state.messages.append({"role": "user", "content": prompt})
                atualizar_chat(chat_container,prompt)
                
    with col11:        
        if st.session_state.ebi:
            with st.expander("Ver Estudo Bíblico Indutivo",expanded=True):
                st.markdown("## "+st.session_state.ebi['title'])
                st.markdown(st.session_state.ebi['plaintext_base'])
                st.markdown("**Perguntas**")
                st.markdown(st.session_state.ebi['description'])
                st.markdown("**Para refletir:**")
                st.markdown("*"+st.session_state.ebi['footer']+"*")
        else:
            with st.expander("Ver Estudo Bíblico Indutivo",expanded=False):
                st.markdown("*Solicite um estudo bíblico...*")
        with st.container(border=False):
            colsx = st.columns([0.3,0.3,0.3])
            with colsx[0]:
                pass
            with colsx[1]:
                if st.session_state.ebi:
                    file_a4,nome_a4 = impressão_a4(st.session_state.ebi)
                    st.download_button(label="Impressão A4 🖨️",
                                       type="primary",
                                       data=file_a4,
                                       file_name=nome_a4,
                                       mime="application/pdf",
                                       use_container_width=True)
            with colsx[2]:
                if st.session_state.ebi:
                    file_mobile, nome_mobile = impressão_mobile(st.session_state.ebi)
                    st.download_button(label="Layout móvel 📱",
                                       type="primary",
                                       data=file_mobile,
                                       file_name=nome_mobile,
                                       mime="application/pdf",
                                       use_container_width=True)