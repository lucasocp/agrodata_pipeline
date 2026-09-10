# AgroData Pipeline

Pipeline de dados orientado ao agronegócio com extração, transformação/validação com Pandas, carga em PostgreSQL e API REST com FastAPI.

## Melhores Práticas de Segurança
- Credenciais e segredos gerenciados via variáveis de ambiente (`.env`).
- `.env` incluído no `.gitignore` (nunca commitado no repositório).
- Container executado com usuário não-root (`appuser`).
- Exposição de portas vinculada ao `127.0.0.1` para prevenir acesso externo indevido.

## Como Executar

1. Copie o arquivo `.env.example` para `.env`:
   ```bash
   cp .env.example .env
   ```
2. Ajuste as senhas e credenciais no arquivo `.env`.
3. Inicie os containers com Docker Compose:
   ```bash
   docker-compose up --build -d
   ```
4. Acesse a documentação Swagger da API:
   `http://localhost:8000/docs`
