# Configuration pour Base de Données Neon PostgreSQL

## 📋 Configuration Neon Database

### 1. Créer une Base Neon
1. Aller sur https://neon.tech/
2. Créer un compte gratuit
3. Créer un nouveau projet
4. Copier la connection string

### 2. Variables d'Environnement
```bash
# Database
DATABASE_URL="postgresql://username:password@ep-example.us-east-1.aws.neon.tech/neondb?sslmode=require"

# Flask
SECRET_KEY="votre-cle-secrete-flask"
FLASK_ENV="production"

# API
COINGECKO_API_URL="https://api.coingecko.com/api/v3"
```

### 3. Installation PostgreSQL Adapter
```bash
pip install psycopg2-binary
```

## 🔄 Migration depuis SQLite

### 1. Mise à Jour app.py
- Remplacer `SQLALCHEMY_DATABASE_URI = 'sqlite:///crypto_portfolio.db'`
- Par `SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')`

### 2. Modèles Prêts pour PostgreSQL
- Les modèles User et Crypto sont compatibles PostgreSQL
- Auto-increment pour les IDs
- Types de données adaptés

## 🚀 Avantages Neon

- ✅ PostgreSQL complet (pas SQLite)
- ✅ Haute disponibilité automatique
- ✅ Sauvegardes automatiques
- ✅ Scalabilité illimitée
- ✅ SSL/TLS natif
- ✅ Monitoring intégré