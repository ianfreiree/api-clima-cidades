from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone
import requests
import urllib.parse 

app = Flask(__name__)
CORS(app) # Habilita CORS para testes via navegador
app.config['JSON_AS_ASCII'] = False # Suporte a UTF-8

# Endpoint 3: Health Check
@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "versao": "1.0.0",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }), 200

# Endpoint 1: Informações da Cidade com Clima
@app.route('/api/v1/clima/<nome_cidade>', methods=['GET'])
def buscar_clima_cidade(nome_cidade):
    # Tratamento de erro 400: Nome muito curto
    if len(nome_cidade) < 2:
        return jsonify({
            "erro": True,
            "codigo": "NOME_INVALIDO",
            "mensagem": "O nome da cidade deve conter pelo menos 2 caracteres",
            "nome_informado": nome_cidade
        }), 400

    try:
        # PASSO 1: Descobrir Lat e Lon pelo nome da cidade usando Nominatim (OpenStreetMap)
        nome_cidade_url = urllib.parse.quote(nome_cidade)
        # O cabeçalho 'User-Agent' é obrigatório para o Nominatim não bloquear a requisição
        headers = {'User-Agent': 'TrabalhoFaculdadeApp/1.0'}
        url_geo = f"https://nominatim.openstreetmap.org/search?q={nome_cidade_url},Brazil&format=json&limit=1"
        
        resposta_geo = requests.get(url_geo, headers=headers)
        dados_geo = resposta_geo.json()

        # Tratamento de erro 404: Cidade não encontrada
        if not dados_geo:
            return jsonify({
                "erro": True,
                "codigo": "CIDADE_NAO_ENCONTRADA",
                "mensagem": "Nenhuma cidade encontrada com o nome informado",
                "nome_informado": nome_cidade
            }), 404

        lat = dados_geo[0]['lat']
        lon = dados_geo[0]['lon']
        nome_oficial = dados_geo[0].get('name', nome_cidade)
        
        # O Nominatim traz a sigla do estado no display_name às vezes, mas para simplificar
        # e garantir a resposta, vamos pegar uma aproximação baseada no retorno deles
        estado_aproximado = dados_geo[0]['display_name'].split(',')[-2].strip() if len(dados_geo[0]['display_name'].split(',')) > 1 else ""

        # PASSO 2: Buscar clima na Open-Meteo usando a Lat e Lon
        url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min&current=weather_code&timezone=America/Sao_Paulo"
        
        resposta_clima = requests.get(url_clima)
        dados_clima = resposta_clima.json()

        # Pegando a temperatura min/max do dia atual e a condição (weather code)
        temp_min = dados_clima['daily']['temperature_2m_min'][0]
        temp_max = dados_clima['daily']['temperature_2m_max'][0]
        weather_code = dados_clima['current']['weather_code']

        # Dicionário simplificado para mapear os códigos de clima da Open-Meteo
        # Fonte: Documentação WMO Weather interpretation codes
        condicoes = {
            0: "Céu Limpo", 1: "Predominantemente Limpo", 2: "Parcialmente Nublado", 3: "Encoberto",
            45: "Neblina", 48: "Nevoeiro", 51: "Garoa Leve", 61: "Chuva Fraca", 63: "Chuva Moderada",
            65: "Chuva Forte", 80: "Pancadas de Chuva", 95: "Tempestade"
        }
        condicao_texto = condicoes.get(weather_code, "Condição Desconhecida")

        # PASSO 3: Retornar o JSON montado conforme o formato de sucesso
        return jsonify({
            "nome": nome_oficial,
            "estado": estado_aproximado, # Dica: Nominatim pode não retornar só a UF, mas cumpre o requisito de localidade
            "clima": {
                "temperatura_min": temp_min,
                "temperatura_max": temp_max,
                "condicao": condicao_texto,
                "unidades": {
                    "temperatura": "°C"
                }
            },
            "consultado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }), 200

    except (requests.exceptions.RequestException, KeyError):
        # Tratamento de erro 503: Algum serviço externo caiu ou falhou
        return jsonify({
            "erro": True,
            "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
            "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
            "servico": "Nominatim ou Open-Meteo"
        }), 503
    
# Endpoint 2: Listagem de Cidades por Estado
@app.route('/api/v1/cidades/<sigla_uf>', methods=['GET'])
def listar_cidades(sigla_uf):
    # Tratamento de erro 400: Sigla inválida (não tem 2 letras)
    if len(sigla_uf) != 2 or not sigla_uf.isalpha():
        return jsonify({
            "erro": True,
            "codigo": "SIGLA_UF_INVALIDA",
            "mensagem": "A sigla do estado deve conter exatamente 2 letras",
            "sigla_uf_informada": sigla_uf
        }), 400

    # Pega o parâmetro opcional 'limite' na URL (padrão 10)
    limite = request.args.get('limite', default=10, type=int)

    # Chamada para a API do IBGE
    url_ibge = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{sigla_uf.upper()}/municipios"
    
    try:
        resposta = requests.get(url_ibge)
        
        # Tratamento de erro 404: UF não encontrada (IBGE retorna vazio '[]' para UF inválida)
        if resposta.status_code != 200 or not resposta.json():
            return jsonify({
                "erro": True,
                "codigo": "UF_NAO_ENCONTRADA",
                "mensagem": "Estado com a sigla informada não foi encontrado",
                "sigla_uf_informada": sigla_uf
            }), 404
            
        dados = resposta.json()
        
        # Formata a lista pegando só o nome e aplicando o limite
        cidades_formatadas = [{"nome": cidade["nome"]} for cidade in dados[:limite]]
        
        return jsonify({
            "uf": sigla_uf.upper(),
            "quantidade_retornada": len(cidades_formatadas),
            "cidades": cidades_formatadas,
            "consultado_em": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }), 200

    except requests.exceptions.RequestException:
        # Tratamento de erro 503: Serviço do IBGE caiu
        return jsonify({
            "erro": True,
            "codigo": "SERVICO_EXTERNO_INDISPONIVEL",
            "mensagem": "Não foi possível obter dados do serviço externo. Tente novamente em alguns instantes",
            "servico": "IBGE"
        }), 503
    
if __name__ == '__main__':
    # API rodando obrigatoriamente na porta 3000
    app.run(port=3000, debug=True)