import json
import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from pedagogical_profile import SYSTEM_PROMPT
from subjects import build_subject_instruction, detect_subject

DEFAULT_MODEL = "gpt-4.1-nano"
DEFAULT_LOGS_DIR = "logs"
Message = dict[str, str]


load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY não configurada. Defina a variável de ambiente ou crie um .env."
        )
    return OpenAI(api_key=api_key)


def get_model_name() -> str:
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def ensure_logs_dir(logs_dir: str | Path | None = None) -> Path:
    log_path = Path(logs_dir or os.getenv("LOGS_DIR", DEFAULT_LOGS_DIR))
    log_path.mkdir(parents=True, exist_ok=True)
    return log_path


def log_interaction(
    messages: list[Message],
    reply: str,
    subject: str,
    source: str = "cli",
    logs_dir: str | Path | None = None,
) -> Path:
    logs_path = ensure_logs_dir(logs_dir)
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    log_file = logs_path / f"chat_log_{date_str}.jsonl"

    entry = {
        "timestamp": now.isoformat(),
        "subject": subject,
        "source": source,
        "messages": messages,
        "reply": reply,
    }

    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return log_file


def build_system_message(user_message: str) -> tuple[str, str]:
    subject = detect_subject(user_message)
    subject_instruction = build_subject_instruction(subject)
    return SYSTEM_PROMPT + "\n\n" + subject_instruction, subject


def chat_with_memory(
    client: OpenAI,
    history: list[Message],
    user_message: str,
    max_history: int = 10,
    source: str = "cli",
    logs_dir: str | Path | None = None,
) -> tuple[str, list[Message]]:
    system_content, subject = build_system_message(user_message)

    messages = [{"role": "system", "content": system_content}]
    trimmed_history = history[-max_history:]
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=get_model_name(),
        messages=messages,
    )

    content = response.choices[0].message.content
    reply = content.strip() if content else ""

    new_history = trimmed_history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": reply},
    ]

    log_interaction(
        messages=messages,
        reply=reply,
        subject=subject,
        source=source,
        logs_dir=logs_dir,
    )

    return reply, new_history
