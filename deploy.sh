#!/bin/bash

# Script de Deploy Automatizado para AWS
# Autor: Redot Team
# Versão: 1.0

set -e  # Para o script se houver erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Verificar se o arquivo .env existe
if [ ! -f .env ]; then
    print_error "Arquivo .env não encontrado!"
    print_message "Criando .env a partir do .env.example..."
    cp .env.example .env
    print_warning "Por favor, edite o arquivo .env com suas configurações antes de continuar!"
    exit 1
fi

# Carregar variáveis de ambiente
source .env

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    print_error "Docker não está instalado!"
    print_message "Instalando Docker..."

    # Atualizar sistema
    sudo apt-get update

    # Instalar dependências
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # Adicionar chave GPG do Docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # Adicionar repositório
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Instalar Docker
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    # Instalar Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Adicionar usuário ao grupo docker
    sudo usermod -aG docker $USER

    print_message "Docker instalado com sucesso!"
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose não está instalado!"
    print_message "Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Menu de opções
echo ""
echo "========================================="
echo "   REDOT - Sistema de Deploy"
echo "========================================="
echo ""
echo "Selecione uma opção:"
echo "1) Deploy completo (build + start)"
echo "2) Apenas build das imagens"
echo "3) Start dos containers"
echo "4) Stop dos containers"
echo "5) Restart dos containers"
echo "6) Ver logs"
echo "7) Backup do banco de dados"
echo "8) Restore do banco de dados"
echo "9) Atualizar código do Git"
echo "0) Sair"
echo ""
read -p "Opção: " option

case $option in
    1)
        print_message "Iniciando deploy completo..."

        # Pull das últimas alterações (se estiver em um repositório git)
        if [ -d .git ]; then
            print_message "Atualizando código do repositório..."
            git pull origin main || git pull origin master
        fi

        # Build das imagens
        print_message "Construindo imagens Docker..."
        docker-compose -f docker-compose.prod.yml build --no-cache

        # Stop containers antigos
        print_message "Parando containers antigos..."
        docker-compose -f docker-compose.prod.yml down

        # Start novos containers
        print_message "Iniciando novos containers..."
        docker-compose -f docker-compose.prod.yml up -d

        # Aguardar containers subirem
        print_message "Aguardando containers iniciarem..."
        sleep 10

        # Verificar saúde dos containers
        print_message "Verificando status dos containers..."
        docker-compose -f docker-compose.prod.yml ps

        print_message "Deploy completo realizado com sucesso!"
        ;;

    2)
        print_message "Construindo imagens Docker..."
        docker-compose -f docker-compose.prod.yml build --no-cache
        print_message "Build completo!"
        ;;

    3)
        print_message "Iniciando containers..."
        docker-compose -f docker-compose.prod.yml up -d
        print_message "Containers iniciados!"
        ;;

    4)
        print_message "Parando containers..."
        docker-compose -f docker-compose.prod.yml down
        print_message "Containers parados!"
        ;;

    5)
        print_message "Reiniciando containers..."
        docker-compose -f docker-compose.prod.yml restart
        print_message "Containers reiniciados!"
        ;;

    6)
        echo "Qual log deseja ver?"
        echo "1) Todos os serviços"
        echo "2) Backend"
        echo "3) Frontend"
        echo "4) Nginx"
        echo "5) PostgreSQL"
        read -p "Opção: " log_option

        case $log_option in
            1) docker-compose -f docker-compose.prod.yml logs -f ;;
            2) docker-compose -f docker-compose.prod.yml logs -f backend ;;
            3) docker-compose -f docker-compose.prod.yml logs -f frontend ;;
            4) docker-compose -f docker-compose.prod.yml logs -f nginx ;;
            5) docker-compose -f docker-compose.prod.yml logs -f postgres ;;
            *) print_error "Opção inválida!" ;;
        esac
        ;;

    7)
        print_message "Realizando backup do banco de dados..."

        # Criar diretório de backup se não existir
        mkdir -p backups

        # Nome do arquivo com timestamp
        BACKUP_FILE="backups/redot_backup_$(date +%Y%m%d_%H%M%S).sql"

        # Executar backup
        docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U ${DB_USER:-postgres} ${DB_NAME:-redot} > $BACKUP_FILE

        print_message "Backup salvo em: $BACKUP_FILE"
        ;;

    8)
        print_message "Listando backups disponíveis:"
        ls -la backups/*.sql 2>/dev/null || print_error "Nenhum backup encontrado!"

        read -p "Digite o caminho do arquivo de backup: " RESTORE_FILE

        if [ -f "$RESTORE_FILE" ]; then
            print_warning "ATENÇÃO: Isso irá sobrescrever o banco de dados atual!"
            read -p "Tem certeza? (s/n): " confirm

            if [ "$confirm" = "s" ]; then
                print_message "Restaurando banco de dados..."
                docker-compose -f docker-compose.prod.yml exec -T postgres psql -U ${DB_USER:-postgres} ${DB_NAME:-redot} < $RESTORE_FILE
                print_message "Restore completo!"
            else
                print_message "Operação cancelada."
            fi
        else
            print_error "Arquivo não encontrado!"
        fi
        ;;

    9)
        if [ -d .git ]; then
            print_message "Atualizando código do repositório..."
            git pull origin main || git pull origin master
            print_message "Código atualizado!"
            print_warning "Lembre-se de fazer rebuild e restart dos containers!"
        else
            print_error "Este diretório não é um repositório Git!"
        fi
        ;;

    0)
        print_message "Saindo..."
        exit 0
        ;;

    *)
        print_error "Opção inválida!"
        ;;
esac

echo ""
print_message "Operação concluída!"