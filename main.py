from flask import Flask, request, render_template_string, jsonify
import random

app = Flask(__name__)

# Pagina principală - aici începe magia
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secretara Virtuală - Web Design</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            width: 400px;
            max-width: 90%;
            padding: 20px;
        }
        .chat-header {
            text-align: center;
            color: #667eea;
            margin-bottom: 20px;
        }
        .chat-box {
            height: 300px;
            overflow-y: auto;
            border: 1px solid #eee;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 10px;
        }
        .bot-message {
            background: #f0f0f0;
            margin-right: 20%;
        }
        .user-message {
            background: #667eea;
            color: white;
            margin-left: 20%;
            text-align: right;
        }
        .options {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .option-btn {
            background: #f0f0f0;
            border: none;
            padding: 12px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }
        .option-btn:hover {
            background: #667eea;
            color: white;
        }
        .discount {
            background: #ff6b6b;
            color: white;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h2>🤖 Secretara Virtuală</h2>
            <p>Web Design & Dezvoltare</p>
        </div>
        <div class="chat-box" id="chatBox">
            <div class="message bot-message">
                Bună! Eu sunt secretara virtuală. Cu ce te pot ajuta azi?
            </div>
        </div>
        <div class="options" id="options">
            <button class="option-btn" onclick="sendMessage('site-prezentare')">
                📄 Vreau un site de prezentare
            </button>
            <button class="option-btn" onclick="sendMessage('magazin-online')">
                🛒 Vreau un magazin online
            </button>
            <button class="option-btn" onclick="sendMessage('redesign')">
                🔄 Vreau să refac site-ul existent
            </button>
            <button class="option-btn" onclick="sendMessage('preturi')">
                💰 Vreau să văd prețurile
            </button>
        </div>
    </div>

    <script>
        let currentStep = 'initial';
        let userNeeds = '';
        let discount = 0;
        
        function addMessage(text, isBot = true) {
            const chatBox = document.getElementById('chatBox');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
            messageDiv.textContent = text;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        function sendMessage(option) {
            let response = '';
            
            if (option === 'site-prezentare') {
                response = 'Excelentă alegere! Un site de prezentare e perfect pentru imaginea afacerii tale. Prețul standard pornește de la 1500 lei.';
                userNeeds = 'prezentare';
            } else if (option === 'magazin-online') {
                response = 'Super! Un magazin online îți poate crește vânzările semnificativ. Prețul pornește de la 3000 lei.';
                userNeeds = 'magazin';
            } else if (option === 'redesign') {
                response = 'Perfect! Un redesign poate aduce un plus de profesionalism. Prețul pornește de la 1200 lei.';
                userNeeds = 'redesign';
            } else if (option === 'preturi') {
                showPrices();
                return;
            }
            
            addMessage(response, false);
            setTimeout(() => askForMeeting(), 1000);
        }
        
        function askForMeeting() {
            addMessage('Ți-a plăcut oferta? 🎁 Dacă începem săptămâna asta, îți pot oferi o REDUCERE SPECIALĂ! Vrei să programăm o discuție gratuită?');
            
            const optionsDiv = document.getElementById('options');
            optionsDiv.innerHTML = `
                <button class="option-btn" onclick="offerDiscount()">DA, vreau reducerea! 🎉</button>
                <button class="option-btn" onclick="noThanks()">Poate mai târziu</button>
            `;
        }
        
        function offerDiscount() {
            discount = randomDiscount();
            addMessage(`FELICITĂRI! 🎊 Ți-am aplicat o reducere de ${discount}%!`, false);
            
            const optionsDiv = document.getElementById('options');
            optionsDiv.innerHTML = `
                <div class="discount">
                    🎁 REDUCERE ${discount}% APLICATĂ!
                </div>
                <button class="option-btn" onclick="scheduleMeeting()" style="background: #4CAF50; color: white;">
                    📅 Programează discuția GRATUITĂ acum
                </button>
                <button class="option-btn" onclick="resetChat()">
                    Înapoi la început
                </button>
            `;
        }
        
        function scheduleMeeting() {
            addMessage('Perfect! Te aștept mâine la ora 10:00 pentru o cafea virtuală ☕️. Îți voi trimite un email cu detaliile. Mulțumesc! ❤️', false);
            document.getElementById('options').innerHTML = `
                <button class="option-btn" onclick="resetChat()">
                    Începe o nouă conversație
                </button>
            `;
        }
        
        function noThanks() {
            addMessage('Nicio problemă! Oricând ai nevoie de ajutor, sunt aici. Poți vedea portofoliul nostru aici: [link]', false);
        }
        
        function showPrices() {
            addMessage('📊 PREȚURI SPECIALE:', false);
            addMessage('• Site Prezentare: 1500 lei\n• Magazin Online: 3000 lei\n• Redesign: 1200 lei\nToate includ consultanță gratuită!', false);
            setTimeout(() => askForMeeting(), 2000);
        }
        
        function randomDiscount() {
            return Math.floor(Math.random() * 20) + 10; // 10-30% reducere
        }
        
        function resetChat() {
            location.reload();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.json
    user_message = data.get('message', '')
    
    # Aici o să adăugăm mai târzeu inteligență AI
    return jsonify({"response": "Am primit mesajul tău!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
