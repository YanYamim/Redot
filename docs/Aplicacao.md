# Sobre o backend

Ele é uma aplicação onde é possível realizar pesquisas de marcas usando um scrapy. Nele o usuário dirá a empresa a ser pesquisada e será coletada o nome, fonte (Instagram, Facebook, Google e etc...), e a url. Será salvo esses dados no banco MySQL. A pesquisada é feita a cada tempo determinado, por isso usa-se um CRON para agendar uma pesquisa, por exemplo, a cada 1 hora. 

# Interpretador usado
venv/bin/python

Obs: Para conectar, usa-se o comando source venv/bin/activate

# Bibliotecas e Frameworks usados

- Flask: Gerencia rotas API para comunicação com o frontend e controla as requisições HTTP e respostas
- Scrapy: Realiza a coleta efetiva dos dados das marcas/empresas
- APSchedule: Gerencia a execução periódica das pesquisas, Permite agendamento flexível e Mantém o estado dos jobs agendados
- Pytest: Realização dos testes automatizados 

# O que ele faz?

No momento que inicia a aplicação e ao lado de um software de testes como postman ou insomnia, será mandado uma requisição com o nome dessa empresa (Ex: Mavip), então, a aplicação fará uma raspagem de dados e salvará no banco o nome da empresa, o perfil do Instagram ou Facebook, a fonte e a sua url.