<template>
  <div class="chatbot-container">
    <div class="chat-window">
      <div v-for="(message, index) in messages" :key="index" :class="message.sender">
        <div class="message">
          {{ message.text }}
        </div>
      </div>
    </div>
    <div class="input-area">
      <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Posez votre question..." />
      <button @click="sendMessage">Envoyer</button>
      <button @click="toggleMode">{{ mode === 'chatbot' ? '🌐' : '🤖' }}</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      userInput: '',
      messages: [],
      mode: 'chatbot' // 'chatbot' ou 'internet'
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '') return;

      // Ajouter le message de l'utilisateur
      this.messages.push({ sender: 'user', text: this.userInput });

      // Choisir la méthode en fonction du mode
      if (this.mode === 'chatbot') {
        await this.sendToChatbot();
      } else {
        await this.sendToInternet();
      }

      // Effacer l'entrée utilisateur
      this.userInput = '';
    },

    async sendToChatbot() {
      try {
        const response = await fetch('http://localhost:7000/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: this.userInput }),
        });

        const data = await response.json();
        this.messages.push({ sender: 'bot', text: data.answer });
      } catch (error) {
        console.error('Erreur lors de la communication avec l\'API:', error);
        this.messages.push({ sender: 'bot', text: 'Désolé, une erreur s\'est produite.' });
      }
    },

    async sendToInternet() {
      try {
        const response = await fetch('http://localhost:7000/ask2', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: this.userInput }),
        });

        const data = await response.json();
        this.messages.push({ sender: 'bot', text: data.answer });
      } catch (error) {
        console.error('Erreur lors de la communication avec l\'API:', error);
        this.messages.push({ sender: 'bot', text: 'Désolé, une erreur s\'est produite.' });
      }
    },

    toggleMode() {
      this.mode = this.mode === 'chatbot' ? 'internet' : 'chatbot';
      this.messages.push({ sender: 'system', text: `Mode changé en : ${this.mode}` });
    }
  }
};
</script>

<style scoped>

.chatbot-container {
  flex-direction: column;
  height: 100%;
  width: 1000px;
  border-radius: 10px;
  overflow: hidden;
}

.chat-window {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f9f9f9;
  height: 500px;
  /* Personnalisation de la barre de défilement */
  scrollbar-width: thin; /* Pour Firefox */
  scrollbar-color: #007bff #f1f1f1; /* Pour Firefox */
}

/* Pour les navigateurs WebKit (Chrome, Safari, etc.) */
.chat-window::-webkit-scrollbar {
  width: 8px; /* Largeur de la barre de défilement */
}

.chat-window::-webkit-scrollbar-track {
  background: #f1f1f1; /* Couleur de la piste de la barre de défilement */
  border-radius: 10px;
}

.chat-window::-webkit-scrollbar-thumb {
  background: #8a8a8a; /* Couleur du curseur de la barre de défilement */
  border-radius: 10px;
}

.chat-window::-webkit-scrollbar-thumb:hover {
  background: #575757; /* Couleur du curseur au survol */
}
.message {
  padding: 10px;
  margin: 5px;
  border-radius: 10px;
  max-width: 70%;
}

.user {
  display: flex;
  justify-content: flex-end;
}

.user .message {
  background-color: #007bff;
  color: white;
}

.bot {
  display: flex;
  justify-content: flex-start;
}

.bot .message {
  background-color: #e9ecef;
  color: black;
}

.system {
  display: flex;
  justify-content: center;
}

.system .message {
  background-color: #ffcc00;
  color: black;
}

.input-area {
  display: flex;
  padding: 10px;
  background-color: #fff;
  border-top: 1px solid #ccc;
}

.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

.input-area button {
  padding: 10px 20px;
  background-color: #00a824;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 10px;
}

.input-area button:hover {
  background-color: #0056b3;
}
</style>