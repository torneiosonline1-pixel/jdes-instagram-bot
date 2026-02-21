#!/usr/bin/env python3
"""
JDES Instagram Direct Bot - Webhook Handler
Atendimento automático para escola de futebol JDES no Instagram Direct
"""

import json
import os
import sys
import time
from datetime import datetime

# Configurações do JDES
JDES_CONFIG = {
    "nome": "JDES - Escola de Futebol",
    "respostas_rapidas": {
        "saudacao": "Olá! ⚽ Bem-vindo à JDES - Escola de Futebol! Como posso ajudar você hoje?\n\n1️⃣ Informações sobre matrículas\n2️⃣ Horários de treinos\n3️⃣ Turmas disponíveis\n4️⃣ Preços e valores\n5️⃣ Localização\n6️⃣ Falar com atendente humano",
        "matricula": "📝 Para matrículas na JDES:\n\n• Idade: 4 a 17 anos\n• Documentos: RG e comprovante de residência\n• Avaliação física gratuita\n\n👉 Quer agendar uma aula experimental? Me envie o nome e idade do aluno!",
        "horarios": "⏰ Horários de treinos JDES:\n\n🏟️ Campo Principal:\n• Seg/Qua/Sex: 16h, 17h, 18h\n• Sáb: 09h, 10h, 11h\n\n🏃 Grupos por idade:\n• Sub-7: 16h\n• Sub-10: 17h\n• Sub-13: 18h\n• Sub-17: Sáb 09h\n\nQual faixa etária?",
        "valores": "💰 Investimento JDES:\n\n• Mensalidade: A partir de R$ 149,90\n• Matrícula: Gratuita (promoção)\n• Uniforme: Kit R$ 189,90\n• Desconto: 10% (2º filho), 15% (3º+)\n\nQuer saber valores específicos de uma turma?",
        "localizacao": "📍 Onde estamos:\n\n🏟️ JDES - Centro de Treinamento\n[Endereço real da JDES]\n\n📱 WhatsApp: [número]\n📧 Email: contato@jdes.com.br\n\nVenha fazer uma aula experimental gratuita!",
        "humano": "👨‍💼 Transferindo para atendente humano...\n\n⏰ Horário de atendimento:\nSeg-Sex: 08h às 20h\nSáb: 08h às 12h\n\nDeixe sua mensagem que responderemos em breve!",
    }
}

class JDESInstagramBot:
    """Bot de atendimento JDES para Instagram Direct"""
    
    def __init__(self):
        self.conversas = {}  # Armazenar contexto de conversas
        self.log_file = "/data/.openclaw/workspace/jdes-instagram-bot/logs/conversas.log"
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
    
    def log(self, sender_id, mensagem, resposta):
        """Registrar conversa no log"""
        timestamp = datetime.now().isoformat()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{sender_id}] User: {mensagem[:100]}\n")
            f.write(f"[{timestamp}] [{sender_id}] Bot: {resposta[:100]}\n")
            f.write("\n")
    
    def processar_mensagem(self, sender_id, mensagem):
        """Processar mensagem recebida e retornar resposta"""
        mensagem_lower = mensagem.lower().strip()
        
        # Detectar intenção
        resposta = self.detectar_intencao(mensagem_lower)
        
        # Salvar contexto
        if sender_id not in self.conversas:
            self.conversas[sender_id] = {"etapa": "inicio", "historico": []}
        
        self.conversas[sender_id]["historico"].append({
            "user": mensagem,
            "bot": resposta,
            "timestamp": time.time()
        })
        
        # Log
        self.log(sender_id, mensagem, resposta)
        
        return resposta
    
    def detectar_intencao(self, mensagem):
        """Detectar intenção da mensagem e retornar resposta apropriada"""
        
        # Saudações
        saudacoes = ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite", 
                     "hey", "e aí", "opa", "oi tudo bem"]
        if any(s in mensagem for s in saudacoes):
            return JDES_CONFIG["respostas_rapidas"]["saudacao"]
        
        # Matrícula / Inscrição
        palavras_matricula = ["matricula", "matrícula", "inscrição", "inscricao", 
                              "cadastro", "fazer", "entrar", "participar", "vaga"]
        if any(p in mensagem for p in palavras_matricula):
            return JDES_CONFIG["respostas_rapidas"]["matricula"]
        
        # Horários
        palavras_horario = ["horario", "horário", "horários", "horas", "treino", 
                            "aula", "quando", "dias", "funciona", "aberto"]
        if any(p in mensagem for p in palavras_horario):
            return JDES_CONFIG["respostas_rapidas"]["horarios"]
        
        # Valores
        palavras_valor = ["preço", "preco", "valor", "mensalidade", "custa", 
                          "pagar", "dinheiro", "investimento", "barato", "desconto"]
        if any(p in mensagem for p in palavras_valor):
            return JDES_CONFIG["respostas_rapidas"]["valores"]
        
        # Localização
        palavras_local = ["onde", "endereço", "local", "fica", "chegar", 
                          "morro", "bairro", "campo", "estádio"]
        if any(p in mensagem for p in palavras_local):
            return JDES_CONFIG["respostas_rapidas"]["localizacao"]
        
        # Números de opção do menu
        if mensagem in ["1", "matrículas", "matriculas"]:
            return JDES_CONFIG["respostas_rapidas"]["matricula"]
        elif mensagem in ["2", "horários", "horarios", "treinos"]:
            return JDES_CONFIG["respostas_rapidas"]["horarios"]
        elif mensagem in ["3", "turmas"]:
            return JDES_CONFIG["respostas_rapidas"]["horarios"]
        elif mensagem in ["4", "preços", "precos", "valores"]:
            return JDES_CONFIG["respostas_rapidas"]["valores"]
        elif mensagem in ["5", "localização", "localizacao", "onde"]:
            return JDES_CONFIG["respostas_rapidas"]["localizacao"]
        elif mensagem in ["6", "atendente", "humano", "pessoa", "funcionário", "gerente"]:
            return JDES_CONFIG["respostas_rapidas"]["humano"]
        
        # Resposta genérica para mensagens não reconhecidas
        return "Desculpe, não entendi bem 🤔\n\nPosso ajudar com:\n1️⃣ Matrículas\n2️⃣ Horários\n3️⃣ Turmas\n4️⃣ Preços\n5️⃣ Localização\n6️⃣ Falar com atendente\n\nEscolha uma opção ou escreva sua pergunta!"

# Instância global do bot
bot = JDESInstagramBot()

def handle_webhook(data):
    """
    Receber webhook do Instagram/Meta
    Formato esperado: {"sender_id": "...", "message": "...", "timestamp": "..."}
    """
    sender_id = data.get("sender_id", "unknown")
    mensagem = data.get("message", "")
    
    resposta = bot.processar_mensagem(sender_id, mensagem)
    
    return {
        "status": "success",
        "sender_id": sender_id,
        "response": resposta
    }

if __name__ == "__main__":
    # Teste local
    if len(sys.argv) > 1:
        mensagem_teste = sys.argv[1]
        resultado = bot.processar_mensagem("test_user", mensagem_teste)
        print(f"Entrada: {mensagem_teste}")
        print(f"Resposta:\n{resultado}")
    else:
        print("JDES Instagram Bot - Pronto para atendimento!")
        print("Modo de teste: python webhook_handler.py \"sua mensagem\"")
