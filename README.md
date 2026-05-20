# API de Agregação de Dados Climáticos e Geográficos (N703)

Esta é uma API REST desenvolvida em Python (Flask) que integra APIs públicas (IBGE, Nominatim OpenStreetMap e Open-Meteo) para fornecer informações combinadas sobre cidades brasileiras, incluindo dados geográficos e climáticos.

## 🛠️ Tecnologias Utilizadas
* Python 3
* Flask
* Flask-CORS
* Requests
* Pytest (para testes automatizados)

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd <NOME_DA_PASTA>

## Crie e ative um ambiente virtual:
python -m venv .venv
# Windows:
.\.venv\Scripts\Activate
# Linux/Mac:
source .venv/bin/activate

## Instale as dependências:
pip install flask flask-cors requests pytest

## Inicie o servidor:
python src/app.py

A API estará rodando em http://localhost:3000.

## 📌 Endpoints da API
**Health Check:** GET /api/v1/health
Retorna o status do servidor.

**Clima da Cidade:** GET /api/v1/clima/{nome_cidade}
Retorna os dados geográficos e climáticos da cidade informada. (Ex: /api/v1/clima/Fortaleza)

**Cidades por Estado:** GET /api/v1/cidades/{sigla_uf}?limite={qtd}
Retorna a lista de municípios de um estado. (Ex: /api/v1/cidades/CE?limite=5)

## 🧪 Como Rodar os Testes
Para executar os testes automatizados, certifique-se de que o ambiente virtual está ativado e rode:
pytest tests/

## 📬 Coleção do Postman
Na pasta docs/ encontra-se o arquivo postman_collection.json. Você pode importá-lo diretamente no seu Postman para testar todas as rotas já configuradas.