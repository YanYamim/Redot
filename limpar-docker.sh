#!/bin/bash

echo "🧹 Limpando cache do Docker..."

# Parar todos os containers
echo "Parando containers..."
docker-compose -f docker-compose.prod.yml down

# Remover imagens do projeto
echo "Removendo imagens do projeto..."
docker rmi redot-frontend redot-backend 2>/dev/null || true
docker rmi $(docker images | grep redot | awk '{print $3}') 2>/dev/null || true

# Limpar cache do build
echo "Limpando cache do Docker..."
docker builder prune -f

# Limpar tudo (cuidado - remove TODAS as imagens não usadas)
echo "Limpeza completa..."
docker system prune -a -f

echo "✅ Limpeza concluída!"
echo ""
echo "Agora rode: ./deploy.sh e escolha opção 1"