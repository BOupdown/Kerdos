<template>
  <div class="container">
    <h1 class="title">Créer une nouvelle formule</h1>
    <form @submit.prevent="addFormule" class="form">
      <label for="formuleName" class="label">Nom de la formule:</label>
      <input type="text" id="formuleName" v-model="formuleName" required class="input common-width">

      <label class="label">Formule:</label>
      <div class="formula-builder common-width">
        <div class="formula-display">{{ formuleFormula || "Cliquez sur les variables ou opérateurs pour construire la formule" }}</div>
        <div class="variables-list">
          <select v-model="selectedVariable" @change="addToFormula(selectedVariable)" class="variable-select common-width">
            <option disabled value="">Sélectionnez une variable</option>
            <option v-for="variable in variables" :key="variable.id" :value="variable.name">
              {{ variable.name }}
            </option>
          </select>
          <button v-for="operator in operators" :key="operator" @click.prevent="addToFormula(operator)" class="operator-button">
            {{ operator }}
          </button>
        </div>
        
      </div>

      <button type="submit" class="button">Ajouter Formule</button>
      <button @click.prevent="resetForm" type="button" class="button reset-button">Réinitialiser</button>
      <div v-if="formuleMessage" :class="{'success': formuleSuccess, 'error': !formuleSuccess}" class="message">
        {{ formuleMessage }}
      </div>
    </form>

    <h1 class="title">Ajouter une nouvelle variable</h1>
    <form @submit.prevent="addVariable" class="form">
      <label for="variableName" class="label">Nom de la variable:</label>
      <input type="text" id="variableName" v-model="variableName" required class="input common-width">
      <div>
        <button type="submit" class="button">Ajouter Variable</button>
      </div>
      <div v-if="variableMessage" :class="{'success': variableSuccess, 'error': !variableSuccess}" class="message">
        {{ variableMessage }}
      </div>
    </form>

    <h2 class="title">Formules enregistrées</h2>
    <ul>
      <li v-for="formule in formules" :key="formule.id" class="common-width">
        <strong>{{ formule.name }}</strong> : <span class="resformule">{{ formule.formula }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formuleName: '',
      formuleFormula: '',
      formuleMessage: '',
      formuleSuccess: false,
      variableName: '',
      variableMessage: '',
      variableSuccess: false,
      variables: [],
      formules: [],
      operators: ['+', '-', '*', '/', '(', ')'],
      selectedVariable: ''
    };
  },
  methods: {
    async addFormule() {
      try {
        await axios.post('http://localhost:3000/formules', {
          name: this.formuleName,
          formula: this.formuleFormula
        });
        this.formuleMessage = 'Formule ajoutée avec succès!';
        this.formuleSuccess = true;
        this.formuleName = '';
        this.formuleFormula = '';
        this.fetchFormules();
      } catch (error) {
        this.formuleMessage = "Erreur lors de l'ajout de la formule.";
        this.formuleSuccess = false;
        console.error('Erreur:', error);
      }
    },
    async addVariable() {
      try {
        await axios.post('http://localhost:3000/variables', {
          name: this.variableName
        });
        this.variableMessage = 'Variable ajoutée avec succès!';
        this.variableSuccess = true;
        this.variableName = '';
        this.fetchVariables();
      } catch (error) {
        this.variableMessage = "Erreur lors de l'ajout de la variable.";
        this.variableSuccess = false;
        console.error('Erreur:', error);
      }
    },
    async fetchVariables() {
      try {
        const response = await axios.get('http://localhost:3000/variables');
        this.variables = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des variables:', error);
      }
    },
    async fetchFormules() {
      try {
        const response = await axios.get('http://localhost:3000/formules');
        this.formules = response.data;
      } catch (error) {
        console.error('Erreur lors de la récupération des formules:', error);
      }
    },
    addToFormula(item) {
      this.formuleFormula = this.formuleFormula ? `${this.formuleFormula} ${item}` : item;
    },
    resetForm() {
      this.formuleFormula = '';
      this.formuleName = '';
    }
  },
  mounted() {
    this.fetchVariables();
    this.fetchFormules();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #c3b9c1;
}

.form {
  margin-bottom: 30px;
}

.label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #0078da;
}

.resformule{
  color: rgb(255, 106, 0);
}

.input,
.variable-select,
.formula-builder,
li {
  width: 500px; /* Même largeur */
  max-width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
}

.button {
  background-color: #508dff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s;
}

.button:hover {
  background-color: #1056f9;
}

.formula-builder {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  background-color: #f9f9f9;
  margin-bottom: 20px;
}

.formula-display {
  min-height: 50px;
  padding: 10px;
  font-size: 18px;
  background: white;
  border: 1px solid #ddd;
  margin-bottom: 15px;
  border-radius: 5px;
  text-align: left;
  color: #5d0404;
}

.variables-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.operator-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  transition: background-color 0.3s;
}

.operator-button:hover {
  background-color: #0056b3;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
}

.success {
  background-color: #d4edda;
  color: #155724;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  background: #f1f1f1;
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
}

li strong {
  color: #333;
}

.reset-button {
  background-color: #f0ad4e;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  margin-left: 10px;
}

.reset-button:hover {
  background-color: #ec971f;
}
</style>
