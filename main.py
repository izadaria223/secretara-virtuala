from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import random
import json

app = Flask(__name__)
CORS(app)  # Permite conexiuni de pe site-ul tău

# ============================================
# BAZA DE DATE - SERVICII ȘI PREȚURI (din site-ul tău)
# ============================================

SERVICES = {
    "site_prezentare": {
        "name": "Site Prezentare",
        "price": "€499",
        "url": "/dezvoltare-site-prezentare",
        "features": ["Design responsive", "6 pagini + contact", "Formular contact", "Link-uri social media"]
    },
    "magazin_online": {
        "name": "Magazin Online Profesional",
        "price": "€1999",
        "url": "/magazin-online",
        "features": ["Temă profesională", "Până la 100 produse", "Plată online", "Integrare curier", "GDPR", "Chat WhatsApp"]
    },
    "site_auto": {
        "name": "Site Piese Auto",
        "price": "€999 - €7900",
        "url": "/site-auto",
        "features": ["Catalog piese auto", "Căutare după VIN", "Căutare după marcă/model", "Import piese din Excel"]
    },
    "aplicatii_ios": {
        "name": "Aplicații iOS",
        "price": "€499 - €9800",
        "url": "/aplicatii-ios",
        "features": ["Swift/SwiftUI", "Design Apple HIG", "Publicare App Store"]
    },
    "aplicatii_android": {
        "name": "Aplicații Android",
        "price": "€499 - €9800",
        "url": "/aplicatii-android",
        "features": ["Kotlin", "Material You", "Publicare Google Play"]
    },
    "seo": {
        "name": "Optimizare SEO",
        "price": "€350",
        "url": "/servicii-seo",
        "features": ["Analiză site", "Optimizare cuvinte cheie", "Rapoarte lunare"]
    },
    "branding": {
        "name": "Branding",
        "price": "Personalizat",
        "url": "/branding",
        "features": ["Logo", "Identitate vizuală", "Ghid de brand"]
    },
    "social_media": {
        "name": "Social Media",
        "price": "Personalizat",
        "url": "/social-media",
        "features": ["Management conturi", "Creare conținut", "Campanii"]
    }
}

# PACHETE POPULARE
PACKAGES = {
    "star_website": {
        "name": "STAR WEBSITE",
        "price": "€999",
        "features": ["Site piese auto", "Catalog de bază", "Căutare după titlu", "3 luni hosting gratuit"]
    },
    "professional_store": {
        "name": "MAGAZIN PROFESIONAL",
        "price": "€1999",
        "features": ["Magazin online complet", "100 produse", "Plată online", "Integrare curier"]
    },
    "mobile_app": {
        "name": "APLICAȚIE START",
        "price": "€499",
        "features": ["Aplicație iOS sau Android", "3 ecrane", "Notificări push", "Publicare în Store"]
    }
}

# ============================================
# INTERFAȚA DARIA (CHAT WIDGET)
# ============================================

CHAT_WIDGET = """
<!DOCTYPE html>
<html>
<head>
    <style>
        .daria-chat-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999999;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }
        
        .daria-chat-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            font-size: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.3s;
        }
        
        .daria-chat-button:hover {
            transform: scale(1.1);
        }
        
        .daria-chat-box {
            position: absolute;
            bottom: 80px;
            right: 0;
            width: 350px;
            height: 500px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 5px 40px rgba(0,0,0,0.16);
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
            padding: 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .daria-header h3 {
            margin: 0;
            font-size: 16px;
        }
        
        .daria-header button {
            background: none;
            border: none;
            color: white;
            cursor: pointer;
            font-size: 20px;
        }
        
        .daria-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #f5f5f5;
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
            padding: 10px 15px;
            border-radius: 15px;
            font-size: 14px;
            line-height: 1.4;
        }
        
        .bot .daria-message-content {
            background: white;
            color: #333;
            border-bottom-left-radius: 5px;
        }
        
        .user .daria-message-content {
            background: #667eea;
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        .daria-input-area {
            padding: 15px;
            background: white;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        
        .daria-input-area input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
        }
        
        .daria-input-area button {
            background: #667eea;
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .daria-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 10px 15px;
            background: white;
        }
        
        .daria-suggestion {
            background: #f0f0f0;
            border: none;
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 12px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .daria-suggestion:hover {
            background: #667eea;
            color: white;
        }
        
        .typing-indicator {
            display: flex;
            gap: 5px;
            padding: 10px 15px;
            background: white;
            border-radius: 15px;
            width: fit-content;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            background: #999;
            border-radius: 50%;
            animation: typing 1s infinite ease-in-out;
        }
        
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-10px); }
        }
        
        .offer-box {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            text-align: center;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
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
                <h3>💬 Daria - Secretara Virtuală</h3>
                <button onclick="toggleChat()">×</button>
            </div>
            
            <div class="daria-messages" id="dariaMessages">
                <div class="daria-message bot">
                    <div class="daria-message-content">
                        Bună! Eu sunt Daria, secretara virtuală. Cu ce te pot ajuta azi?
                    </div>
                </div>
            </div>
            
            <div class="daria-suggestions" id="dariaSuggestions">
                <button class="daria-suggestion" onclick="sendMessage('servicii')">🔧 Servicii</button>
                <button class="daria-suggestion" onclick="sendMessage('preturi')">💰 Prețuri</button>
                <button class="daria-suggestion" onclick="sendMessage('site auto')">🚗 Site auto</button>
                <button class="daria-suggestion" onclick="sendMessage('aplicații')">📱 Aplicații</button>
                <button class="daria-suggestion" onclick="sendMessage('contact')">📞 Contact</button>
                <button class="daria-suggestion" onclick="sendMessage('ofertă')">🎁 Ofertă specială</button>
            </div>
            
            <div class="daria-input-area">
                <input type="text" id="dariaInput" placeholder="Scrie un mesaj..." onkeypress="if(event.key==='Enter') sendMessage(this.value)">
                <button onclick="sendMessage(document.getElementById('dariaInput').value)">
                    ➤
                </button>
            </div>
        </div>
    </div>

    <script>
        let conversationContext = {
            step: 'initial',
            userNeeds: null,
            lastOffer: null
        };
        
        function toggleChat() {
            const box = document.getElementById('dariaChatBox');
            box.classList.toggle('open');
        }
        
        function addMessage(text, isBot = true) {
            const messagesDiv = document.getElementById('dariaMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `daria-message ${isBot ? 'bot' : 'user'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'daria-message-content';
            contentDiv.textContent = text;
            
            messageDiv.appendChild(contentDiv);
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function showTyping() {
            const messagesDiv = document.getElementById('dariaMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'daria-message bot';
            typingDiv.id = 'typingIndicator';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'typing-indicator';
            contentDiv.innerHTML = '<span></span><span></span><span></span>';
            
            typingDiv.appendChild(contentDiv);
            messagesDiv.appendChild(typingDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function removeTyping() {
            const typing = document.getElementById('typingIndicator');
            if (typing) typing.remove();
        }
        
        function sendMessage(message) {
            if (!message || message.trim() === '') return;
            
            const input = document.getElementById('dariaInput');
            input.value = '';
            
            addMessage(message, false);
            showTyping();
            
            fetch('/daria/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message, context: conversationContext})
            })
            .then(response => response.json())
            .then(data => {
                removeTyping();
                addMessage(data.response);
                conversationContext = data.context;
                
                if (data.offer) {
                    showOffer(data.offer);
                }
            });
        }
        
        function showOffer(offer) {
            const messagesDiv = document.getElementById('dariaMessages');
            const offerDiv = document.createElement('div');
            offerDiv.className = 'daria-message bot';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'offer-box';
            contentDiv.innerHTML = `
                <div style="font-size: 20px; margin-bottom: 10px;">🎁 OFERTĂ SPECIALĂ</div>
                <div style="font-size: 24px; font-weight: bold;">${offer.discount}% REDUCERE</div>
                <div style="margin: 10px 0;">Pentru ${offer.service}</div>
                <button onclick="scheduleMeeting()" style="background: white; color: #667eea; border: none; padding: 10px 20px; border-radius: 25px; font-weight: bold; cursor: pointer; margin-top: 10px;">
                    📅 Vreau oferta!
                </button>
            `;
            
            offerDiv.appendChild(contentDiv);
            messagesDiv.appendChild(offerDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function scheduleMeeting() {
            addMessage('Perfect! Te rog să-mi lași numărul de telefon și o să te sunăm în 30 de minute pentru a discuta oferta. Sau poți completa formularul de contact de pe site. 🤗', false);
        }
    </script>
</body>
</html>
"""

# ============================================
# API DARIA - LOGICA DE CONVERSAȚIE
# ============================================

@app.route('/daria')
def daria_widget():
    return render_template_string(CHAT_WIDGET)

@app.route('/daria/chat', methods=['POST'])
def daria_chat():
    data = request.json
    user_message = data.get('message', '').lower()
    context = data.get('context', {'step': 'initial'})
    
    response = ""
    new_context = context.copy()
    
    # Oferte random (10-30%)
    discount = random.randint(10, 30)
    
    # Logica de conversație
    if any(word in user_message for word in ['bună', 'salut', 'hey', 'hello']):
        response = "Bună! Eu sunt Daria, secretara virtuală. Cu ce serviciu pot să te ajut?"
        new_context['step'] = 'greeting'
    
    elif any(word in user_message for word in ['servicii', 'ce faceți', 'ce oferiți']):
        response = """Avem o gamă variată de servicii:
🔹 **Site-uri Web** - Prezentare (€499), Magazine online (€1999), Site-uri piese auto (€999)
🔹 **Aplicații Mobile** - iOS, Android, Hibride (€499 - €9800)
🔹 **Marketing Digital** - SEO, Branding, Social Media

Ce anume te interesează?"""
    
    elif any(word in user_message for word in ['site auto', 'piese auto']):
        response = """Pentru site-uri piese auto avem:
🚗 **STAR WEBSITE** - €999
   • Catalog de bază
   • Căutare după titlu
   • 3 luni hosting gratuit

🚗 **PREMIUM WEBSITE** - €2100
   • Căutare după VIN
   • Catalog avansat
   • 6 luni hosting gratuit

🚗 **BEST WEBSITE** - €7900
   • API cu furnizori
   • Aplicație Android inclusă
   • Integrare AI

Vrei mai multe detalii despre vreunul?"""
    
    elif any(word in user_message for word in ['magazin online', 'e-commerce']):
        response = """Pentru magazine online avem:
🛒 **STARTER SHOP** - €550
   • 20 produse
   • Plată online
   • Design profesional

🛒 **PROFESSIONAL STORE** - €1999
   • 100 produse
   • Integrare curier
   • GDPR, Chat WhatsApp

🛒 **PREMIUM SHOP** - €2800
   • Până la 1000 produse
   • Module extra
   • Suport prioritar"""
    
    elif any(word in user_message for word in ['aplicații', 'app', 'mobile']):
        response = """Dezvoltăm aplicații mobile:
📱 **APLICAȚIE START** - €499
   • iOS sau Android
   • 3 ecrane principale
   • Notificări push

📱 **APLICAȚIE PROFESIONALĂ** - €3950
   • iOS + Android
   • Catalog produse
   • Sistem fidelizare

📱 **APLICAȚIE EXCLUSIVĂ** - €9800
   • Cross-platform
   • Inteligență Artificială
   • Self-service"""
    
    elif any(word in user_message for word in ['seo', 'optimizare']):
        response = """Optimizare SEO:
📊 **Analiză SEO** - Gratuită
   • Raport complet
   • Sugestii de optimizare

📊 **Pachet SEO START** - €350
   • Optimizare on-page
   • 10 cuvinte cheie
   • Raport lunar"""
    
    elif any(word in user_message for word in ['preț', 'pret', 'cost', 'cât']):
        response = "Pentru ce serviciu dorești prețul? Pot să-ți dau detalii despre site-uri, aplicații sau pachete SEO."
    
    elif any(word in user_message for word in ['contact', 'telefon', 'email']):
        response = """Ne poți contacta:
📞 Telefon: +40 721 234 567
📧 Email: office@hakunadesign.ro
📍 Adresă: Strada Alexandru Ioan Cuza nr. 45, Sector 1, București"""
    
    elif any(word in user_message for word in ['ofertă', 'reducere', 'specială']):
        service = random.choice(['site-uri auto', 'magazine online', 'aplicații mobile'])
        response = f"🎁 Îți pot oferi o reducere specială de {discount}% pentru {service} dacă începem săptămâna asta! Te interesează?"
        new_context['last_offer'] = {'service': service, 'discount': discount}
    
    elif any(word in user_message for word in ['da', da']):
        if context.get('last_offer'):
            response = f"Perfect! Ți-am aplicat reducerea de {context['last_offer']['discount']}%. Vrei să programăm o discuție pentru a stabili detaliile?"
        else:
            response = "Super! Ce anume ți-ar plăcea să discutăm?"
    
    elif any(word in user_message for word in ['program', 'discuție', 'întâlnire']):
        response = "Cu plăcere! Te așteptăm mâine la ora 10:00 pentru o cafea virtuală. Îți voi trimite un email cu link-ul de meet. ☕️"
    
    else:
        response = "Nu sunt sigură că am înțeles. Poți fi mai specific? Mă poți întreba despre servicii, prețuri, sau poți cere o ofertă personalizată."
    
    return jsonify({
        'response': response,
        'context': new_context,
        'offer': new_context.get('last_offer')
    })

@app.route('/daria/health')
def health():
    return jsonify({'status': 'healthy', 'name': 'Daria'})

@app.route('/')
def home():
    return "Daria - Secretara Virtuală este online! Accesează /daria pentru widget."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
