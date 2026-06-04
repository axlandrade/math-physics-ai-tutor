import json
from types import SimpleNamespace

from core import build_system_message, chat_with_memory, log_interaction


class FakeCompletions:
    def __init__(self) -> None:
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=" Resposta guiada. "))]
        )


class FakeClient:
    def __init__(self) -> None:
        self.chat = SimpleNamespace(completions=FakeCompletions())


def test_build_system_message_includes_subject_instruction() -> None:
    system_message, subject = build_system_message("Explique força resultante")

    assert subject == "physics"
    assert "FÍSICA" in system_message


def test_log_interaction_writes_jsonl(tmp_path) -> None:
    log_file = log_interaction(
        messages=[{"role": "user", "content": "oi"}],
        reply="olá",
        subject="generic",
        logs_dir=tmp_path,
    )

    payload = json.loads(log_file.read_text(encoding="utf-8"))
    assert payload["reply"] == "olá"
    assert payload["source"] == "cli"


def test_chat_with_memory_trims_history_and_logs(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    client = FakeClient()
    history = [
        {"role": "user", "content": "pergunta antiga"},
        {"role": "assistant", "content": "resposta antiga"},
        {"role": "user", "content": "pergunta recente"},
        {"role": "assistant", "content": "resposta recente"},
    ]

    reply, new_history = chat_with_memory(
        client=client,
        history=history,
        user_message="Explique derivada",
        max_history=2,
        logs_dir=tmp_path,
    )

    assert reply == "Resposta guiada."
    assert new_history == history[-2:] + [
        {"role": "user", "content": "Explique derivada"},
        {"role": "assistant", "content": "Resposta guiada."},
    ]
    assert client.chat.completions.last_request["model"] == "test-model"
    assert client.chat.completions.last_request["messages"][1:] == history[-2:] + [
        {"role": "user", "content": "Explique derivada"}
    ]
