import pytest
import sys
import os

# Adiciona a pasta raiz ao path para conseguir importar o src.app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_clima_cidade_valida(client):
    """Verifica resposta correta para nome de cidade válido"""
    resposta = client.get('/api/v1/clima/Fortaleza')
    dados = resposta.get_json()
    
    assert resposta.status_code == 200
    assert "clima" in dados
    assert "temperatura_min" in dados["clima"]

def test_clima_cidade_nao_encontrada(client):
    """Verifica tratamento de erro para cidade não encontrada"""
    resposta = client.get('/api/v1/clima/CidadeInexistente12345')
    dados = resposta.get_json()
    
    assert resposta.status_code == 404
    assert dados["erro"] is True
    assert dados["codigo"] == "CIDADE_NAO_ENCONTRADA"