from flask import Flask, request, jsonify, render_template_string, redirect
from flask_cors import CORS
import random
import json
import re
import time

app = Flask(__name__)
CORS(app)

# ============================================
# BAZA DE DATE COMPLETĂ - CU TOATE SERVICIILE
# ============================================

SERVICES = {
    "site_prezentare": {
        "id": "site_prezentare",
        "name": "Site Prezentare",
        "price": "€499",
        "url": "/dezvoltare-site-prezentare",
        "keywords": ["prezentare", "site simplu", "site firma", "site company", "site de prezentare", "prezentare firma", "site business", "site corporativ"],
        "features": ["Design responsive premium", "6 pagini personalizate + contact", "Formular inteligent", "Integrare social media", "Optimizat SEO", "Viteză super-rapidă"],
        "description": "Perfect pentru firme care vor să aibă prezență online profesională."
    },
    "magazin_online": {
        "id": "magazin_online",
        "name": "Magazin Online Profesional",
        "price": "€1999",
        "url": "/magazin-online",
        "keywords": ["magazin", "e-commerce", "shop", "vanzari", "vânzări", "comert", "comerț", "produse", "cos cumparaturi", "coș cumpărături", "cumpărături"],
        "features": ["Temă premium profesională", "Până la 1000 produse", "Plată online integrată", "Integrare curier (FanCourier, Cargus)", "GDPR complet", "Chat WhatsApp live", "Admin dashboard", "Rapoarte vânzări"],
        "description": "Soluție completă pentru afaceri care vor să vândă online."
    },
    "site_auto": {
        "id": "site_auto",
        "name": "Site Piese Auto",
        "price": "€999 - €7900",
        "url": "/site-auto",
        "keywords": ["auto", "piese auto", "masina", "mașină", "catalog piese", "tecdoc", "vin", "car parts", "auto parts", "piese", "autoturisme"],
        "features": ["Catalog piese auto complet", "Căutare inteligentă după VIN", "Căutare după marcă/model", "Import piese din Excel/XML", "Compatibilitate TecDoc", "Gestionare stoc", "Prețuri automate"],
        "description": "Specializare în domeniul auto - cea mai căutată soluție."
    },
    "aplicatii_ios": {
        "id": "aplicatii_ios",
        "name": "Aplicații iOS",
        "price": "€499 - €9800",
        "url": "/aplicatii-ios",
        "keywords": ["ios", "iphone", "ipad", "apple", "swift", "aplicație ios", "app ios", "aplicatie iphone"],
        "features": ["Swift/SwiftUI nativ", "Design Apple HIG", "Publicare App Store", "Notificări push", "Integrare iCloud", "Performanță maximă"],
        "description": "Aplicații native pentru ecosistemul Apple."
    },
    "aplicatii_android": {
        "id": "aplicatii_android",
        "name": "Aplicații Android",
        "price": "€499 - €9800",
        "url": "/aplicatii-android",
        "keywords": ["android", "google", "kotlin", "aplicație android", "app android", "play store", "aplicatie google"],
        "features": ["Kotlin modern", "Material You", "Publicare Google Play", "Notificări push", "Integrare servicii Google", "Optimizare baterie"],
        "description": "Aplicații native pentru miliardele de utilizatori Android."
    },
    "aplicatii_hibrid": {
        "id": "aplicatii_hibrid",
        "name": "Aplicații Hibride",
        "price": "€499 - €9800",
        "url": "/aplicatii-hibrid",
        "keywords": ["hibrid", "cross platform", "flutter", "react native", "ios si android", "o singură aplicație"],
        "features": ["Flutter/React Native", "O singură bază de cod", "iOS + Android simultan", "Cost redus", "Dezvoltare rapidă", "Aspect nativ"],
        "description": "O singură aplicație pentru ambele platforme."
    },
    "seo": {
        "id": "seo",
        "name": "Optimizare SEO",
        "price": "€350/lună",
        "url": "/servicii-seo",
        "keywords": ["seo", "optimizare", "google", "cautare", "căutare", "promovare", "motor cautare", "primele rezultate"],
        "features": ["Analiză site completă", "Optimizare cuvinte cheie", "Rapoarte lunare detaliate", "Link building", "Monitorizare poziții", "Consultanță continuă"],
        "description": "Apari primul în Google și atrage clienți."
    },
    "branding": {
        "id": "branding",
        "name": "Branding",
        "price": "Personalizat",
        "url": "/branding",
        "keywords": ["branding", "logo", "identitate vizuala", "identitate vizuală", "design logo", "marca", "nume", "identitate"],
        "features": ["Logo profesional", "Identitate vizuală completă", "Ghid de brand", "Staționărie", "Prezentare PowerPoint", "Elemente de marketing"],
        "description": "Creează o identitate puternică pentru afacerea ta."
    },
    "social_media": {
        "id": "social_media",
        "name": "Social Media",
        "price": "Personalizat",
        "url": "/social-media",
        "keywords": ["social media", "facebook", "instagram", "tiktok", "postari", "postări", "reclame", "promovare social"],
        "features": ["Management conturi", "Creare conținut", "Campanii plătite", "Calendar editorial", "Rapoarte performanță", "Interacțiune cu clienții"],
        "description": "Crește-ți prezența pe rețelele sociale."
    }
}

# ============================================
# FUNCȚIE DE ÎNȚELEGERE AVANSATĂ
# ============================================

def detecteaza_intentia(message):
    """Detectează exact ce caută utilizatorul"""
    msg = message.lower().strip()
    
    # Listă de intenții și cuvinte cheie
    intents = {
        "salut": ["buna", "salut", "hey", "hello", "bună", "buna ziua", "bună ziua", "bună dimineața", "buna dimineata"],
        "site_prezentare": ["prezentare", "site simplu", "site firma", "site company", "site de prezentare"],
        "magazin_online": ["magazin", "e-commerce", "shop", "vanzari", "vânzări", "comert", "comerț", "produse", "cos cumparaturi"],
        "site_auto": ["auto", "piese auto", "masina", "mașină", "catalog piese", "tecdoc", "vin", "piese"],
        "aplicatii_ios": ["ios", "iphone", "ipad", "apple", "swift", "aplicație ios"],
        "aplicatii_android": ["android", "google", "kotlin", "aplicație android"],
        "aplicatii_hibrid": ["hibrid", "cross platform", "flutter", "react native"],
        "seo": ["seo", "optimizare", "google", "cautare", "promovare"],
        "branding": ["branding", "logo", "identitate vizuala"],
        "social_media": ["social media", "facebook", "instagram", "tiktok"],
        "preturi": ["pret", "preț", "cost", "cat costa", "cât costă", "tarif", "euro", "€"],
        "contact": ["contact", "telefon", "email", "adresa", "adresă", "sediu", "locatie", "locație", "program"],
        "oferta": ["oferta", "ofertă", "reducere", "speciala", "specială", "promo", "discount"],
        "programare": ["programare", "discutie", "discuție", "intalnire", "întâlnire", "meet", "cafea", "consultatii", "consultații"]
    }
    
    for intent, keywords in intents.items():
        if any(keyword in msg for keyword in keywords):
            return intent
    
    return "neclar"

# ============================================
# INTERFAȚA DARIA - ELEGANTĂ ȘI PROFESIONALĂ
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
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .daria-chat-widget {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 999999;
        }
        
        /* BUTON PRINCIPAL ELEGANT */
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
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            animation: pulse 2s infinite;
        }
        
        .daria-chat-button:hover {
            transform: scale(1.1) rotate(5deg);
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); }
            50% { box-shadow: 0 15px 50px rgba(102, 126, 234, 0.7); }
            100% { box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4); }
        }
        
        /* FEREASTRĂ CHAT ELEGANTĂ */
        .daria-chat-box {
            position: absolute;
            bottom: 90px;
            right: 0;
            width: 450px;
            height: 650px;
            background: white;
            border-radius: 30px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.15);
            display: none;
            flex-direction: column;
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .daria-chat-box.open {
            display: flex;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* HEADER ELEGANT */
        .daria-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px 20px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .daria-avatar {
            width: 50px;
            height: 50px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            backdrop-filter: blur(10px);
        }
        
        .daria-header-info {
            flex: 1;
        }
        
        .daria-header-info h3 {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 4px;
        }
        
        .daria-header-info p {
            font-size: 13px;
            opacity: 0.9;
        }
        
        .daria-header button {
            background: rgba(255, 255, 255, 0.2);
            border: none;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
            transition: background 0.3s;
        }
        
        .daria-header button:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        /* ZONA MESAJE */
        .daria-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8faff;
        }
        
        .daria-message {
            margin-bottom: 20px;
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
            padding: 15px 20px;
            border-radius: 25px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-line;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .bot .daria-message-content {
            background: white;
            color: #1a1f36;
            border-bottom-left-radius: 5px;
            border-left: 3px solid #667eea;
        }
        
        .user .daria-message-content {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border-bottom-right-radius: 5px;
        }
        
        /* ZONA SUGESTII */
        .daria-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding: 15px 20px;
            background: white;
            border-top: 1px solid #edf2f7;
        }
        
        .daria-suggestion {
            background: #f0f4ff;
            border: none;
            padding: 10px 16px;
            border-radius: 30px;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s;
            color: #4a5568;
            border: 1px solid transparent;
        }
        
        .daria-suggestion:hover {
            background: #667eea;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        }
        
        /* ZONA INPUT */
        .daria-input-area {
            padding: 20px;
            background: white;
            border-top: 1px solid #edf2f7;
            display: flex;
            gap: 10px;
        }
        
        .daria-input-area input {
            flex: 1;
            padding: 15px 20px;
            border: 2px solid #e2e8f0;
            border-radius: 30px;
            outline: none;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .daria-input-area input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .daria-input-area button {
            width: 55px;
            height: 55px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .daria-input-area button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* TYPING INDICATOR */
        .typing-indicator {
            display: flex;
            gap: 6px;
            padding: 15px 20px;
            background: white;
            border-radius: 25px;
            width: fit-content;
            border-left: 3px solid #667eea;
        }
        
        .typing-indicator span {
            width: 10px;
            height: 10px;
            background: #667eea;
            border-radius: 50%;
            animation: typing 1.4s infinite;
            opacity: 0.5;
        }
        
        .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
        .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
            30% { transform: translateY(-10px); opacity: 1; }
        }
        
        /* OFERTĂ ELEGANTĂ */
        .offer-box {
            background: linear-gradient(145deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 20px;
            margin: 15px 0;
            text-align: center;
            animation: gentlePulse 3s infinite;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        @keyframes gentlePulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        
        .offer-box h4 {
            font-size: 18px;
            margin-bottom: 10px;
        }
        
        .offer-box .discount {
            font-size: 36px;
            font-weight: 700;
            margin: 10px 0;
        }
        
        .offer-btn {
            background: white;
            color: #667eea;
            border: none;
            padding: 12px 24px;
            border-radius: 30px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 15px;
            transition: all 0.3s;
            font-size: 14px;
        }
        
        .offer-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(255, 255, 255, 0.2);
        }
        
        /* CONTACT BUTOANE */
        .contact-buttons {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        .contact-btn {
            flex: 1;
            padding: 12px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .whatsapp-btn {
            background: #25D366;
            color: white;
        }
        
        .email-btn {
            background: #667eea;
            color: white;
        }
        
        .contact-btn:hover {
            transform: translateY(-2px);
            filter: brightness(1.1);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        /* TIMER NOTIFICARE */
        .typing-timer {
            position: absolute;
            bottom: 90px;
            right: 20px;
            background: white;
            padding: 10px 20px;
            border-radius: 30px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            font-size: 13px;
            color: #667eea;
            display: none;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="daria-chat-widget">
        <button class="daria-chat-button" onclick="toggleChat()">
            💬
        </button>
        
        <div class="typing-timer" id="typingTimer">
            👋 Mai ești acolo? Te putem ajuta cu ceva?
        </div>
        
        <div class="daria-chat-box" id="dariaChatBox">
            <div class="daria-header">
                <div class="daria-avatar">
                    🤖
                </div>
                <div class="daria-header-info">
                    <h3>Daria - Asistent Virtual</h3>
                    <p>🟢 Online acum | Răspuns instant</p>
                </div>
                <button onclick="toggleChat()">×</button>
            </div>
            
            <div class="daria-messages" id="dariaMessages">
                <div class="daria-message bot">
                    <div class="daria-message-content">
                        👋 Bună! Eu sunt Daria, asistentul tău virtual.

                        Cu ce te pot ajuta azi? Poți alege una dintre opțiuni sau scrie direct ce cauți:

                        • Site-uri web (prezentare, magazine, piese auto)
                        • Aplicații mobile (iOS, Android)
                        • SEO, branding, social media
                        • Prețuri și oferte
                        • Sau cere o ofertă personalizată!
                    </div>
                </div>
            </div>
            
            <div class="daria-suggestions" id="dariaSuggestions">
                <button class="daria-suggestion" onclick="sendMessage('site web')">🌐 Site web</button>
                <button class="daria-suggestion" onclick="sendMessage('magazin online')">🛒 Magazin online</button>
                <button class="daria-suggestion" onclick="sendMessage('piese auto')">🚗 Site auto</button>
                <button class="daria-suggestion" onclick="sendMessage('aplicație mobilă')">📱 Aplicație</button>
                <button class="daria-suggestion" onclick="sendMessage('prețuri')">💰 Prețuri</button>
                <button class="daria-suggestion" onclick="sendMessage('ofertă')">🎁 Ofertă specială</button>
            </div>
            
            <div class="daria-input-area">
                <input type="text" id="dariaInput" placeholder="Scrie mesajul tău aici..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">
                    ➤
                </button>
            </div>
        </div>
    </div>

    <script>
        let conversationContext = {
            step: 'initial',
            lastIntent: null,
            lastOffer: null,
            waitingForResponse: false,
            inactivityTimer: null,
            responseTimer: null,
            lastMessageTime: Date.now()
        };
        
        const WHATSAPP_NUMBER = '0730176058';
        const CONTACT_EMAIL = 'contact@hakunadesign.ro';
        
        function toggleChat() {
            const box = document.getElementById('dariaChatBox');
            box.classList.toggle('open');
            
            if (box.classList.contains('open')) {
                clearInactivityTimer();
                document.getElementById('typingTimer').style.display = 'none';
            } else {
                startInactivityTimer();
            }
        }
        
        function startInactivityTimer() {
            clearInactivityTimer();
            conversationContext.inactivityTimer = setTimeout(() => {
                if (!document.getElementById('dariaChatBox').classList.contains('open')) {
                    const timer = document.getElementById('typingTimer');
                    timer.style.display = 'block';
                    
                    setTimeout(() => {
                        timer.style.display = 'none';
                    }, 5000);
                }
            }, 10000);
        }
        
        function clearInactivityTimer() {
            if (conversationContext.inactivityTimer) {
                clearTimeout(conversationContext.inactivityTimer);
                conversationContext.inactivityTimer = null;
            }
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
        
        function startResponseTimer() {
            if (conversationContext.responseTimer) {
                clearTimeout(conversationContext.responseTimer);
            }
            
            conversationContext.responseTimer = setTimeout(() => {
                if (!conversationContext.waitingForResponse) {
                    addMessage("👋 Mai ești acolo? Te pot ajuta cu ceva în continuare?");
                }
            }, 15000);
        }
        
        function sendMessage() {
            const input = document.getElementById('dariaInput');
            const message = input.value.trim();
            
            if (message === '') return;
            
            input.value = '';
            addMessage(message, false);
            showTyping();
            
            conversationContext.waitingForResponse = true;
            conversationContext.lastMessageTime = Date.now();
            
            clearTimeout(conversationContext.responseTimer);
            
            fetch('/daria/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    message: message,
                    context: conversationContext
                })
            })
            .then(response => response.json())
            .then(data => {
                removeTyping();
                addMessage(data.response);
                
                conversationContext = data.context;
                conversationContext.waitingForResponse = false;
                
                if (data.offer) {
                    showOffer(data.offer);
                }
                
                if (data.redirect) {
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 2000);
                }
                
                startResponseTimer();
            })
            .catch(error => {
                removeTyping();
                addMessage('Îmi pare rău, am o problemă tehnică. Te rog să încerci mai târziu.');
                console.error(error);
            });
        }
        
        function showOffer(offer) {
            const messagesDiv = document.getElementById('dariaMessages');
            const offerDiv = document.createElement('div');
            offerDiv.className = 'daria-message bot';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'offer-box';
            contentDiv.innerHTML = `
                <h4>🎁 OFERTĂ SPECIALĂ</h4>
                <div class="discount">${offer.discount}% REDUCERE</div>
                <p>Pentru ${offer.service}</p>
                <button class="offer-btn" onclick="showContactOptions()">
                    📞 Vreau această ofertă
                </button>
            `;
            
            offerDiv.appendChild(contentDiv);
            messagesDiv.appendChild(offerDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function showContactOptions() {
            addMessage(`Perfect! Ne putem întâlni în două moduri:`, false);
            
            const messagesDiv = document.getElementById('dariaMessages');
            const contactDiv = document.createElement('div');
            contactDiv.className = 'daria-message bot';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'daria-message-content';
            contentDiv.innerHTML = `
                <div class="contact-buttons">
                    <button class="contact-btn whatsapp-btn" onclick="openWhatsApp()">
                        📱 WhatsApp
                    </button>
                    <button class="contact-btn email-btn" onclick="openEmail()">
                        📧 Email
                    </button>
                </div>
                <p style="margin-top: 10px; font-size: 12px; text-align: center;">
                    Răspundem în maxim 30 de minute!
                </p>
            `;
            
            contactDiv.appendChild(contentDiv);
            messagesDiv.appendChild(contactDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function openWhatsApp() {
            window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=Bună%20Daria!%20Am%20primit%20oferta%20ta%20și%20vreau%20să%20discutăm.`, '_blank');
            addMessage('✅ Te redirecționez către WhatsApp. Așteaptă mesajul nostru!', false);
        }
        
        function openEmail() {
            window.location.href = `mailto:${CONTACT_EMAIL}?subject=Ofertă%20personalizată%20de%20la%20Daria&body=Bună%20Daria!%20Am%20primit%20oferta%20ta%20și%20vreau%20să%20discutăm.`;
            addMessage('✅ Deschid clientul de email. Te așteptăm!', false);
        }
        
        // Inițializare
        startInactivityTimer();
    </script>
</body>
</html>
"""

# ============================================
# API DARIA - INTELIGENȚĂ AVANSATĂ
# ============================================

@app.route('/daria')
def daria_widget():
    return render_template_string(CHAT_WIDGET)

@app.route('/daria/chat', methods=['POST'])
def daria_chat():
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', {'step': 'initial', 'lastIntent': None})
    
    intent = detecteaza_intentia(user_message)
    
    new_context = context.copy()
    new_context['lastIntent'] = intent
    new_context['step'] = 'conversation'
    
    response = ""
    redirect = None
    offer = None
    
    # LOGICĂ PROFESIONALĂ DE CONVERSAȚIE
    if intent == "salut":
        response = """👋 Bună! Mă bucur că ai trecut pe la noi.

Cu ce te pot ajuta astăzi? Poți fi specific:
• "Vreau un site de prezentare pentru firma mea"
• "Caut un magazin online"
• "Am nevoie de un site pentru piese auto"
• "Cât costă o aplicație mobilă?"
• "Vreau o ofertă personalizată"

Sau alege una dintre opțiunile de mai jos!"""
    
    elif intent == "site_prezentare":
        response = """🌐 **Site Prezentare - €499**

Un site profesional pentru afacerea ta include:
✅ Design responsive premium
✅ 6 pagini personalizate
✅ Formular de contact inteligent
✅ Optimizat pentru Google
✅ Viteză super-rapidă
✅ Suport 30 zile

🎁 **Ofertă specială pentru tine:**
Dacă începem săptămâna asta, primești 15% reducere și audit SEO gratuit!

Te interesează?"""
        new_context['lastOffer'] = {'service': 'site de prezentare', 'discount': 15}
        
    elif intent == "magazin_online":
        response = """🛒 **Magazin Online Profesional - €1999**

Soluție completă pentru vânzări online:
✅ Până la 1000 produse
✅ Plată online integrată
✅ Integrare curier (FanCourier, Cargus)
✅ Chat WhatsApp live
✅ Dashboard administrare
✅ GDPR complet
✅ Suport 60 zile

🎁 **Ofertă specială:**
Reducere 20% + instalare gratuită pentru luna aceasta!

Vrei să vezi o demonstrație?"""
        new_context['lastOffer'] = {'service': 'magazin online', 'discount': 20}
        redirect = "/magazin-online"
        
    elif intent == "site_auto":
        response = """🚗 **Site Piese Auto**

Avem 3 pachete specializate:

**1. STAR - €999**
• Catalog piese de bază
• Căutare după titlu
• 3 luni hosting gratuit

**2. PREMIUM - €2100**
• Căutare după VIN
• Catalog avansat
• 6 luni hosting

**3. BEST - €7900**
• API furnizori
• Aplicație Android inclusă
• Inteligență Artificială

Pentru ce tip de afacere auto ai nevoie?"""
        redirect = "/site-auto"
        
    elif intent in ["aplicatii_ios", "aplicatii_android", "aplicatii_hibrid"]:
        response = f"""📱 **{SERVICES[intent]['name']} - {SERVICES[intent]['price']}**

{SERVICES[intent]['description']}

Include:
{chr(10).join(['✅ ' + f for f in SERVICES[intent]['features'][:5]])}

🎁 **Ofertă specială:**
Primești consultanță gratuită și 10% reducere la primul proiect!

Vrei să discutăm detaliile?"""
        new_context['lastOffer'] = {'service': SERVICES[intent]['name'], 'discount': 10}
        
    elif intent == "seo":
        response = """📈 **Optimizare SEO - €350/lună**

Ce primești:
✅ Analiză completă site
✅ Optimizare 10 cuvinte cheie
✅ Raport lunar detaliat
✅ Link building
✅ Monitorizare poziții

🎁 Prima lună cu 25% reducere!"""
        new_context['lastOffer'] = {'service': 'pachet SEO', 'discount': 25}
        
    elif intent == "preturi":
        response = """💰 **PREȚURI SERVICII:**

🌐 **Site-uri:**
• Prezentare: €499
• Magazin online: €1999
• Site auto: €999 - €7900

📱 **Aplicații:**
• Start: €499
• Profesional: €3950
• Exclusiv: €9800

📈 **Marketing:**
• SEO: €350/lună
• Branding: Personalizat
• Social Media: Personalizat

🎁 Toate includ suport și consultanță. Vrei o ofertă personalizată?"""
        
    elif intent == "contact":
        response = f"""📞 **DATE DE CONTACT:**

📱 **WhatsApp:** {WHATSAPP_NUMBER}
📧 **Email:** {CONTACT_EMAIL}
📍 **Adresă:** Str. Alexandru Ioan Cuza nr. 45, Sector 1, București

🕒 **Program:**
Luni - Vineri: 09:00 - 18:00

Alege cum preferi să discutăm mai departe!"""
        
    elif intent == "oferta":
        discount = random.randint(15, 30)
        service = random.choice(['site-uri web', 'magazine online', 'aplicații mobile', 'servicii SEO'])
        response = f"""🎁 **OFERTĂ SPECIALĂ PENTRU TINE!**

Îți pot oferi o reducere de **{discount}%** pentru {service} dacă începem proiectul săptămâna asta!

Ce părere ai? Vrei să discutăm detaliile?"""
        new_context['lastOffer'] = {'service': service, 'discount': discount}
        
    elif intent == "programare":
        response = f"""📅 **PROGRAMEAZĂ O DISCUȚIE**

Alege metoda preferată:
• WhatsApp: {WHATSAPP_NUMBER}
• Email: {CONTACT_EMAIL}
• Sau completează formularul de contact

Te aștept mâine între 10:00 și 17:00 pentru o cafea virtuală! ☕️"""
        
    else:  # intent neclar
        response = """🤔 Hmm, nu sunt sigură că am înțeles exact.

Poți fi mai specific? De exemplu:
• "Vreau un site pentru firma mea"
• "Cât costă un magazin online?"
• "Am nevoie de aplicație mobilă"
• "Vreau o ofertă pentru piese auto"

Sau alege una dintre opțiunile de mai jos și te ajut cu drag!"""
    
    return jsonify({
        'response': response,
        'context': new_context,
        'offer': new_context.get('lastOffer'),
        'redirect': redirect
    })

@app.route('/daria/health')
def health():
    return jsonify({'status': 'healthy', 'name': 'Daria Pro', 'version': '2.0'})

@app.route('/')
def home():
    return "Daria - Asistent Virtual Profesional este online! Accesează <a href='/daria'>/daria</a> pentru widget."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
