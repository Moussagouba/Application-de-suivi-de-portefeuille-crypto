# Portefeuille Crypto - Application de Suivi de Cryptomonnaies

## 📱 Description

**Portefeuille Crypto** est une application web moderne et intuitive permettant de suivre et gérer votre portefeuille de cryptomonnaies en temps réel. L'application offre une interface utilisateur responsive et des fonctionnalités complètes pour le suivi des investissements crypto.

## ✨ Fonctionnalités Principales

### 📊 Suivi du Portefeuille
- **Ajout de cryptomonnaies** : Recherchez et ajoutez facilement des cryptos à votre portefeuille
- **Suivi en temps réel** : Prix actuels mis à jour automatiquement via l'API CoinGecko
- **Calcul des gains/pertes** : Visualisation instantanée de vos performances
- **Statistiques détaillées** : Analyse complète de votre portefeuille avec graphiques

### 💰 Gestion Financière
- **Ajout d'actifs** : Spécifiez la quantité et le prix d'achat
- **Retrait/Vente** : Gérez vos ventes partielles ou totales
- **Historique des transactions** : Suivi de tous vos mouvements
- **Calcul de performance** : Pourcentage de gains/pertes en temps réel

### 📈 Analytics et Visualisation
- **Tableau de bord principal** : Vue d'ensemble de votre portefeuille
- **Analytics avancées** : Analyse des meilleures/pires performances
- **Marché en direct** : Suivi des principales cryptomonnaies
- **Graphiques interactifs** : Visualisation de l'évolution

### 🔄 Fonctionnalités Techniques
- **Mise à jour automatique** : Actualisation des prix toutes les 5 minutes
- **Cache intelligent** : Optimisation des performances avec système de cache
- **Rate limiting** : Respect des limites de l'API CoinGecko
- **API REST** : Endpoints pour intégrations externes

### 📱 Compatibilité Mobile
- **Design responsive** : Interface adaptée mobile et desktop
- **Conversion APK** : Script de build inclus pour créer une application Android
- **Optimisation tactile** : Interface optimisée pour les écrans tactiles

## 🛠️ Technologies Utilisées

### Backend
- **Flask 2.3.3** : Framework web Python
- **Flask-Login 0.6.3** : Gestion des sessions utilisateur
- **Flask-SQLAlchemy 3.0.5** : ORM pour la base de données
- **Werkzeug 2.3.7** : Sécurité et hachage des mots de passe
- **PostgreSQL (Neon)** : Base de données cloud
- **psycopg2-binary 2.9.10** : Driver PostgreSQL

### Frontend
- **HTML5/CSS3** : Interface moderne et responsive
- **JavaScript (ES6+)** : Interactions dynamiques
- **Font Awesome** : Icônes vectorielles

### Intégrations
- **CoinGecko API** : Données de marché en temps réel
- **Neon PostgreSQL** : Base de données cloud serverless
- **Netlify Functions** : API serverless pour les prix crypto
- **Capacitor** : Framework pour conversion mobile

## 📁 Structure du Projet

```
crypto-portfolio/
├── backend/              # Code backend Python
│   ├── app.py            # Application Flask principale
│   ├── models.py         # Modèles de base de données
│   ├── requirements.txt  # Dépendances Python backend
│   ├── .env              # Variables d'environnement
│   └── Procfile          # Configuration Heroku
├── frontend/             # Interface utilisateur
│   └── index.html        # Application SPA complète
├── netlify/              # Fonctions serverless Netlify
│   └── functions/
│       ├── crypto-api.js # API pour prix crypto
│       └── package.json  # Dépendances Node.js
├── templates/            # Templates HTML (Flask)
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── analytics.html    # Analytics du portefeuille
│   ├── add_crypto.html   # Ajout de cryptomonnaies
│   ├── market.html       # Vue du marché
│   └── withdraw.html     # Retrait/vente
├── static/               # Fichiers statiques
│   ├── css/
│   │   └── style.css     # Styles CSS
│   └── js/
│       └── chart.js      # Scripts JavaScript
├── instance/             # Base de données locale
│   └── crypto_portfolio.db  # SQLite (fallback)
├── main.py               # Point d'entrée principal
├── requirements.txt      # Dépendances Python (racine)
├── netlify.toml          # Configuration Netlify
├── runtime.txt           # Version Python pour Netlify
├── build_apk.sh          # Script de build APK
└── init_db.py            # Initialisation de la base
```

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### 1. Cloner le projet
```bash
git clone <repository-url>
cd crypto-portfolio
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Initialiser la base de données
```bash
python init_db.py
```

### 4. Lancer l'application
```bash
python app.py
```

L'application sera accessible sur : `http://127.0.0.1:8080`

### Déploiement sur Netlify (Recommandé)

1. **Connecter le repository** sur Netlify
2. **Variables d'environnement** :
   - `DATABASE_URL` : URL de connexion Neon PostgreSQL
   - `SECRET_KEY` : Clé secrète pour Flask
3. **Build settings** :
   - **Build command** : `echo 'Static frontend ready'`
   - **Publish directory** : `frontend`
4. **Fonctions serverless** : Automatiquement déployées depuis `netlify/functions/`

L'application sera accessible sur votre domaine Netlify avec API fonctionnelle !

## 🔑 Première Utilisation - Authentification

### 1. Créer un compte
1. Accédez à l'application sur `http://127.0.0.1:8080`
2. Vous serez automatiquement redirigé vers la page de connexion
3. Cliquez sur "Créer un compte"
4. Remplissez le formulaire d'inscription :
   - **Nom d'utilisateur** : Choisissez un nom unique (min. 3 caractères)
   - **Email** : Votre adresse email pour la récupération de compte
   - **Mot de passe** : Créez un mot de passe sécurisé (min. 6 caractères)
   - **Confirmer le mot de passe** : Saisissez le même mot de passe
5. Cliquez sur "Créer mon compte"

### 2. Se connecter
1. Utilisez vos identifiants sur la page de connexion
2. Accédez à votre portefeuille personnalisé
3. Vos données sont séparées des autres utilisateurs

### 3. Interface utilisateur
- **Profil** : Accessible via le menu "Mon Profil"
- **Connexion** : Statut affiché en temps réel
- **Sécurité** : Déconnexion via le profil ou menu

## 📱 Création de l'Application Mobile (APK)

### Option 1 : Script automatisé
```bash
chmod +x build_apk.sh
./build_apk.sh
```

### Option 2 : Manuel avec Capacitor
```bash
# Installation de Capacitor
npm install -g @capacitor/core @capacitor/cli @capacitor/android

# Initialisation
npx cap init "Portefeuille Crypto" "com.cryptoportfolio.app"

# Ajout plateforme Android
npx cap add android

# Copie des fichiers
npx cap copy

# Build APK
npx cap run android
```

## 🔧 Configuration

### Variables d'Environnement
L'application utilise les configurations suivantes dans `app.py` :
- `SECRET_KEY` : Clé secrète Flask
- `SQLALCHEMY_DATABASE_URI` : URI de la base de données
- `COINGECKO_API` : URL de l'API CoinGecko

### Support des Cryptomonnaies
L'application supporte automatiquement les principales cryptomonnaies :
- Bitcoin (BTC)
- Ethereum (ETH)
- Cardano (ADA)
- Polkadot (DOT)
- Chainlink (LINK)
- Litecoin (LTC)
- Ripple (XRP)
- Binance Coin (BNB)
- Dogecoin (DOGE)
- Solana (SOL)
- Et plus de 19 autres cryptomonnaies populaires

## 📊 API Endpoints

### Endpoints Publics
- `GET /` : Page d'accueil du portefeuille
- `GET /add` : Formulaire d'ajout de crypto
- `GET /analytics` : Page d'analytics
- `GET /market` : Vue du marché
- `GET /withdraw` : Page de retrait

### API REST
- `POST /search_crypto` : Recherche de cryptomonnaies
- `GET /api/crypto_price/<symbol>` : Prix d'une crypto
- `GET /api/market_data` : Données du marché

### API Authentification
- `POST /auth-api/register` : Inscription utilisateur
- `POST /auth-api/login` : Connexion utilisateur
- `GET /auth-api/verify` : Vérification token JWT
- `GET /auth-api/profile` : Profil utilisateur (protégé)

## 🎨 Interface Utilisateur

### Design Moderne
- **Thème sombre/clair** adaptatif
- **Cards responsive** pour une meilleure lisibilité
- **Animations fluides** pour une expérience utilisateur premium
- **Icons Font Awesome** pour une navigation intuitive

### Mobile-First
- **Interface tactile** optimisée
- **Navigation adaptative** selon la taille d'écran
- **Performance** optimisée pour mobile

## 👤 Authentification Utilisateur

### 🔑 Fonctionnalités d'Authentification
- **Inscription sécurisée** avec validation des données
- **Connexion/Déconnexion** avec JWT tokens
- **Hachage des mots de passe** avec bcrypt
- **Interface utilisateur** avec informations de profil
- **Protection des routes** avec tokens JWT
- **Vérification automatique** des tokens à chaque chargement

### 🏷️ Gestion des Comptes
- **Profil utilisateur** avec informations personnelles
- **Statut de connexion** en temps réel
- **Séparation des données** par utilisateur
- **Base de données relationnelle** User-Crypto

### 🛡️ Sécurité
- **Rate limiting** pour respecter les APIs externes
- **Validation des données** côté serveur
- **Protection CSRF** avec Flask-WTF
- **Base de données locale** pour la confidentialité

## 📈 Performances

- **Cache intelligent** pour réduire les appels API
- **Pagination** des données volumineuses
- **Optimisation SQL** avec SQLAlchemy
- **Minification** des ressources statiques

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committer vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pusher vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Consultez la documentation
2. Vérifiez les issues existantes
3. Créez une nouvelle issue avec les détails du problème

## 🚧 Roadmap

- [ ] Graphiques en temps réel
- [ ] Export des données (CSV, PDF)
- [ ] Alertes de prix
- [ ] Portfolio multi-devises
- [ ] Historique des transactions détaillé
- [ ] Intégration d'autres APIs (Binance, Coinbase)
- [ ] Application iOS
- [ ] Authentification utilisateur
- [ ] Cloud sync

---

**Développé avec ❤️ pour la communauté crypto française**