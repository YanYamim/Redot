FROM ubuntu:noble

# Variáveis de versão
ARG NODE_VERSION=18.19.1
ARG POSTGRES_VERSION=17
ARG USER="redot"
ARG USER_ID=1000
ARG GROUP_ID=1000

# Evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza pacotes e instala dependências
RUN apt update && apt upgrade -y && \
    apt install -y \
    python3 python3-pip python3-venv \
    curl wget git sudo \
    build-essential libpq-dev gcc \
    postgresql-${POSTGRES_VERSION} postgresql-contrib \
    locales locales-all && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Configura locale
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Instala Node
RUN curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz \
    -o /tmp/node.tar.xz && \
    tar -xf /tmp/node.tar.xz -C /opt && \
    mv /opt/node-v${NODE_VERSION}-linux-x64 /opt/node && \
    ln -s /opt/node/bin/node /usr/local/bin/node && \
    ln -s /opt/node/bin/npm /usr/local/bin/npm && \
    ln -s /opt/node/bin/npx /usr/local/bin/npx && \
    rm /tmp/node.tar.xz

# Configura Postgres para aceitar conexões externas
RUN sed -i 's/peer/trust/g' /etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf && \
    sed -i 's/scram-sha-256/trust/g' /etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf && \
    sed -i 's/127.0.0.1\/32/0.0.0.0\/0/g' /etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf && \
    echo "listen_addresses = '*'" >> /etc/postgresql/${POSTGRES_VERSION}/main/postgresql.conf

# Cria usuário não-root para desenvolvimento
RUN useradd -m -u ${USER_ID} -s /bin/bash ${USER} && \
    groupmod -g ${GROUP_ID} ${USER} && \
    usermod -aG sudo ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USER}

USER ${USER}
WORKDIR /home/${USER}

# Instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Instala dependências Node (para Vue/Vuetify)
WORKDIR /home/${USER}/app
COPY package*.json ./
RUN npm install

# Cria pasta para extensões do VSCode
RUN mkdir -p /home/${USER}/.vscode-server/extensions

# Porta padrão (Flask + Postgres)
EXPOSE 5000 5432 5173

# Comando default (apenas mantém container ativo no modo dev)
CMD ["bash"]
