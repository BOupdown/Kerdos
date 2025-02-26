<template>
    <div class="search-container">
      <div class="search-box">
        <input
          v-model="query"
          type="text"
          class="search-input"
          placeholder="Entrez votre recherche..."
        />
        <button @click="search" class="search-button">Rechercher</button>
      </div>
  
      <!-- Spinner (boussole) pendant la recherche -->
      <div v-if="loading" class="spinner-container">
        <div class="spinner"></div>
      </div>
  
      <div v-if="results.length > 0" class="results">
        <ul>
          <li
            v-for="(result, index) in displayedResults"
            :key="result.codeK"
            class="result-item"
          >
            <span class="document-content">{{ result.content.document }}</span>
            <span class="document-code">{{ result.content.codeK }}</span>
          </li>
        </ul>
      </div>
    </div>
  </template>
    
    <script>
    export default {
      data() {
        return {
          query: "",
          results: [],
          displayedResults: [], // Liste des résultats affichés progressivement
          loading: false, // pour indiquer si la recherche est en cours
        };
      },
      methods: {
        async search() {
          if (this.query.trim()) {
            this.loading = true; // Commence la recherche
            try {
              const response = await fetch("http://localhost:5000/search", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({ query: this.query }),
              });
    
              if (response.ok) {
                this.results = await response.json();
                this.displayResultsGradually();
              } else {
                console.error("Erreur lors de la recherche");
              }
            } catch (error) {
              console.error("Erreur de connexion:", error);
            } finally {
              this.loading = false; // Fin de la recherche
            }
          }
        },
    
        displayResultsGradually() {
          this.displayedResults = [];
          this.results.forEach((result, index) => {
            setTimeout(() => {
              this.displayedResults.push(result);
            }, index * 200); // Délai de 200ms entre chaque ajout
          });
        },
      },
    };
    </script>
      
  <style scoped>
  .search-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
  }
  
  .title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 20px;
  }
  
  .search-box {
    display: flex;
    width: 100%;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .search-input {
    flex: 1;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    font-size: 16px;
    width: 700px;
  }
  
  .search-button {
    padding: 10px 20px;
    border-radius: 5px;
    background-color: #108c14;
    color: white;
    border: none;
    font-size: 16px;
    cursor: pointer;
  }
  
  .search-button:hover {
    background-color: #020227;
  }
  
  /* Spinner (boussole ou icône tournante) */
  .spinner-container {
    margin: 20px;
  }
  
  .spinner {
    border: 8px solid #f3f3f3; /* couleur de fond */
    border-top: 8px solid #108c14; /* couleur de la barre tournante */
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1.5s linear infinite; /* animation pour faire tourner */
  }
  
  /* Animation de rotation */
  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  
  .results {
    width: 100%;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 5px;
    border: 1px solid #ccc;
  }
  
  .result-item {
    padding: 8px 0;
    border-bottom: 1px solid #ddd;
  }
  
  .result-item:last-child {
    border-bottom: none;
  }
  
  .document-content {
    color: #504646;
    font-weight: bold;
    margin-right: 10px;
  }
  
  .document-code {
    color: #888;
  }
  </style>