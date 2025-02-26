const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();
const port = 3000;
const { spawn } = require('child_process');


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors()); // Permet les requêtes CORS

// Configuration de la connexion à la base de données
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'omarleboss',
  database: 'Calculs',
  port: 4306,
  connectTimeout: 60000 // Augmente le délai d'attente à 60 secondes
});

db.connect((err) => {
  if (err) {
    console.error('Erreur de connexion à la base de données:', err);
    return;
  }
  console.log('Connecté à la base de données MySQL');
});

// Middleware pour gérer les erreurs
app.use((err, req, res, next) => {
  console.error('Erreur interne du serveur:', err);
  res.status(500).json({ error: 'Erreur interne du serveur' });
});

// Route pour récupérer toutes les formules (GET)
app.get('/formules', (req, res, next) => {
  const sql = 'SELECT * FROM formules';
  db.query(sql, (err, results) => {
    if (err) {
      console.error('Erreur lors de la récupération des formules:', err);
      return next(err);
    }
    res.json(results);
  });
});

// Route pour ajouter une nouvelle formule (POST)
app.post('/formules', (req, res, next) => {
  const { name, formula } = req.body;
  if (!name || !formula) {
    return res.status(400).json({ error: 'Nom et formule sont requis' });
  }
  const sql = 'INSERT INTO formules (name, formula) VALUES (?, ?)';
  db.query(sql, [name, formula], (err, result) => {
    if (err) {
      console.error('Erreur lors de l\'ajout de la formule:', err);
      return next(err);
    }
    res.status(201).json({ id: result.insertId, name, formula });
  });
});

// Route pour récupérer toutes les variables (GET)
app.get('/variables', (req, res, next) => {
  const sql = 'SELECT * FROM variables';
  db.query(sql, (err, results) => {
    if (err) {
      console.error('Erreur lors de la récupération des variables:', err);
      return next(err);
    }
    res.json(results);
  });
});

// Route pour ajouter une nouvelle variable (POST)
app.post('/variables', (req, res, next) => {
  const { name } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'Nom est requis' });
  }
  const sql = 'INSERT INTO variables (name) VALUES (?)';
  db.query(sql, [name], (err, result) => {
    if (err) {
      console.error('Erreur lors de l\'ajout de la variable:', err);
      return next(err);
    }
    res.status(201).json({ id: result.insertId, name });
  });
});


app.listen(port, () => {
  console.log(`Serveur en écoute sur le port ${port}`);
});
