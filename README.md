# 🌾 AgroData Pipeline

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.1-150458.svg)](https://pandas.pydata.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

Um pipeline de dados orientado ao agronegócio focado em extração, validação, limpeza, engenharia de features e disponibilização de métricas agrícolas via API REST. Projetado seguindo princípios de **Clean Architecture**, **SOLID**, **DevSecOps** e **Data Quality**.

Fluxo de Dados (Pipeline ETL)

Extract: Leitura de dados brutos agrícolas a partir de fontes estruturadas (CSV, APIs).

Transform & Data Quality:

Padronização do esquema de colunas.

Remoção de duplicatas com base em chaves compostas (farm_id, crop_type, harvest_date).

Normalização de tipos de dados (datas, números, textos).

Validação de regras de negócio (áreas e produções estritamente maiores que zero).

Engine de Feature Engineering (Cálculo automático da produtividade em $ton/ha$).

Load: Carga otimizada via bulk operations na tabela agro_production do PostgreSQL.

Serve: Disponibilização dos dados e KPIs agregados através de endpoints da API REST.


Princípios de Segurança (DevSecOps)

Gestão de Segredos: Credenciais gerenciadas via .env (ignorado no versionamento Git pelo .gitignore).

Princípio do Menor Privilégio: Container executado por usuário não-root (appuser).

Isolamento de Rede: Portas vinculadas diretamente à interface local (127.0.0.1) no Docker Compose, evitando exposição indevida da base de dados.

Validação Estrita de Input: Tipagem e validação com Pydantic e filtros sanitizados pelo ORM SQLAlchemy.


Tecnologias Utilizadas

Linguagem: Python 3.11

Processamento de Dados: Pandas, NumPy

Framework Web / API: FastAPI, Uvicorn

Banco de Dados & ORM: PostgreSQL, SQLAlchemy, Psycopg2

Conteinerização: Docker, Docker Compose


Como Executar o Projeto

Pré-requisitos

Docker instalado.

Docker Compose instalado.


Passo a Passo

Clonar o repositório:

Bash
git clone [https://github.com/seu-usuario/agrodata-pipeline.git](https://github.com/seu-usuario/agrodata-pipeline.git)
cd agrodata-pipeline

Configurar as variáveis de ambiente:
Copie o template .env.example para criar seu arquivo .env:

Bash
cp .env.example .env

Iniciar a infraestrutura com Docker Compose:

Bash
docker-compose up --build -d
(Aguarde até que o container do PostgreSQL passe na verificação de healthcheck e a API seja iniciada).

Verificar os containers em execução:

Bash
docker-compose ps


Utilização da API

Documentação Interativa (Swagger)
Acesse a documentação no navegador para testar os endpoints interativamente:
http://localhost:8000/docs

Endpoints Principais
1. Executar o Pipeline ETLExecuta a ingestão, limpeza e carga dos dados contidos no arquivo CSV especificado.
Método: POST
URL: /api/v1/etl/run
Exemplo de chamada:

Bash
curl -X POST "http://localhost:8000/api/v1/etl/run"

2. Consultar Dados de ProduçãoRetorna listagem dos dados agrícolas com paginação e filtros por cultura ou região.
Método: GET
URL: /api/v1/production
Exemplo de chamada:

Bash
curl -X GET "http://localhost:8000/api/v1/production?crop_type=Soja&region=CENTRO-OESTE"

3. Consultar KPIs ConsolidadosCalcula e retorna métricas consolidadas (Área Total, Produção Total, Produtividade Média).
Método: GET
URL: /api/v1/production/kpis
Exemplo de chamada:

Bash
curl -X GET "http://localhost:8000/api/v1/production/kpis?crop_type=Soja"


Exemplo de Resposta de KPIs
JSON

{
  "total_area_hectares": 150.0,
  "total_yield_tons": 520.5,
  "average_productivity": 3.47,
  "total_records": 1
}


Encerrando os Serviços

Para parar e remover os containers e redes mantendo a persistência dos dados:

Bash
docker-compose down

Para remover também o volume de dados do PostgreSQL:

Bash
docker-compose down -v

---

## 📐 Arquitetura do Projeto

```text
agrodata-pipeline/
├── app/
│   ├── __init__.py
│   ├── config.py         # Configurações globais e Pydantic Settings
│   ├── database.py       # Conexão SQLAlchemy e sessão do banco
│   ├── etl.py            # Engine de ETL (Extract, Transform, Load)
│   ├── main.py           # Aplicação FastAPI e Endpoints REST
│   ├── models.py         # Modelos ORM (PostgreSQL)
│   └── schemas.py        # Schemas de validação e serialização Pydantic
├── data/
│   └── raw_agro_data.csv # Dataset bruto de exemplo
├── .env.example          # Template de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
├── Dockerfile            # Imagem Docker da API (Non-root user)
├── docker-compose.yml    # Orquestração dos serviços (API + PostgreSQL)
├── README.md             # Documentação do projeto
└── requirements.txt      # Dependências do projeto
🛑 Encerrando os ServiçosPara parar e remover os containers e redes mantendo a persistência dos dados:Bashdocker-compose down
Para remover também o volume de dados do PostgreSQL:Bashdocker-compose down -v
