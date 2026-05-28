# 🌦️ API de Clima e Cidades (N703)

Bem-vindo(a) ao repositório do projeto! Esta é uma **API REST** construída em **Python** usando o micro-framework **Flask**. 

O objetivo principal desta API é integrar e combinar dados de diferentes serviços (APIs externas públicas) para entregar informações rápidas sobre cidades brasileiras e seu respectivo clima atual.

---

## 📚 O que você vai encontrar aqui?
Este projeto acadêmico demonstra de forma prática:
- A criação de uma API utilizando rotas do Flask.
- O consumo de APIs externas (IBGE, Nominatim OpenStreetMap e Open-Meteo).
- Tratamentos de erros, retornando Códigos de Status HTTP adequados (`200 OK`, `400 Bad Request`, `404 Not Found`, `503 Service Unavailable`).
- Testes automatizados com a biblioteca `pytest`.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3**: A linguagem de programação base do projeto.
- **Flask**: Framework para facilitar a criação do servidor e de suas rotas (endpoints).
- **Flask-CORS**: Biblioteca para permitir requisições seguras de origens cruzadas (CORS).
- **Requests**: Ferramenta utilizada para buscar os dados de clima e cidades nas APIs do IBGE e Open-Meteo.
- **Pytest**: Responsável por rodar os testes das nossas regras de negócio.

---

## 🚀 Passo a Passo: Como Rodar o Projeto na Sua Máquina

Para que o projeto rode perfeitamente no computador sem conflitos com outras versões e bibliotecas já instaladas, preparamos um passo a passo completo utilizando um ambiente virtual:

### 1️⃣ Clone ou baixe o repositório
Baixe o código do projeto para o seu computador e abra a pasta do projeto no seu terminal:
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd <NOME_DA_PASTA>
```

### 2️⃣ Crie o Ambiente Virtual (venv)
O ambiente virtual isola os arquivos deste projeto num cantinho seguro. Execute:
```bash
python -m venv .venv
```

**Ative o Ambiente Virtual!** *(É necessário ativar a `.venv` sempre que for usar o projeto)*
- **No Windows (Prompt de Comando ou PowerShell):**
  ```bash
  .\.venv\Scripts\activate
  ```
- **No Windows (Git Bash):**
  ```bash
  source .venv/Scripts/activate
  ```
- **No Linux ou Mac:**
  ```bash
  source .venv/bin/activate
  ```
> 💡 *Dica:* Quando for ativado, você notará uma marcação `(.venv)` no início da linha de comandos do terminal.

### 3️⃣ Instale as dependências
Com o ambiente ativado, instale os pacotes e bibliotecas que o nosso código precisa:
```bash
pip install flask flask-cors requests pytest
```

### 4️⃣ Ligue o Servidor 
Agora é só colocar o "app" para rodar!
```bash
python src/app.py
```
🎉 Se tudo deu certo, sua API estará disponível localmente acessando o endereço: **http://localhost:3000**

---

## 📌 Endpoints (Rotas da API)

Com o servidor rodando, você fará as requisições acessando as rotas da nossa aplicação. Abaixo explicamos cada uma delas. 

### 🟢 1. Health Check (Verificação de Status)
Testa se a API está online, indicando também o horário e versão de resposta.
- **Método HTTP:** `GET`
- **Rota:** `/api/v1/health`
- **Exemplo no navegador:** [http://localhost:3000/api/v1/health](http://localhost:3000/api/v1/health)

### 🌤️ 2. Buscar Clima da Cidade
Aciona as APIs de dados geográficos e climáticos, e devolve a temperatura (mín/máx) de hoje para o município consultado.
- **Método HTTP:** `GET`
- **Rota:** `/api/v1/clima/<nome_da_cidade>`
- **Exemplo no navegador:** [http://localhost:3000/api/v1/clima/Fortaleza](http://localhost:3000/api/v1/clima/Fortaleza)

### 🏙️ 3. Listar Cidades por Estado (UF)
Lista municípios que se encontram no estado brasileiro passado por sigla. Você pode definir a quantidade de cidades ao manipular a variável `limite`.
- **Método HTTP:** `GET`
- **Rota:** `/api/v1/cidades/<sigla_da_uf>?limite=<opcional>`
- **Exemplo no navegador:** [http://localhost:3000/api/v1/cidades/CE?limite=5](http://localhost:3000/api/v1/cidades/CE?limite=5)

---

## 🧪 Como Rodar os Testes Automatizados

O projeto vem acompanhado de testes garantindo a segurança de nossas regras contra erros futuros. 
Para rodar nosso ambiente de testes (`pytest`), mantenha a **`.venv`** ativada e rode direto na pasta raiz do projeto:
```bash
pytest tests/
```

---

## 📬 Postman (Coleção de Rotas Prontas)

Quer testar a API com um programa profissional que seu professor vai amar, direto ao ponto? Nós facilitamos essa parte!
1. Olhe na pasta `docs/` e você encontrará o arquivo `postman_collection.json`.
2. Abra seu **Postman**.
3. Clique em **Import** (menu do canto superior esquerdo da área de trabalho do Postman).
4. Arraste ou selecione nosso arquivo. Pronto! Todas as rotas já estarão devidamente configuradas numa pasta para você dar "Send" a vontade.