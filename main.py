from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# ============================================
# DATELE TALE DE CONTACT
# ============================================
WHATSAPP_NUMBER = '0730176058'
CONTACT_EMAIL = 'contact@hakunadesign.ro'

# ============================================
# INTERFAȚA DARIA - SIMPLĂ ȘI ELEGANTĂ
# ============================================

CHAT_WIDGET = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .daria-chat-widget {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 999999;
        }
        
        .daria-chat-button {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(145deg, #667eea, #764ba2);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            font-size: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
        }
        
        .daria-chat-button:hover {
            transform: scale(1.1);
        }
        
        .daria-chat-box {
            position: absolute;
            bottom: 90px;
            right: 0;
            width: 400px;
            height: 600px;
            background: white;
            border-radius: 25px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
            display: none;
            flex-direction: column;
            overflow: hidden;
        }
        
        .daria-chat-box.open {
            display: flex;
        }
        
        .daria-header {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .daria-avatar {
            width: 45px;
            height: 45px;
            background: rgba(255,255,255,0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
        }
        
        .daria-header-info {
            flex: 1;
        }
        
        .daria-header-info h3 {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .daria-header-info p {
            font-size: 12px;
            opacity: 0.9;
        }
        
        .daria-header button {
            background: rgba(255,255,255,0.2);
            border: none;
            color: white;
            width: 35px;
            height: 35px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
        }
        
        .daria-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8faff;
        }
        
        .daria-message {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
        }
        
        .daria-message.bot {
            align-items: flex-start;
        }
        
        .daria-message.user {
            align-items: flex-end;
        }
        
        .daria-message-content {
            max-width: 80%;
            padding: 12px 18px;
            border-radius: 20px;
            font-size: 14px;
            line-height: 1.5;
            white-space: pre-line;
        }
        
        .bot .daria-message-content {
            background: white;
            color: #1a1f36;
            border-bottom-left-radius: 5px;
        }
        
        .user .daria-message-content {
            background: #667eea;
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .daria-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 15px;
            background: white;
            border-top: 1px solid #edf2f7;
        }
        
        .daria-suggestion {
            background: #f0f4ff;
            border: none;
            padding: 8px 15px;
            border-radius: 25px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s;
            color: #4a5568;
        }
        
        .daria-suggestion:hover {
            background: #667eea;
            color: white;
        }
        
        .daria-input-area {
            padding: 15px;
            background: white;
            border-top: 1px solid #edf2f7;
            display: flex;
            gap: 10px;
        }
        
        .daria-input-area input {
            flex: 1;
            padding: 12px 18px;
            border: 2px solid #e2e8f0;
            border-radius: 30px;
            outline: none;
            font-size: 14px;
        }
        
        .daria-input-area input:focus {
            border-color: #667eea;
        }
        
        .daria-input-area button {
            width: 45px;
            height: 45px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
        }
        
        .typing-indicator {
            display: flex;
            gap: 5px;
            padding: 12px 18px;
            background: white;
            border-radius: 20px;
            width: fit-content;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background: #667eea;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
            30% { transform: translateY(-10px); opacity: 1; }
        }
        
        .offer-box {
            background: linear-gradient(145deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: center;
        }
        
        .offer-btn {
            background: white;
            color: #667eea;
            border: none;
            padding: 10px 20px;
            border-radius: 30px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 10px;
        }
        
        .contact-buttons {
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }
        
        .contact-btn {
            flex: 1;
            padding: 10px;
            border-radius: 25px;
            border: none;
            cursor: pointer;
            font-weight: 600;
            font-size: 13px;
        }
        
        .whatsapp-btn {
            background: #25D366;
            color: white;
        }
        
        .email-btn {
            background: #667eea;
            color: white;
        }
    </style>
</head>
<body>
    <div class="daria-chat-widget">
        <button class="daria-chat-button" onclick="toggleChat()">
            💬
        </button>
        
        <div class="daria-chat-box" id="dariaChatBox">
            <div class="daria-header">
                <div class="daria-avatar">🤖</div>
                <div class="daria-header-info">
                    <h3>Daria - Asistent Virtual</h3>
                    <p>🟢 Online | Răspund în 5 secunde</p>
                </div>
                <button onclick="toggleChat()">×</button>
            </div>
            
            <div class="daria-messages" id="dariaMessages">
                <div class="daria-message bot">
                    <div class="daria-message-content">
                        👋 Bună! Sunt Daria.

Cu ce te pot ajuta? Scrie direct ce cauți:
• site de prezentare
• magazin online
• site piese auto
• aplicație mobilă
• prețuri
• ofertă
                    </div>
                </div>
            </div>
            
            <div class="daria-suggestions">
                <button class="daria-suggestion" onclick="sendMessage('site web')">🌐 Site web</button>
                <button class="daria-suggestion" onclick="sendMessage('magazin online')">🛒 Magazin</button>
                <button class="daria-suggestion" onclick="sendMessage('piese auto')">🚗 Auto</button>
                <button class="daria-suggestion" onclick="sendMessage('aplicație')">📱 Aplicație</button>
                <button class="daria-suggestion" onclick="sendMessage('prețuri')">💰 Prețuri</button>
                <button class="daria-suggestion" onclick="sendMessage('ofertă')">🎁 Ofertă</button>
            </div>
            
            <div class="daria-input-area">
                <input type="text" id="dariaInput" placeholder="Scrie aici..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">➤</button>
            </div>
        </div>
    </div>

    <script>
        let context = {
            lastIntent: null,
            lastOffer: null
        };
        
        function toggleChat() {
            document.getElementById('dariaChatBox').classList.toggle('open');
        }
        
        function addMessage(text, isBot = true) {
            const div = document.getElementById('dariaMessages');
            const msgDiv = document.createElement('div');
            msgDiv.className = `daria-message ${isBot ? 'bot' : 'user'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'daria-message-content';
            contentDiv.textContent = text;
            
            msgDiv.appendChild(contentDiv);
            div.appendChild(msgDiv);
            div.scrollTop = div.scrollHeight;
        }
        
        function showTyping() {
            const div = document.getElementById('dariaMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'daria-message bot';
            typingDiv.id = 'typingIndicator';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'typing-indicator';
            contentDiv.innerHTML = '<span></span><span></span><span></span>';
            
            typingDiv.appendChild(contentDiv);
            div.appendChild(typingDiv);
            div.scrollTop = div.scrollHeight;
        }
        
        function removeTyping() {
            const typing = document.getElementById('typingIndicator');
            if (typing) typing.remove();
        }
        
        function sendMessage() {
            const input = document.getElementById('dariaInput');
            let message = input.value.trim();
            
            if (!message && arguments[0]) {
                message = arguments[0];
            }
            
            if (!message) return;
            
            input.value = '';
            addMessage(message, false);
            showTyping();
            
            fetch('/daria/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: message,
                    context: context
                })
            })
            .then(res => res.json())
            .then(data => {
                removeTyping();
                addMessage(data.response);
                context = data.context;
                
                if (data.offer) {
                    showOffer(data.offer);
                }
            });
        }
        
        function showOffer(offer) {
            const div = document.getElementById('dariaMessages');
            const offerDiv = document.createElement('div');
            offerDiv.className = 'daria-message bot';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'offer-box';
            contentDiv.innerHTML = `
                <h4>🎁 OFERTĂ SPECIALĂ</h4>
                <div style="font-size: 28px; font-weight: bold; margin: 10px 0;">${offer.discount}% REDUCERE</div>
                <p>Pentru ${offer.service}</p>
                <button class="offer-btn" onclick="showContact()">Vreau oferta</button>
            `;
            
            offerDiv.appendChild(contentDiv);
            div.appendChild(offerDiv);
            div.scrollTop = div.scrollHeight;
        }
        
        function showContact() {
            addMessage(`Alege cum preferi să discutăm:`, false);
            
            const div = document.getElementById('dariaMessages');
            const contactDiv = document.createElement('div');
            contactDiv.className = 'daria-message bot';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'daria-message-content';
            contentDiv.innerHTML = `
                <div class="contact-buttons">
                    <button class="contact-btn whatsapp-btn" onclick="window.open('https://wa.me/${WHATSAPP_NUMBER}')">📱 WhatsApp</button>
                    <button class="contact-btn email-btn" onclick="window.location.href='mailto:${CONTACT_EMAIL}'">📧 Email</button>
                </div>
            `;
            
            contactDiv.appendChild(contentDiv);
            div.appendChild(contactDiv);
            div.scrollTop = div.scrollHeight;
        }
    </script>
</body>
</html>
"""

# ============================================
# BACKEND - LOGICĂ SIMPLĂ ȘI CURATĂ
# ============================================

@app.route('/daria')
def daria_widget():
    return render_template_string(CHAT_WIDGET)

@app.route('/daria/chat', methods=['POST'])
def daria_chat():
    data = request.json
    msg = data.get('message', '').lower()
    ctx = data.get('context', {})
    
    # Detectează ce vrea utilizatorul
    if any(word in msg for word in ['buna', 'salut', 'hey']):
        resp = "Bună! Ce serviciu te interesează?"
    
    elif 'prezentare' in msg or ('site' in msg and 'web' in msg):
        resp = """🌐 **Site Prezentare - €499**

Include:
• Design responsive
• 6 pagini + contact
• Optimizat pentru mobil
• Suport 30 zile

🎁 Îți pot face o ofertă specială. Vrei?"""
        ctx['lastOffer'] = {'service': 'site prezentare', 'discount': 15}
    
    elif 'magazin' in msg or 'e-commerce' in msg:
        resp = """🛒 **Magazin Online - €1999**

Include:
• 1000 produse
• Plată online
• Integrare curier
• Chat WhatsApp
• Suport 60 zile

🎁 Reducere 20% pentru luna asta. Te interesează?"""
        ctx['lastOffer'] = {'service': 'magazin online', 'discount': 20}
    
    elif 'auto' in msg or 'piese' in msg:
        resp = """🚗 **Site Piese Auto - €999**

Include:
• Catalog piese
• Căutare după VIN
• 3 luni hosting gratuit
• Optimizat pentru mobil

🎁 Reducere 15% pentru început de drum!"""
        ctx['lastOffer'] = {'service': 'site piese auto', 'discount': 15}
    
    elif 'aplicație' in msg or 'app' in msg or 'mobil' in msg:
        resp = """📱 **Aplicații Mobile - €499**

Alege:
• iOS (Swift)
• Android (Kotlin)
• Hibrid (Flutter)

🎁 Primești consultanță gratuită!"""
    
    elif 'preț' in msg or 'cost' in msg:
        resp = """💰 **Prețuri:**

• Site prezentare: €499
• Magazin online: €1999
• Site piese auto: €999
• Aplicații: €499 - €9800
• SEO: €350/lună"""
    
    elif 'ofertă' in msg:
        discount = random.randint(15, 25)
        resp = f"🎁 Îți ofer {discount}% reducere la orice serviciu. Vrei să discutăm?"
        ctx['lastOffer'] = {'service': 'orice serviciu', 'discount': discount}
    
    elif 'contact' in msg:
        resp = f"""📞 **Contact:**
WhatsApp: {WHATSAPP_NUMBER}
Email: {CONTACT_EMAIL}"""
    
    else:
        resp = """Nu sunt sigură. Poți alege:
• site web
• magazin online
• piese auto
• aplicație
• prețuri
• ofertă"""
    
    return jsonify({
        'response': resp,
        'context': ctx,
        'offer': ctx.get('lastOffer')
    })

@app.route('/')
def home():
    return "Daria e online! Accesează <a href='/daria'>/daria</a>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
