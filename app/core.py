# app/core.py

import json
import os
from datetime import datetime
from typing import List, Dict

from openai import OpenAI

from .config import API_KEY, MODEL_NAME
from .pedagogical_profile import SYSTEM_PROMPT
from .subjects import detect_subject, build_subject_instruction


def get_client() -> OpenAI:
    api_key = API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API_KEY não configurada. Defina em config.py ou variável de ambiente.")
    return OpenAI(api_key=api_key)


def ensure_logs_dir():
    os.makedirs("logs", exist_ok=True)


def log_interaction(
    messages: List[Dict[str, str]],
    reply: str,
    subject: str,
    source: str = "cli",
):
    """
    Registra cada interação em um arquivo JSONL por dia.
    """
    ensure_logs_dir()
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_path = os.path.join("logs", f"chat_log_{date_str}.jsonl")

    entry = {
        "timestamp": datetime.now().isoformat(),
        "subject": subject,
        "source": source,
        "messages": messages,
        "reply": reply,
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def build_system_message(user_message: str) -> str:
    subject = detect_subject(user_message)
    subject_instruction = build_subject_instruction(subject)
    return SYSTEM_PROMPT + "\n\n" + subject_instruction, subject


def chat_with_memory(
    client: OpenAI,
    history: List[Dict[str, str]],
    user_message: str,
    max_history: int = 10,
    source: str = "cli",
) -> (str, List[Dict[str, str]]):
    """
    history: lista de mensagens no formato [{"role": "...", "content": "..."}]
    Retorna (resposta_do_bot, nova_history).
    """

    system_content, subject = build_system_message(user_message)

    # Construímos o contexto: system + histórico + nova mensagem
    messages = [{"role": "system", "content": system_content}]
    # limitamos o tamanho do histórico para não estourar contexto
    trimmed_history = history[-max_history:]
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )

    reply = response.choices[0].message.content.strip()

    # Atualiza histórico
    new_history = trimmed_history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply},
    ]

    # Logging
    log_interaction(messages=messages, reply=reply, subject=subject, source=source)

    return reply, new_history
