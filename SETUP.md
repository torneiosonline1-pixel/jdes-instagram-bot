# 🤖 JDES Instagram Direct Bot - Guia de Instalação

Bot de atendimento automático para a escola de futebol JDES no Instagram Direct.

## ✅ Status Atual

**BOT CRIADO E TESTADO** ✅
- Handler Python configurado
- Respostas automáticas
- Logs de conversas

---

## 📋 Pré-requisitos (Você precisa fazer)

Antes de conectar ao Instagram, você precisa criar algumas coisas no Meta:

### 1. Conta Business
- [ ] Converter o perfil @jdesfutebol para **Conta Business** ou **Creator**
- [ ] Acessar: Instagram → Configurações → Conta → Tipo de Conta

### 2. Facebook Business
- [ ] Criar página no Facebook Business: https://business.facebook.com
- [ ] Conectar Instagram à página

### 3. Meta Developers App
- [ ] Acessar: https://developers.facebook.com
- [ ] Criar novo app → Tipo: "Outro"
- [ ] Adicionar permissões:
  - `instagram_basic`
  - `instagram_messaging`
  - `pages_messaging`

### 4. Configurar Webhook (Precisa de URL pública)
Opções:
- **Ngrok** (dev/teste): `ngrok http 8080`
- **Servidor próprio**
- **Heroku/Vercel**

---

## 🚀 Arquivos Criados

### `webhook_handler.py`
Bot principal com:
- Respostas automáticas
- Detecção de intenções
- Menu interativo
- Logs de conversas

### Fluxos de conversa automáticos:
1. **Saudação** → Menu principal
2. **Matrículas** → Informações sobre inscrição
3. **Horários** → Tabela de treinos por idade
4. **Preços** → Valores e descontos
5. **Localização** → Endereço e contatos
6. **Atendente** → Transferência para humano

---

## 🔧 Próximos Passos

1. **Você precisa**:
   - Criar app no Meta Developers
   - Configurar webhook público
   - Autorizar permissões

2. **Eu conecto**:
   - Assim que tiver webhook URL, configuro recebimento
   - Integro respostas automáticas
   - Configuro notificações

---

## 💬 Exemplo de Conversa

```
Usuário: "Oi"
Bot: "Olá! ⚽ Bem-vindo à JDES! ..."

Usuário: "Quero matricular meu filho"
Bot: "📝 Para matrículas na JDES..."

Usuário: "2"
Bot: "⏰ Horários de treinos JDES..."
```

---

## 📁 Estrutura

```
jdes-instagram-bot/
├── webhook_handler.py    # Bot principal
├── SETUP.md              # Este arquivo
├── logs/
│   └── conversas.log     # Histórico de chats
└── credentials.json        # Tokens (a ser criado)
```

---

## ⚡ Quer começar?

Me confirme quando você tiver:
1. ✅ App criado no Meta Developers
2. ✅ Página Facebook Business conectada
3. ✅ URL pública para webhook (ngrok ou servidor)

Aí eu finalizo a conexão! 🚀
