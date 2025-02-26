<template>
    <div class="chat-box" aria-live="polite">
      <div class="messages">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
          {{ message.text }}
        </div>
      </div>
      <div class="input-box">
        <input v-model="question" @keyup.enter="sendMessage" placeholder="Posez une question..." />
        <button @click="sendMessage">Envoyer</button>
      </div>
    </div>
  </template>
    
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        question: '',
        messages: []
      };
    },
    methods: {
      async sendMessage() {
        if (this.question.trim() === '') return;
  
        const userMessage = { text: this.question, sender: 'user' };
        this.messages.push(userMessage);
  
        try {
          const response = await axios.post('http://localhost:7000/ask', { question: this.question });
          const botMessage = { text: response.data.answer, sender: 'bot' };
          this.messages.push(botMessage);
        } catch (error) {
          console.error('Erreur lors de la requête :', error);
          const errorMessage = { text: 'Désolé, il y a eu un problème avec le serveur.', sender: 'bot' };
          this.messages.push(errorMessage);
        }
  
        this.question = '';
        this.$nextTick(() => {
          const chatBox = document.querySelector('.chat-box');
          chatBox.scrollTop = chatBox.scrollHeight;  // Défilement automatique vers le bas
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .chat-box {
    display: flex;
    flex-direction: column;
    height: 100vh; /* Prend toute la hauteur de la fenêtre */
  }
  
  .messages {
    flex-grow: 1; /* Prend tout l'espace disponible */
    overflow-y: auto; /* Permet le défilement vertical */
    padding: 10px;
    box-sizing: border-box;
  }
  
  .message {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
    background-color: #f1f1f1;
  }
  
  .input-box {
    position: sticky;
    bottom: 200px;
    padding: 10px;
    box-sizing: border-box;
    display: flex;
    align-items: center;
  }
  
  .input-box input {
    flex-grow: 1;
    padding: 10px;
    border-radius: 20px;
    border: 1px solid #ccc;
    margin-right: 10px;
  }
  
  .input-box button {
    padding: 10px 20px;
    border-radius: 20px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }
  </style>
    