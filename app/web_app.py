# app/web_app.py

import sys, os

# Caminho do diretório atual (app/)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho da raiz do projeto
ROOT_DIR = os.path.dirname(CURRENT_DIR)

# Adiciona raiz ao PYTHONPATH
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

from core import get_client, chat_with_memory     # CORRIGIDO
from subjects import detect_subject               # CORRIGIDO


def init_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "client" not in st.session_state:
        st.session_state.client = get_client()


def main():
    st.set_page_config(
        page_title="Tutor de Matemática e Física",
        page_icon="📘",
    )

    init_session_state()

    st.title("📘 Tutor de Matemática e Física com IA")
    st.markdown(
        "Faça perguntas de Matemática e Física. "
        "O tutor responde passo a passo, com foco em entendimento conceitual."
    )

    with st.sidebar:
        st.header("Configurações")
        max_history = st.slider(
            "Tamanho da memória (número de mensagens anteriores)",
            min_value=2,
            max_value=30,
            value=10,
        )
        if st.button("Limpar conversa"):
            st.session_state.history = []
            st.success("Histórico limpo.")

    # Mostrar histórico
    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_message = st.chat_input("Digite sua pergunta de Matemática ou Física...")

    if user_message:
        with st.chat_message("user"):
            st.markdown(user_message)

        reply, new_history = chat_with_memory(
            client=st.session_state.client,
            history=st.session_state.history,
            user_message=user_message,
            max_history=max_history,
            source="web",
        )

        st.session_state.history = new_history

        with st.chat_message("assistant"):
            st.markdown(reply)


if __name__ == "__main__":
    main()
