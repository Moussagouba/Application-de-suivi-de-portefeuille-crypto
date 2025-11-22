# 🛠️ Configuration Netlify pour Flask

## 📋 Configuration des Paramètres de Build

Selon votre interface, configurez ainsi :

### Build Settings
```
Branch to deploy: main
Base directory: (laisser vide)
Build command: npm run build
Publish directory: dist
Functions directory: netlify/functions
```

### 🏗️ Architecture de Déploiement Netlify

```
Application/
├── netlify/              # Netlify Functions (Backend)
│   └── functions/
│       ├── index.js      # API handlers
│       ├── crypto-price.js
│       └── portfolio-stats.js
├── frontend/             # Frontend statique
│   ├── index.html
│   ├── assets/
│   └── api-calls.js
├── dist/                 # Build output
└── package.json          # Build scripts
```

## 🔧 Fichiers de Configuration Requis

### 1. package.json
```json
{
  "name": "crypto-portfolio-netlify",
  "version": "1.0.0",
  "scripts": {
    "build": "echo 'No build needed for static files'",
    "serve": "python -m http.server 8000"
  }
}
```

### 2. netlify.toml
```toml
[build]
  publish = "frontend"
  command = "npm run build"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

## 🚀 Étapes de Préparation

### 1. Créer la Structure
```bash
# Créer dossiers
mkdir frontend netlify/functions dist

# Copier les fichiers Flask vers l'architecture Netlify
cp templates/* frontend/
cp static/* frontend/assets/
```

### 2. Netlify Functions pour l'API

Créer `netlify/functions/index.js` :
```javascript
// Handler principal pour les routes Flask
const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  const path = event.path;
  const method = event.httpMethod;
  
  // Routing API
  if (path.includes('/api/crypto_price/')) {
    return handleCryptoPrice(event, context);
  } else if (path.includes('/api/portfolio_stats')) {
    return handlePortfolioStats(event, context);
  } else if (path === '/api/search_crypto') {
    return handleSearchCrypto(event, context);
  }
  
  return {
    statusCode: 404,
    body: JSON.stringify({ error: 'Not found' })
  };
};

async function handleCryptoPrice(event, context) {
  // Implémenter l'appel à CoinGecko
  const symbol = event.path.split('/').pop();
  const response = await fetch(`https://api.coingecko.com/api/v3/simple/price?ids=${symbol}&vs_currencies=usd`);
  const data = await response.json();
  
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  };
}
```

### 3. Adapter le Frontend

Modifier `frontend/index.html` pour utiliser localStorage au lieu des sessions Flask :
```javascript
// api-calls.js
const API_BASE = '/.netlify/functions';

// Remplacer les appels Flask par des appels Netlify Functions
async function fetchCryptoPrice(symbol) {
  const response = await fetch(`${API_BASE}/api/crypto_price/${symbol}`);
  return response.json();
}

// Authentification avec localStorage
function getCurrentUser() {
  return JSON.parse(localStorage.getItem('crypto_user'));
}

function saveUser(userData) {
  localStorage.setItem('crypto_user', JSON.stringify(userData));
}
```

## ⚙️ Variables d'Environnement Netlify

Dans l'interface Netlify, ajoutez :

```
COINGECKO_API_URL=https://api.coingecko.com/api/v3
ENVIRONMENT=production
```

## 🚧 Limitations à Considérer

### ❌ Fonctionnalités Non Supportées
- Sessions Flask persistantes
- Base de données SQLite
- Authentification serveur-side
- WebSockets

### ✅ Solutions Alternatives
- **Authentification** : Firebase Auth, Auth0
- **Base de données** : Supabase, Firebase Firestore
- **Sessions** : localStorage + JWT
- **State Management** : Redux ou Context API

## 🎯 Déploiement Rapide

1. **Push sur GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Netlify deployment"
   git push origin main
   ```

2. **Connecter sur Netlify**
   - Sélectionner le repository
   - Configurer les paramètres ci-dessus
   - Déployer

3. **Tester**
   - Vérifier que l'interface se charge
   - Tester les appels API via Netlify Functions
   - Configurer la base de données cloud

## 🔗 Base de Données Cloud Recommandée

### Supabase (Gratuit)
```javascript
// Dans les Netlify Functions
const { createClient } = require('@supabase/supabase-js');
const supabase = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_KEY);
```

### Configuration Supabase
1. Créer compte sur supabase.io
2. Créer base de données
3. Obtenir URL et clé API
4. Configurer dans les variables Netlify

---

**⚠️ Note : Cette configuration transforme votre app Flask en une application SPA avec backend serverless. Fonctionnel mais avec des limitations.**

**Voulez-vous que je vous aide à implémenter cette configuration Netlify ?**