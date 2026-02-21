#!/usr/bin/env python3
"""
JDES Instagram Bot - Flask App para Render
Bot de atendimento - VERSÃO SIMPLES SEM DEPENDÊNCIAS EXTERNAS
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações
PORT = int(os.environ.get('PORT', 8765))

# Respostas do bot
RESPOSTAS = {
    "saudacao": """Olá! ⚽ Bem-vindo à JDES - Escola de Futebol! Como posso ajudar você hoje?

1️⃣ Informações sobre matrículas
2️⃣ Horários de treinos
3️⃣ Turmas disponíveis
4️⃣ Preços e valores
5️⃣ Localização
6️⃣ Falar com atendente humano""",
    "matricula": """📝 Para matrículas na JDES:

• Idade: 4 a 17 anos
• Documentos: RG e comprovante de residência
• Avaliação física gratuita

👉 Quer agendar uma aula experimental? Me envie o nome e idade do aluno!""",
    "horarios": """⏰ Horários de treinos JDES:

🏟️ Campo Principal:
• Seg/Qua/Sex: 16h, 17h, 18h
• Sáb: 09h, 10h, 11h

🏃 Grupos por idade:
• Sub-7: 16h
• Sub-10: 17h
• Sub-13: 18h
• Sub-17: Sáb 09h

Qual faixa etária?""",
    "valores": """💰 Investimento JDES:

• Mensalidade: A partir de R$ 149,90
• Matrícula: Gratuita (promoção)
• Uniforme: Kit R$ 189,90
• Desconto: 10% (2º filho), 15% (3º+)

Quer saber valores específicos de uma turma?""",
    "localizacao": """📍 Onde estamos:

🏟️ JDES - Centro de Treinamento
[Endereço real da JDES]

📱 WhatsApp: [número]
📧 Email: contato@jdes.com.br

Venha fazer uma aula experimental gratuita!""",
    "humano": """👨‍💼 Transferindo para atendente humano...

⏰ Horário de atendimento:
Seg-Sex: 08h às 20h
Sáb: 08h às 12h

Deixe sua mensagem que responderemos em breve!""",
    "erro": """Desculpe, não entendi bem 🤔

Posso ajudar com:
1️⃣ Matrículas
2️⃣ Horários
3️⃣ Turmas
4️⃣ Preços
5️⃣ Localização
6️⃣ Falar com atendente

Escolha uma opção ou escreva sua pergunta!"""
}

def processar_msg(texto):
    """Processar mensagem e retornar resposta"""
    msg = texto.lower().strip()
    
    # Saudações
    if any(x in msg for x in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", "hey", "opa"]):
        return RESPOSTAS["saudacao"]
    
    # Matrícula
    if any(x in msg for x in ["matricula", "matrícula", "inscrição", "inscricao", "cadastro", "vaga", "entrar"]):
        return RESPOSTAS["matricula"]
    
    # Horários
    if any(x in msg for x in ["horario", "horário", "horas", "treino", "aula", "quando", "funciona"]):
        return RESPOSTAS["horarios"]
    
    # Valores
    if any(x in msg for x in ["preço", "preco", "valor", "mensalidade", "custa", "pagar", "dinheiro", "desconto"]):
        return RESPOSTAS["valores"]
    
    # Localização
    if any(x in msg for x in ["onde", "endereço", "local", "fica", "chegar", "morro", "bairro"]):
        return RESPOSTAS["localizacao"]
    
    # Menu numérico
    if msg in ["1", "matrículas", "matriculas"]:
        return RESPOSTAS["matricula"]
    elif msg in ["2", "horários", "horarios", "treinos"]:
        return RESPOSTAS["horarios"]
    elif msg in ["3", "turmas"]:
        return RESPOSTAS["horarios"]
    elif msg in ["4", "preços", "precos", "valores"]:
        return RESPOSTAS["valores"]
    elif msg in ["5", "localização", "localizacao", "onde"]:
        return RESPOSTAS["localizacao"]
    elif msg in ["6", "atendente", "humano", "pessoa"]:
        return RESPOSTAS["humano"]
    
    return RESPOSTAS["erro"]

@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "JDES Bot Online", "timestamp": datetime.now().isoformat()})

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        if challenge:
            return challenge, 200
        return jsonify({"status": "ok"})
    
    data = request.get_json() or {}
    sender_id = data.get('sender', {}).get('id', 'unknown')
    msg = data.get('message', {}).get('text', '')
    
    if not msg and 'entry' in data:
        try:
            msg = data['entry'][0]['messaging'][0]['message']['text']
            sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        except:
            pass
    
    if msg:
        resp = processar_msg(msg)
        return jsonify({"status": "success", "response": resp})
    
    return jsonify({"status": "error", "message": "No text"}), 400

@app.route('/test', methods=['POST'])
def teste():
    data = request.get_json() or {}
    msg = data.get('message', 'oi')
    return jsonify({"status": "success", "input": msg, "output": processar_msg(msg)})

if __name__ == '__main__':
    print(f"🚀 JDES Bot rodando na porta {PORT}")
    app.run(host='0.0.0.0', port=PORT)
