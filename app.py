#!/usr/bin/env python3
"""
JDES Instagram Bot - Flask App para Render
Servidor web para receber webhooks do Instagram/Meta
"""

import json
import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify

# Adicionar path do bot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Corrigido: era 'patd' typo, agora 'path'
from webhook_handler import bot

app = Flask(__name__)

# Configurações
PORT = int(os.environ.get('PORT', 8765))
LOG_FILE = '/data/.openclaw/workspace/jdes-instagram-bot/logs/server.log'

# Garantir que diretório de logs existe
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_message(message):
    """Salvar log no arquivo"""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {message}")
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

@app.route('/', methods=['GET'])
def home():
    """Pagina inicial - status do bot"""
    return jsonify({
        "status": "ok",
        "message": "JDES Instagram Bot Server online!",
        "bot_name": "JDES Futebol Bot",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /": "Status",
            "POST /webhook": "Receber mensagens do Instagram",
            "POST /test": "Testar bot",
            "GET /health": "Health check"
        }
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check para Render"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Receber webhooks do Instagram/Meta"""
    
    # GET - Verificação do webhook (Meta webhook verification)
    if request.method == 'GET':
        challenge = request.args.get('hub.challenge')
        if challenge:
            log_message(f"✅ Verificação de webhook recebida: {challenge}")
            return challenge, 200
        
        return jsonify({"status": "ok", "method": "GET"})
    
    # POST - Receber mensagens
    if request.method == 'POST':
        try:
            data = request.get_json() or {}
            log_message(f"📩 Webhook recebido: {json.dumps(data)[:200]}...")
            
            # Extrair mensagem do formato Instagram/Meta
            sender_id = data.get('sender', {}).get('id', 'unknown')
            message_text = data.get('message', {}).get('text', '')
            
            # Formato webhook Meta (mais complexo)
            if not message_text and 'entry' in data:
                try:
                    entry = data['entry'][0]
                    messaging = entry['messaging'][0]
                    sender_id = messaging['sender']['id']
                    message_text = messaging['message']['text']
                except (KeyError, IndexError):
                    pass
            
            # Processar com o bot
            if message_text:
                resposta = bot.processar_mensagem(sender_id, message_text)
                log_message(f"🤖 Resposta para {sender_id}: {resposta[:100]}...")
                
                return jsonify({
                    "status": "success",
                    "sender_id": sender_id,
                    "message_received": message_text,
                    "bot_response": resposta
                })
            else:
                return jsonify({
                    "status": "error",
                    "message": "No text message found"
                }), 400
                
        except Exception as e:
            log_message(f"❌ Erro: {str(e)}")
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

@app.route('/test', methods=['POST'])
def test_bot():
    """Endpoint para testar o bot"""
    try:
        data = request.get_json() or {}
        mensagem = data.get('message', 'oi')
        sender = data.get('sender_id', 'test')
        
        resposta = bot.processar_mensagem(sender, mensagem)
        
        return jsonify({
            "status": "success",
            "test": True,
            "input": mensagem,
            "output": resposta
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    print(f"""
🚀 JDES INSTAGRAM BOT SERVER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 Porta: {PORT}
🌐 Local: http://localhost:{PORT}
📩 Webhook: POST http://localhost:{PORT}/webhook
🧪 Teste: POST http://localhost:{PORT}/test
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    app.run(host='0.0.0.0', port=PORT, debug=False)
