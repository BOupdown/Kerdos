from flask import Flask
from apiCalculs import calculs_bp
from apiChatBot import chatbot_bp
from apiRecherche import recherche_bp

app = Flask(__name__)
app.register_blueprint(calculs_bp, url_prefix="/calculs")
app.register_blueprint(chatbot_bp, url_prefix="/chatbot")
app.register_blueprint(recherche_bp, url_prefix="/recherche")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
