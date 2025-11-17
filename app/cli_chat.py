# app/cli_chat.py

import sys, os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(ROOT_DIR)
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from app.core import get_client, chat_with_memory


def main():
    client = get_client()
    history = []

    print("=== Chatbot Educacional de Matemática e Física ===")
    print("Digite sua pergunta ou 'sair' para encerrar.\n")

    while True:
        user_message = input("Você: ").strip()
        if user_message.lower() in {"sair", "exit", "quit"}:
            print("Chatbot: Até mais! Bons estudos!")
            break

        if not user_message:
            continue

        reply, history = chat_with_memory(
            client=client,
            history=history,
            user_message=user_message,
            source="cli",
        )

        print("\nChatbot:", reply, "\n")


if __name__ == "__main__":
    main()
