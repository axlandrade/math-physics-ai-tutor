# Math AI Tutor

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)]()
[![OpenAI](https://img.shields.io/badge/OpenAI-API-black.svg)]()
[![CI](https://github.com/axlandrade/math-ai-tutor/actions/workflows/ci.yml/badge.svg)](https://github.com/axlandrade/math-ai-tutor/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Tutor educacional de Matemática e Física com interface web em Streamlit, memória curta de
conversa e respostas guiadas por um perfil pedagógico especializado.

Aplicação em produção:

https://math-tutor-ai.streamlit.app/

## Recursos

- Atendimento focado em Matemática e Física para Ensino Médio e início de graduação.
- Detecção simples de tema para ajustar a instrução pedagógica do modelo.
- Memória configurável de conversa na interface web.
- Registro local das interações em JSONL para auditoria e melhoria do produto.
- Interface web em Streamlit e interface de linha de comando.
- Configuração via variáveis de ambiente e arquivo `.env`.

## Arquitetura

![Arquitetura](math-ai-tutor.png)

| Arquivo | Responsabilidade |
| --- | --- |
| `core.py` | Orquestra mensagens, cliente OpenAI, memória, modelo e logs. |
| `web_app.py` | Interface web em Streamlit. |
| `cli_chat.py` | Interface de terminal para testes e uso local. |
| `subjects.py` | Heurísticas de detecção de Matemática, Física ou tema genérico. |
| `pedagogical_profile.py` | Prompt de sistema e regras pedagógicas do tutor. |

## Requisitos

- Python 3.10 ou superior.
- Chave da API da OpenAI.

## Configuração Local

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale o projeto:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Edite o `.env`:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-nano
LOGS_DIR=logs
```

## Execução

Interface web:

```bash
streamlit run web_app.py
```

Interface de terminal:

```bash
math-ai-tutor
```

Também é possível executar diretamente:

```bash
python cli_chat.py
```

## Qualidade

Rode lint e testes antes de publicar alterações:

```bash
ruff check .
pytest
```

O workflow de CI executa os mesmos passos a cada push para `main` e em pull requests.

## Variáveis de Ambiente

| Variável | Obrigatória | Padrão | Descrição |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Sim | - | Chave usada para autenticar na API da OpenAI. |
| `OPENAI_MODEL` | Não | `gpt-4.1-nano` | Modelo usado nas respostas do tutor. |
| `LOGS_DIR` | Não | `logs` | Diretório onde os arquivos JSONL de conversa são salvos. |

## Logs

Cada interação é salva em `logs/chat_log_YYYY-MM-DD.jsonl` com timestamp, tema detectado,
origem da conversa, mensagens enviadas ao modelo e resposta retornada.

Não faça commit de `.env` nem do diretório `logs/`.

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).

## Autor

Desenvolvido por **Axl Andrade**.
