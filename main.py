from flask import Flask, render_template_string, request
import subprocess
import os

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Automation</title>
    <style>
        body { font-family: Arial; background: #121212; color: white; text-align: center; padding: 20px; }
        input, button, textarea { padding: 10px; margin: 10px; border-radius: 6px; width: 80%; }
        .box { background: #1e1e1e; padding: 20px; border-radius: 10px; margin: auto; max-width: 600px; }
    </style>
</head>
<body>
    <h1>📱 WhatsApp Automation (Baileys)</h1>
    <div class="box">
        <form action="/pair" method="post">
            <input type="text" name="number" placeholder="Enter WhatsApp Number" required>
            <button type="submit">Generate QR</button>
        </form>

        <form action="/send" method="post" enctype="multipart/form-data">
            <input type="text" name="number" placeholder="Your WhatsApp Number (same as QR)" required>
            <input type="text" name="target" placeholder="Target Number with country code" required>
            <input type="text" name="delay" placeholder="Delay in seconds" required>
            <input type="file" name="message_file" required>
            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/pair', methods=['POST'])
def pair():
    number = request.form['number']
    auth_path = f'auth/{number}'

    os.makedirs(auth_path, exist_ok=True)

    # Pairing using sender.js
    subprocess.Popen(['node', 'sender.js', 'pair', number])
    return f"<h2 style='color:lime'>QR code generated for {number}. Check terminal to scan it.</h2>"

@app.route('/send', methods=['POST'])
def send():
    number = request.form['number']
    target = request.form['target']
    delay = request.form['delay']
    message_file = request.files['message_file']
    
    message_path = f"messages.txt"
    message_file.save(message_path)

    subprocess.Popen(['node', 'sender.js', 'send', number, target, delay, message_path])
    return f"<h2 style='color:lime'>Message sending started from {number} to {target}</h2>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
  
