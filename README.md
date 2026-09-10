# 🌾 AgroData Pipeline

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.1-150458.svg)](https://pandas.pydata.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

Um pipeline de dados orientado ao agronegócio focado em extração, validação, limpeza, engenharia de features e disponibilização de métricas agrícolas via API REST. Projetado seguindo princípios de **Clean Architecture**, **SOLID**, **DevSecOps** e **Data Quality**.

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
