# 📚 GUIA COMPLETO DE DEPLOY NA AWS - PROJETO REDOT

## 📋 Índice

1. [Preparação Inicial](#1-preparação-inicial)
2. [Criando Conta na AWS](#2-criando-conta-na-aws)
3. [Configurando EC2 (Servidor)](#3-configurando-ec2-servidor)
4. [Conectando ao Servidor](#4-conectando-ao-servidor)
5. [Instalando Dependências](#5-instalando-dependências)
6. [Clonando e Configurando o Projeto](#6-clonando-e-configurando-o-projeto)
7. [Configurando Domínio e DNS](#7-configurando-domínio-e-dns)
8. [Configurando SSL (HTTPS)](#8-configurando-ssl-https)
9. [Deploy da Aplicação](#9-deploy-da-aplicação)
10. [Monitoramento e Manutenção](#10-monitoramento-e-manutenção)
11. [Troubleshooting (Resolução de Problemas)](#11-troubleshooting-resolução-de-problemas)

---

## 1. PREPARAÇÃO INICIAL

### O que você vai precisar:

- ✅ Cartão de crédito (para criar conta AWS - não será cobrado se ficar no free tier)
- ✅ Um computador com acesso à internet
- ✅ O código do projeto Redot
- ✅ Um e-mail válido
- ✅ Aproximadamente 2 horas livres

### Custos estimados:

- **Free Tier (Grátis por 12 meses):** EC2 t2.micro
- **Após Free Tier:** ~$15-30/mês para uso básico
- **Domínio (opcional):** ~$12/ano

---

## 2. CRIANDO CONTA NA AWS

### Passo a Passo Detalhado:

1. **Acesse o site da AWS:**
   - Abra seu navegador
   - Digite: https://aws.amazon.com
   - Clique em "Criar uma conta da AWS" (botão laranja no canto superior direito)

2. **Preencha o formulário:**
   ```
   E-mail: seu-email@exemplo.com
   Senha: (crie uma senha forte com letras, números e símbolos)
   Nome da conta AWS: redot-producao
   ```

3. **Informações de contato:**
   - Tipo de conta: Pessoal
   - Nome completo: Seu nome
   - Telefone: Seu telefone com +55 para Brasil
   - País: Brasil
   - Endereço: Seu endereço completo

4. **Informações de pagamento:**
   - Digite os dados do cartão de crédito
   - AWS pode fazer uma cobrança de $1 para verificação (será estornada)

5. **Verificação de identidade:**
   - AWS enviará um código por SMS ou ligação
   - Digite o código recebido

6. **Escolha o plano de suporte:**
   - Selecione "Basic Plan - Free"

7. **Finalize o cadastro:**
   - Clique em "Complete Sign Up"
   - Aguarde o e-mail de confirmação (pode levar até 24h)

---

## 3. CONFIGURANDO EC2 (SERVIDOR)

### Acessando o Console AWS:

1. **Faça login no AWS Console:**
   - Acesse: https://console.aws.amazon.com
   - Use seu e-mail e senha criados

2. **Selecione a região:**
   - No canto superior direito, clique na região
   - Escolha "São Paulo" (sa-east-1) para menor latência no Brasil

### Criando a Instância EC2:

1. **Acesse o serviço EC2:**
   - Na barra de busca superior, digite "EC2"
   - Clique em "EC2"

2. **Clique em "Launch Instance" (botão laranja)**

3. **Configure a instância:**

   **Nome e tags:**
   ```
   Name: redot-server
   ```

   **Escolha a AMI (Sistema Operacional):**
   - Selecione "Ubuntu Server 22.04 LTS (HVM), SSD Volume Type"
   - Arquitetura: 64-bit (x86)

   **Tipo de instância:**
   - Selecione "t2.micro" (Free tier eligible)
   - Isso dá 1 vCPU e 1GB RAM

   **Par de chaves (Key Pair):**
   - Clique em "Create new key pair"
   - Nome: `redot-key`
   - Tipo: RSA
   - Formato: .pem (para Mac/Linux) ou .ppk (para Windows com PuTTY)
   - **IMPORTANTE:** Baixe e salve este arquivo em local seguro!

   **Configurações de rede:**
   - VPC: default
   - Subnet: No preference
   - Auto-assign public IP: Enable

   **Firewall (Security Group):**
   - Clique em "Create security group"
   - Nome: `redot-security-group`
   - Descrição: `Security group for Redot application`

   **Regras de entrada (Inbound rules):**
   Adicione as seguintes regras:
   ```
   Tipo: SSH       | Protocolo: TCP | Porta: 22   | Origem: My IP
   Tipo: HTTP      | Protocolo: TCP | Porta: 80   | Origem: 0.0.0.0/0
   Tipo: HTTPS     | Protocolo: TCP | Porta: 443  | Origem: 0.0.0.0/0
   Tipo: Custom TCP| Protocolo: TCP | Porta: 5000 | Origem: 0.0.0.0/0
   ```

   **Armazenamento:**
   - 1x 8GB gp3 (padrão)
   - Delete on termination: Yes

4. **Revise e lance:**
   - Clique em "Launch instance"
   - Aguarde a instância iniciar (status: running)

5. **Anote o IP público:**
   - Na lista de instâncias, copie o "Public IPv4 address"
   - Exemplo: `54.232.123.456`

---

## 4. CONECTANDO AO SERVIDOR

### Para Windows (usando PuTTY):

1. **Baixe o PuTTY:**
   - Acesse: https://www.putty.org
   - Baixe e instale

2. **Se você baixou .pem, converta para .ppk:**
   - Abra o PuTTYgen
   - File → Load private key
   - Selecione o arquivo .pem baixado
   - Save private key → salve como redot-key.ppk

3. **Configure o PuTTY:**
   - Host Name: `ubuntu@SEU-IP-PUBLICO`
   - Port: 22
   - Connection → SSH → Auth → Private key: selecione o arquivo .ppk
   - Clique em "Open"

### Para Mac/Linux:

1. **Abra o Terminal**

2. **Configure as permissões da chave:**
   ```bash
   chmod 400 ~/Downloads/redot-key.pem
   ```

3. **Conecte ao servidor:**
   ```bash
   ssh -i ~/Downloads/redot-key.pem ubuntu@SEU-IP-PUBLICO
   ```
   Substitua SEU-IP-PUBLICO pelo IP que você anotou.

4. **Aceite a fingerprint:**
   - Digite "yes" quando perguntado

---

## 5. INSTALANDO DEPENDÊNCIAS

### Execute os comandos abaixo NO SERVIDOR (após conectar via SSH):

```bash
# 1. Atualize o sistema
sudo apt update && sudo apt upgrade -y

# 2. Instale ferramentas essenciais
sudo apt install -y curl git vim nano wget software-properties-common

# 3. Instale Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Configure Docker para rodar sem sudo
sudo usermod -aG docker ubuntu

# 5. Instale Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 6. Verifique as instalações
docker --version
docker-compose --version

# 7. Faça logout e login novamente para aplicar permissões
exit
```

Reconecte ao servidor:
```bash
ssh -i ~/Downloads/redot-key.pem ubuntu@SEU-IP-PUBLICO
```

---

## 6. CLONANDO E CONFIGURANDO O PROJETO

### No servidor, execute:

```bash
# 1. Clone o repositório (substitua pela URL do seu repositório)
git clone https://github.com/seu-usuario/redot.git
cd redot

# OU se não tiver no GitHub, copie os arquivos via SCP:
# No seu computador local:
# scp -i ~/Downloads/redot-key.pem -r /caminho/para/redot ubuntu@SEU-IP-PUBLICO:~/
```

### Configure as variáveis de ambiente:

```bash
# 1. Copie o arquivo de exemplo
cp .env.example .env

# 2. Edite o arquivo .env
nano .env
```

Edite as seguintes variáveis:
```env
# Banco de dados - MUDE ESTAS SENHAS!
DB_USER=postgres
DB_PASSWORD=SuaSenhaSegura123!@#
DB_NAME=redot

# Segurança - MUDE ESTA CHAVE!
SECRET_KEY=suaChaveSecretaMuitoLongaESegura123456789ABCDEF

# URLs
CORS_ORIGINS=http://SEU-IP-PUBLICO,http://seu-dominio.com.br
VITE_API_URL=http://SEU-IP-PUBLICO/api

# Ambiente
ENVIRONMENT=production
DEBUG=false
```

**Para salvar no nano:**
- Ctrl+O (salvar)
- Enter (confirmar)
- Ctrl+X (sair)

### Adicione o endpoint de health check no backend:

```bash
# Edite o arquivo app.py
nano backend/app.py
```

Adicione antes do `if __name__ == '__main__':`:

```python
@app.route('/health')
def health_check():
    return 'OK', 200
```

Salve o arquivo (Ctrl+O, Enter, Ctrl+X).

---

## 7. CONFIGURANDO DOMÍNIO E DNS

### Opção A: Usando apenas IP (mais simples):

Você pode acessar sua aplicação diretamente pelo IP:
- Frontend: `http://SEU-IP-PUBLICO`
- Backend: `http://SEU-IP-PUBLICO/api`

### Opção B: Configurando um domínio (recomendado):

1. **Compre um domínio:**
   - Registro.br (~R$40/ano): https://registro.br
   - GoDaddy: https://godaddy.com
   - Namecheap: https://namecheap.com

2. **Configure o DNS:**

   No painel do seu registrador de domínio, adicione:
   ```
   Tipo: A     | Nome: @    | Valor: SEU-IP-PUBLICO | TTL: 3600
   Tipo: A     | Nome: www  | Valor: SEU-IP-PUBLICO | TTL: 3600
   Tipo: CNAME | Nome: api  | Valor: seu-dominio.com.br | TTL: 3600
   ```

3. **Aguarde propagação:**
   - Pode levar até 48h, mas geralmente funciona em minutos

4. **Atualize o .env com seu domínio:**
   ```bash
   nano .env
   ```
   ```env
   CORS_ORIGINS=http://seu-dominio.com.br,https://seu-dominio.com.br
   VITE_API_URL=http://seu-dominio.com.br/api
   ```

---

## 8. CONFIGURANDO SSL (HTTPS)

### Instalando Certbot para certificados SSL gratuitos:

```bash
# 1. Instale o Certbot
sudo apt install -y certbot python3-certbot-nginx

# 2. Primeiro, faça o deploy sem SSL
./deploy.sh
# Escolha opção 1 (Deploy completo)

# 3. Aguarde os containers subirem
docker-compose -f docker-compose.prod.yml ps

# 4. Obtenha o certificado SSL
sudo certbot certonly --standalone -d seu-dominio.com.br -d www.seu-dominio.com.br

# Siga as instruções:
# - Digite seu e-mail
# - Aceite os termos (A)
# - Compartilhar e-mail (N ou Y, sua escolha)
```

### Configure o Nginx para usar SSL:

```bash
# 1. Crie diretório para SSL
mkdir -p nginx/ssl

# 2. Copie os certificados
sudo cp /etc/letsencrypt/live/seu-dominio.com.br/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/seu-dominio.com.br/privkey.pem nginx/ssl/key.pem
sudo chown ubuntu:ubuntu nginx/ssl/*

# 3. Edite o nginx.prod.conf
nano nginx/nginx.prod.conf
```

Descomente as linhas de SSL no arquivo (remova os #):
```nginx
    # server {
    #     listen 80;
    #     server_name seu-dominio.com.br www.seu-dominio.com.br;
    #     return 301 https://$server_name$request_uri;
    # }
```

E também:
```nginx
        # listen 443 ssl http2;
        # ssl_certificate /etc/nginx/ssl/cert.pem;
        # ssl_certificate_key /etc/nginx/ssl/key.pem;
        # ssl_protocols TLSv1.2 TLSv1.3;
        # ssl_ciphers HIGH:!aNULL:!MD5;
```

### Reinicie com SSL ativado:

```bash
# Rebuild e restart
./deploy.sh
# Escolha opção 1
```

### Configure renovação automática do SSL:

```bash
# Adicione ao crontab
sudo crontab -e

# Adicione esta linha:
0 2 * * 1 certbot renew --quiet && cp /etc/letsencrypt/live/seu-dominio.com.br/*.pem /home/ubuntu/redot/nginx/ssl/ && docker-compose -f /home/ubuntu/redot/docker-compose.prod.yml restart nginx
```

---

## 9. DEPLOY DA APLICAÇÃO

### Execute o deploy:

```bash
# 1. Dê permissão ao script
chmod +x deploy.sh

# 2. Execute o deploy
./deploy.sh
```

**Menu de opções:**
```
1) Deploy completo (build + start) ← ESCOLHA ESTA NA PRIMEIRA VEZ
2) Apenas build das imagens
3) Start dos containers
4) Stop dos containers
5) Restart dos containers
6) Ver logs
7) Backup do banco de dados
8) Restore do banco de dados
9) Atualizar código do Git
0) Sair
```

### Verificando se tudo está funcionando:

```bash
# 1. Verifique os containers
docker-compose -f docker-compose.prod.yml ps

# Você deve ver algo assim:
# NAME                 STATUS    PORTS
# redot-postgres       healthy   5432/tcp
# redot-backend        healthy   5000/tcp
# redot-frontend       healthy   80/tcp
# redot-nginx          healthy   0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

```bash
# 2. Teste o health check
curl http://localhost/health

# Deve retornar: healthy
```

```bash
# 3. Veja os logs se houver problemas
docker-compose -f docker-compose.prod.yml logs -f
```

### Acessando a aplicação:

Abra seu navegador e acesse:
- Se configurou domínio: `https://seu-dominio.com.br`
- Se não: `http://SEU-IP-PUBLICO`

---

## 10. MONITORAMENTO E MANUTENÇÃO

### Comandos úteis do dia a dia:

```bash
# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Ver logs de um serviço específico
docker-compose -f docker-compose.prod.yml logs -f backend

# Reiniciar um serviço
docker-compose -f docker-compose.prod.yml restart backend

# Ver uso de recursos
docker stats

# Ver espaço em disco
df -h

# Limpar imagens Docker antigas
docker system prune -a

# Fazer backup do banco
./deploy.sh
# Escolha opção 7
```

### Configurando backups automáticos:

```bash
# Crie script de backup
nano backup.sh
```

```bash
#!/bin/bash
# Backup automático
BACKUP_DIR="/home/ubuntu/redot/backups"
mkdir -p $BACKUP_DIR
docker-compose -f /home/ubuntu/redot/docker-compose.prod.yml exec -T postgres \
  pg_dump -U postgres redot > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"

# Manter apenas últimos 7 backups
ls -t $BACKUP_DIR/*.sql | tail -n +8 | xargs rm -f 2>/dev/null
```

```bash
chmod +x backup.sh

# Adicione ao cron para rodar diariamente às 3AM
crontab -e
# Adicione:
0 3 * * * /home/ubuntu/redot/backup.sh
```

### Monitorando a aplicação:

1. **CloudWatch (AWS):**
   - No console AWS, vá para CloudWatch
   - Create Dashboard → Add widget
   - Escolha EC2 → Per-Instance Metrics
   - Selecione sua instância
   - Adicione CPU, Network, Disk

2. **Alertas por e-mail:**
   - CloudWatch → Alarms → Create Alarm
   - Métrica: EC2 → CPU Utilization
   - Condição: Greater than 80%
   - Notification: Create SNS topic → adicione seu e-mail

---

## 11. TROUBLESHOOTING (RESOLUÇÃO DE PROBLEMAS)

### Problema: "Connection refused" ao acessar o site

**Solução:**
```bash
# 1. Verifique se os containers estão rodando
docker-compose -f docker-compose.prod.yml ps

# 2. Se não estiverem, inicie:
docker-compose -f docker-compose.prod.yml up -d

# 3. Verifique os logs
docker-compose -f docker-compose.prod.yml logs
```

### Problema: "502 Bad Gateway"

**Solução:**
```bash
# Backend pode estar com problema
docker-compose -f docker-compose.prod.yml logs backend

# Reinicie o backend
docker-compose -f docker-compose.prod.yml restart backend
```

### Problema: Erro de CORS

**Solução:**
```bash
# Edite o .env
nano .env

# Certifique-se que CORS_ORIGINS inclui sua URL
CORS_ORIGINS=http://seu-dominio.com.br,https://seu-dominio.com.br

# Reinicie
docker-compose -f docker-compose.prod.yml restart backend
```

### Problema: Banco de dados não conecta

**Solução:**
```bash
# Verifique se postgres está healthy
docker-compose -f docker-compose.prod.yml ps postgres

# Veja os logs
docker-compose -f docker-compose.prod.yml logs postgres

# Teste conexão
docker-compose -f docker-compose.prod.yml exec postgres psql -U postgres -d redot -c "SELECT 1;"
```

### Problema: Sem espaço em disco

**Solução:**
```bash
# Veja o uso
df -h

# Limpe Docker
docker system prune -a --volumes

# Limpe logs antigos
truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

### Problema: Alto uso de CPU/Memória

**Solução:**
```bash
# Veja qual container está consumindo
docker stats

# Reinicie o problemático
docker-compose -f docker-compose.prod.yml restart nome-do-servico

# Se persistir, considere upgrade da instância EC2
```

---

## 📞 SUPORTE E AJUDA

### Recursos úteis:

- **Documentação Docker:** https://docs.docker.com
- **Documentação AWS EC2:** https://docs.aws.amazon.com/ec2
- **Stack Overflow:** https://stackoverflow.com
- **Comunidade AWS:** https://forums.aws.amazon.com

### Comandos de emergência:

```bash
# Parar tudo
docker-compose -f docker-compose.prod.yml down

# Reiniciar servidor
sudo reboot

# Ver todos os logs
journalctl -xe

# Verificar porta em uso
sudo netstat -tulpn | grep :80
```

### Checklist de verificação:

- [ ] EC2 está running?
- [ ] Security Group permite portas 80/443?
- [ ] Docker está instalado?
- [ ] Arquivo .env configurado?
- [ ] Containers estão healthy?
- [ ] DNS está apontando para IP correto?
- [ ] Certificado SSL válido?

---

## 🎉 PARABÉNS!

Se você chegou até aqui, sua aplicação Redot deve estar rodando na AWS!

### Próximos passos recomendados:

1. **Configure um banco de dados RDS** (mais robusto que container)
2. **Use um Load Balancer** para alta disponibilidade
3. **Configure CloudFront** (CDN) para melhor performance
4. **Implemente CI/CD** com GitHub Actions
5. **Configure monitoramento** com New Relic ou Datadog

### Dicas de segurança:

- Sempre mantenha backups
- Atualize regularmente os pacotes
- Use senhas fortes
- Habilite 2FA na AWS
- Monitore logs regularmente
- Configure firewall (ufw)

---

**Documento criado para deploy do Projeto Redot**
**Versão: 1.0**
**Data: 2024**

> 💡 **DICA FINAL:** Salve este documento e o arquivo .pem em local seguro. Você precisará deles para acessar e manter seu servidor!