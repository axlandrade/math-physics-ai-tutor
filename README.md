# 📘 **math-physics-ai-tutor**

### *Um Tutor Educacional de Matemática e Física baseado em IA*

Este repositório contém um **chatbot educacional de Matemática e Física**, desenvolvido com **OpenAI**, **Streamlit**, **Docker** e **Railway**.  
O objetivo é oferecer explicações **passo a passo**, com foco em clareza conceitual, rigor matemático e suporte a diferentes níveis de ensino.

A aplicação pode ser usada para:

- resolução de exercícios  
- explicação de conceitos matemáticos e físicos  
- ensino interativo  
- demonstrações acadêmicas  
- experimentação com IA generativa aplicada à educação  

---

# 🚀 **Demonstração Pública**

*(Adicione aqui a URL do Railway assim que fizer o deploy)*

👉 **URL pública:** _em breve_

---

# 🧠 **Principais Funcionalidades**

- Tutor especializado em **Matemática** e **Física**  
- Respostas **explicadas passo a passo**  
- Detecção automática da disciplina (Math/Física/Genérico)  
- Memória de conversa configurável  
- Logging em formato JSONL  
- Interface Web feita em **Streamlit**  
- Deploy profissional com **Docker + Railway**  
- Segurança via **variáveis de ambiente** (sem expor API key)

---

# 🧱 **Arquitetura do Projeto**

```
math-physics-ai-tutor/
│
├─ app/
│  ├─ core.py              # Chamada ao modelo, memória e logging
│  ├─ web_app.py           # Interface Streamlit
│  ├─ cli_chat.py          # Interface de terminal (opcional)
│  ├─ subjects.py          # Detecção de disciplina
│  ├─ pedagogical_profile.py
│  ├─ config_example.py
│  └─ config.py            # (local, não vai para o GitHub)
│
├─ logs/                   # logs locais (ignorados no deploy)
│
├─ requirements.txt
├─ Dockerfile
├─ railway.json
├─ .dockerignore
├─ .gitignore
└─ README.md
```

---

# 📦 **Instalação Local (Sem Docker)**

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/math-physics-ai-tutor
cd math-physics-ai-tutor
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Criar arquivo `.env`

Crie um arquivo chamado `.env` na raiz:

```
OPENAI_API_KEY=coloque_sua_chave_aqui
```

### 5. Rodar a versão Web

```bash
streamlit run app/web_app.py
```

---

# 🐳 **Execução com Docker (Local)**

### 1. Build da imagem

```bash
docker build -t math-tutor .
```

### 2. Executar o contêiner

```bash
docker run -p 8080:8080 -e OPENAI_API_KEY=SUA_CHAVE math-tutor
```

Acesse em:

👉 http://localhost:8080

---

# 🚆 **Deploy no Railway (Produção)**

### 1. Instalar CLI

```bash
npm i -g @railway/cli
railway login
```

### 2. Inicializar projeto

```bash
railway init
```

### 3. Criar variável de ambiente

```bash
railway variables set OPENAI_API_KEY="SUA_CHAVE"
```

### 4. Deploy

```bash
railway up
```

Aguarde a build terminar — o Railway enviará uma URL pública.  
Copie a URL e coloque no início deste README.

---

# 🔧 **Configuração da Aplicação**

### Variáveis de ambiente obrigatórias:

| Nome             | Descrição              |
| ---------------- | ---------------------- |
| `OPENAI_API_KEY` | chave de API do OpenAI |

### Ajustes opcionais:

| Variável                | Função                                      |
| ----------------------- | ------------------------------------------- |
| `MODEL_NAME`            | modelo OpenAI usado (default: gpt-4.1-mini) |
| `STREAMLIT_SERVER_PORT` | porta (Railway usa 8080)                    |

---

# 📜 **Pedagogia do Tutor**

O tutor segue princípios:

- explicações passo a passo  
- foco conceitual  
- rigor quando apropriado  
- analogias quando útil  
- adaptação ao nível do aluno  
- resumo final  

Essas regras estão em:

```
app/pedagogical_profile.py
```

---

# 🗂️ **Logging**

Cada interação é salva em:

```
logs/chat_log_YYYY-MM-DD.jsonl
```

Cada entrada possui:

```json
{
  "timestamp": "...",
  "subject": "math/physics/generic",
  "source": "cli/web",
  "messages": [...],
  "reply": "..."
}
```

No Railway, logs aparecem no dashboard.

---

# 🛡 **Segurança**

- A chave da API **NUNCA** deve ser adicionada ao GitHub.  
- O arquivo `config.py` é ignorado pelo `.gitignore`.  
- A chave é passada via `.env` (local) ou variável do Railway (produção).  
- O Dockerfile não contém chaves embutidas.

---

# 🤝 **Contribuições**

Contribuições são bem-vindas!  
Basta abrir uma *issue* ou *pull request*.

---

# 📄 **Licença**

MIT License