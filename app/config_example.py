# app/config_example.py
#
# Copie este arquivo para config.py e preencha com sua chave de API.
# NÃO COMITE o arquivo config.py com a chave em repositórios públicos.

import os

# Você pode configurar a chave via variável de ambiente:
#   export OPENAI_API_KEY="sua_chave"
# ou preencher manualmente aqui (apenas localmente).

API_KEY = os.getenv("OPENAI_API_KEY", "SUA_CHAVE_AQUI")

# Modelo recomendado para chatbot educacional
MODEL_NAME = "gpt-4.1-mini"
