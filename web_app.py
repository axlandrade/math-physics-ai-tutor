# app/web_app.py

import streamlit as st

from core import get_client, chat_with_memory
from subjects import detect_subject
from PIL import Image

def init_session_state():
    if "history" not in st.session_state:
        st.session_state.history = []
    if "client" not in st.session_state:
        st.session_state.client = get_client()

# Limitar largura do conteúdo e centralizar
st.markdown("""
    <style>
        .main {
            max-width: 900px;
            margin: auto;
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Math AI Tutor",
    page_icon="logo.png",
    layout="wide"
    )

def main():

    init_session_state()

    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("logo.png", width=250)
    with col2:
        st.title("Math & Physics AI Tutor")
        st.write("Desenvolvido por **Axl Andrade**")


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
