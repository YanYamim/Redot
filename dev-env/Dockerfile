FROM ubuntu:noble

# Versões
ARG USER="redot"
ARG USER_ID=1000
ARG GROUP_ID=1000

ENV DEBIAN_FRONTEND=noninteractive

# Pacotes básicos para Python/Node e build
RUN apt update && apt upgrade -y && \
    apt install -y \
    python3 python3-pip python3-venv python3-dev \
    curl wget git sudo \
    build-essential libpq-dev gcc \
    libffi-dev libssl-dev pkg-config \
    libxml2-dev libxslt1-dev zlib1g-dev \
    locales locales-all && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Locale
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

# Node (via NodeSource)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Prepara diretório de trabalho para UID/GID em runtime
RUN mkdir -p /home/${USER}/app && chown -R ${USER_ID}:${GROUP_ID} /home/${USER}

WORKDIR /home/${USER}/app

# Cria e usa venv para evitar conflitos com pip no sistema
RUN python3 -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia apenas manifests para cache de dependências
COPY --chown=${USER_ID}:${GROUP_ID} ../backend/requirements.txt /home/${USER}/app/backend/requirements.txt
# Evita erro em sqlpython com validação recente de entry points
RUN python -m pip install --upgrade "pip<24" "setuptools<69" "wheel<0.42" && \
    python -m pip install --no-cache-dir -r backend/requirements.txt

COPY --chown=${USER_ID}:${GROUP_ID} ../frontend/package*.json /home/${USER}/app/frontend/
RUN cd frontend && npm install

# Portas de dev (Flask/Vite)
EXPOSE 5000 5173

# Shell interativo por padrão
CMD ["bash"]
