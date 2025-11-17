# app/core.py

import sys, os

# Caminho do diretório atual (app/)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminho do diretório raiz do projeto
ROOT_DIR = os.path.dirname(CURRENT_DIR)

# Garantir que o Python consiga importar "app"
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import json
from datetime import datetime
from typing import List, Dict

from openai import OpenAI

from config import API_KEY, MODEL_NAME   # CORRIGIDO
from subjects import detect_subject, build_subject_instruction   # CORRIGIDO
from pedagogical_profile import SYSTEM_PROMPT   # CORRIGIDO


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
):
    system_content, subject = build_system_message(user_message)

    messages = [{"role": "system", "content": system_content}]
    trimmed_history = history[-max_history:]
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
    )

    reply = response.choices[0].message.content.strip()

    new_history = trimmed_history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply},
    ]

    log_interaction(messages=messages, reply=reply, subject=subject, source=source)

    return reply, new_history
