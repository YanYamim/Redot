# Guia de Instalação - Redot

Este documento contém todas as instruções necessárias para configurar e inicializar o projeto Redot em sua máquina local.

## Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Configuração Backend](#configuração-backend)
3. [Configuração Frontend](#configuração-frontend)
4. [Executando a Aplicação](#executando-a-aplicação)
5. [Variáveis de Ambiente](#variáveis-de-ambiente)
6. [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

Antes de começar, certifique-se de que seu sistema possui:

- **Git**: [Instalar Git](https://git-scm.com/downloads)
- **Python 3.12+**: [Instalar Python](https://www.python.org/downloads/)
- **Node.js 18+**: [Instalar Node.js](https://nodejs.org/)
- **npm** (geralmente vem com Node.js)
- **PostgreSQL** (para banco de dados)

### Verificar Versões Instaladas

```bash
python --version
node --version
npm --version
git --version
```

---

## Configuração Backend

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd python_scrappy
```

### 2. Instalar pyenv (Gerenciador de Versões Python)

**No macOS (com Homebrew):**
```bash
brew install pyenv
```

**No Linux (Ubuntu/Debian):**
```bash
curl https://pyenv.run | bash
```

**No Windows:**
Use WSL2 (Windows Subsystem for Linux) ou instale Python diretamente

### 3. Configurar pyenv (para Linux/macOS)

Adicione as linhas abaixo ao seu arquivo `~/.bashrc`, `~/.zshrc` ou `~/.bash_profile`:

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

Depois recarregue o shell:
```bash
source ~/.bashrc  # ou ~/.zshrc
```

### 4. Instalar Python 3.12 com pyenv

```bash
pyenv install 3.12.0
pyenv global 3.12.0
python --version  
```

### 5. Criar Virtual Environment

```bash
# Navegar até a pasta do projeto
cd python_scrappy

# Criar virtual environment
python -m venv venv
```

### 6. Ativar Virtual Environment

**No Linux/macOS:**
```bash
source venv/bin/activate
```

**No Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**No Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Você saberá que a venv está ativa quando ver `(venv)` no início do prompt do terminal.

### 7. Instalar Dependências Python

```bash
# Certifique-se que a venv está ativada
pip install --upgrade pip
pip install -r requirements.txt
```

### 8. Configurar Banco de Dados

Se ainda não tem um banco PostgreSQL, crie um:

```bash
# Via Terminal
CREATE DATABASE redot_db;

# Ou use o pgAdmin para criar graficamente
```

### 9. Aplicar Migrações Django

```bash
python manage.py migrate
```

### 10. Criar Superuser (Admin)

```bash
python manage.py createsuperuser
# Siga as instruções para criar username, email e senha
```

---

## Configuração Frontend

### 1. Navegar até a Pasta Frontend

```bash
cd frontend
```

### 2. Instalar Dependências Node.js

```bash
npm install
```

Isso instalará todas as dependências definidas em `package.json`.

### 3. Verificar Instalação

```bash
npm list vue vuetify
# Deve mostrar as versões instaladas
```

---

## Executando a Aplicação

### Iniciar Backend (Django)

Na pasta raiz do projeto, com a venv ativada:

```bash
# Terminal 1 - Backend
python manage.py runserver
# O servidor estará disponível em http://localhost:8000
```

### Iniciar Frontend (Vite)

Em outro terminal, na pasta frontend:

```bash
# Terminal 2 - Frontend
npm run dev
# O servidor estará disponível em http://localhost:5173
```

### Acessar a Aplicação

- **Frontend**: http://localhost:5173
- **Backend (API)**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

---

## Variáveis de Ambiente

### Backend

Crie um arquivo `.env` na raiz do projeto:

```env
# Django Settings
DEBUG=True
SECRET_KEY=sua_chave_secreta_aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=redot_db
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# AWS (se usar)
AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=sua_secreta
```

### Frontend

Crie um arquivo `.env` na pasta `frontend`:

```env
VITE_API_URL=http://localhost:8000
```

---

## Comandos Úteis

### Backend

```bash
# Ativar virtual environment
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows

# Desativar virtual environment
deactivate

# Executar testes
pytest

# Executar linter/formatador
black . --check
flake8 .

# Criar nova migração
python manage.py makemigrations

# Ver migrações
python manage.py showmigrations

# Recriar banco de dados (cuidado!)
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

### Frontend

```bash
# Desenvolver com hot reload
npm run dev

# Build para produção
npm run build

# Preview da build de produção
npm run preview

# Verificar tipos TypeScript
npm run type-check

# Lint e fix automático
npm run lint
```

---

## Troubleshooting

### Problema: "Python version not found"
**Solução**: Execute `pyenv install 3.12.0` e depois `pyenv global 3.12.0`

### Problema: Módulos Python não encontrados
**Solução**: Verifique se a venv está ativada e se `pip install -r requirements.txt` foi executado

### Problema: Erro de conexão com banco de dados
**Solução**: Verifique se PostgreSQL está rodando e se as credenciais em `.env` estão corretas

### Problema: Porta 8000 ou 5173 já em uso
**Solução**: 
```bash
# Kill processo na porta 8000
kill -9 $(lsof -t -i:8000)

# Kill processo na porta 5173
kill -9 $(lsof -t -i:5173)
```

### Problema: Dependências não instalam
**Solução**: Tente limpar o cache do pip:
```bash
pip cache purge
pip install --upgrade pip
pip install -r requirements.txt
```

### Problema: npm install falha
**Solução**: Tente limpar o cache do npm:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

---

## Configurar Python Interpreter no VS Code

1. Abra a Command Palette: `Ctrl+Shift+P` (ou `Cmd+Shift+P` no macOS)
2. Digite: "Python: Select Interpreter"
3. Escolha o interpretador virtual: `./venv/bin/python`

---

## Próximos Passos

- Leia a documentação do [Django](https://docs.djangoproject.com/)
- Leia a documentação do [Vue 3](https://vuejs.org/)
- Explore a estrutura do projeto
- Configure as variáveis de ambiente necessárias
- Execute os testes: `pytest`
