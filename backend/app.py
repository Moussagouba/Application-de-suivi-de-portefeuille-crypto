import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from models import create_models
import requests
import json
import time
from datetime import datetime

# Initialiser Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'crypto_portfolio_mobile_2025_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///crypto_portfolio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# Initialiser SQLAlchemy
db = SQLAlchemy(app)

# Créer les modèles avec l'instance db
User, Crypto = create_models(db)

# Configuration Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info'

# Rendre current_user disponible dans tous les templates
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_current_user():
    """Rendre current_user disponible dans tous les templates"""
    from flask_login import current_user
    return dict(current_user=current_user)

# Initialisation automatique de la base de données
def init_database():
    """Créer toutes les tables si elles n'existent pas"""
    try:
        with app.app_context():
            db.create_all()
            print("Base de donnees initialisee avec succes!")
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base: {e}")

# Initialiser la base de données au démarrage
init_database()
# Routes d'authentification
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Inscription d'un nouvel utilisateur"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not email or not password:
            flash('Tous les champs sont requis.', 'error')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return redirect(url_for('register'))
        
        # Vérifier si l'utilisateur existe déjà
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur est déjà pris.', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Cette adresse email est déjà utilisée.', 'error')
            return redirect(url_for('register'))
        
        # Créer le nouvel utilisateur
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Connexion d'un utilisateur existant"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Connexion réussie!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté avec succès.', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    """Profil utilisateur"""
    return render_template('profile.html')

# API simple CoinGecko
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Mapping des symboles vers les IDs CoinGecko
SYMBOL_TO_ID = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum', 
    'ADA': 'cardano',
    'DOT': 'polkadot',
    'LINK': 'chainlink',
    'LTC': 'litecoin',
    'XRP': 'ripple',
    'BNB': 'binancecoin',
    'DOGE': 'dogecoin',
    'SOL': 'solana',
    'MATIC': 'matic-network',
    'AVAX': 'avalanche-2',
    'UNI': 'uniswap',
    'ATOM': 'cosmos',
    'VET': 'vechain',
    'FIL': 'filecoin',
    'TRX': 'tron',
    'ETC': 'ethereum-classic',
    'XLM': 'stellar',
    'BCH': 'bitcoin-cash'
}

# Cache pour éviter trop d'appels API
price_cache = {}
CACHE_DURATION = 300  # 5 minutes

# Contrôle de rate limiting
last_api_call = 0
MIN_API_INTERVAL = 1.1  # Minimum 1.1 secondes entre les appels

def rate_limit():
    """Respecte le rate limiting de l'API"""
    global last_api_call
    now = time.time()
    elapsed = now - last_api_call
    if elapsed < MIN_API_INTERVAL:
        time.sleep(MIN_API_INTERVAL - elapsed)
    last_api_call = time.time()

def get_cached_price(symbol):
    """Récupère le prix avec cache pour optimiser les performances"""
    now = datetime.now()
    if symbol in price_cache:
        cached_data, timestamp = price_cache[symbol]
        if (now - timestamp).seconds < CACHE_DURATION:
            return cached_data
    
    return None

def set_cached_price(symbol, price_data):
    """Met en cache les données de prix"""
    price_cache[symbol] = (price_data, datetime.now())

def get_crypto_price_simple(symbol):
    """Récupère le prix via l'API simple CoinGecko avec rate limiting"""
    try:
        # Vérifie le cache d'abord
        cached = get_cached_price(symbol)
        if cached:
            return cached
        
        # Rate limiting
        rate_limit()
        
        # Convertit le symbole en ID CoinGecko
        coin_id = SYMBOL_TO_ID.get(symbol.upper())
        if not coin_id:
            # Essaie de rechercher par nom
            search_url = f"{COINGECKO_API}/search"
            rate_limit()  # Rate limiting pour la recherche aussi
            search_response = requests.get(search_url, params={'query': symbol}, timeout=5)
            
            if search_response.status_code == 429:
                app.logger.warning(f"Rate limit hit for search: {symbol}")
                return {'price': 0, 'change_24h': 0}
                
            search_data = search_response.json()
            
            if not search_data.get('coins'):
                return {'price': 0, 'change_24h': 0}
            
            coin_id = search_data['coins'][0]['id']
        
        # Récupère le prix simple
        price_url = f"{COINGECKO_API}/simple/price"
        params = {
            'ids': coin_id,
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(price_url, params=params, timeout=10)
        
        if response.status_code == 429:
            app.logger.warning(f"Rate limit hit for price: {symbol}")
            return {'price': 0, 'change_24h': 0}
            
        response.raise_for_status()
        data = response.json()
        
        price_info = {
            'price': data.get(coin_id, {}).get('usd', 0),
            'change_24h': data.get(coin_id, {}).get('usd_24h_change', 0)
        }
        
        # Met en cache
        set_cached_price(symbol, price_info)
        return price_info
        
    except requests.exceptions.RequestException as e:
        if e.response and e.response.status_code == 429:
            app.logger.warning(f"Rate limit API pour {symbol}: {e}")
        else:
            app.logger.error(f"Erreur réseau pour {symbol}: {e}")
        return {'price': 0, 'change_24h': 0}
    except Exception as e:
        app.logger.error(f"Erreur prix {symbol}: {e}")
        return {'price': 0, 'change_24h': 0}

def search_crypto_coinGecko(query):
    """Recherche de cryptomonnaies via l'API CoinGecko avec rate limiting"""
    try:
        rate_limit()  # Rate limiting
        
        url = f"{COINGECKO_API}/search"
        response = requests.get(url, params={'query': query}, timeout=5)
        
        if response.status_code == 429:
            app.logger.warning(f"Rate limit hit for search: {query}")
            return []
            
        response.raise_for_status()
        data = response.json()
        
        results = []
        for coin in data.get('coins', [])[:10]:
            results.append({
                'id': coin['id'],
                'name': coin['name'],
                'symbol': coin['symbol'].upper(),
                'image': coin.get('thumb', '')
            })
        return results
    except Exception as e:
        app.logger.error(f"Erreur recherche crypto: {e}")
        return []

@app.route('/')
@login_required
def index():
    """Page d'accueil - Tableau de bord principal"""
    cryptos = Crypto.query.filter_by(user_id=current_user.id).all()
    total_portfolio_value = 0
    total_profit_loss = 0
    total_invested = 0
    
    # Calcule les valeurs sans les stocker dans la base
    for crypto in cryptos:
        # Récupère les prix actuels
        price_info = get_crypto_price_simple(crypto.symbol)
        current_price = price_info['price']
        change_24h = price_info['change_24h']
        
        # Met à jour la base de données seulement avec les champs stockés
        crypto.current_price = current_price
        crypto.price_change_24h = change_24h
        crypto.last_updated = datetime.now()
        
        # Calcule les valeurs (propriétés calculées)
        crypto_value = crypto.current_value  # Utilise la propriété calculée
        crypto_profit_loss = crypto.profit_loss  # Utilise la propriété calculée
        crypto_invested = crypto.quantity * crypto.purchase_price  # Calcul direct
        
        total_portfolio_value += crypto_value
        total_profit_loss += crypto_profit_loss
        total_invested += crypto_invested
    
    # Sauvegarde des mises à jour
    db.session.commit()
    
    total_profit_loss_percentage = (total_profit_loss/total_portfolio_value*100) if total_portfolio_value > 0 else 0
    
    return render_template('index.html',
                         cryptos=cryptos,
                         total_portfolio_value=total_portfolio_value,
                         total_profit_loss=total_profit_loss,
                         total_profit_loss_percentage=total_profit_loss_percentage,
                         total_invested=total_invested)

@app.route('/search_crypto', methods=['POST'])
def search_crypto():
    """API pour rechercher des cryptomonnaies"""
    query = request.json.get('query', '')
    if not query or len(query) < 2:
        return jsonify({'results': []})
    
    results = search_crypto_coinGecko(query)
    return jsonify({'results': results})

@app.route('/api/crypto_price/<symbol>')
def api_crypto_price(symbol):
    """API pour obtenir le prix d'une crypto"""
    price_info = get_crypto_price_simple(symbol)
    return jsonify(price_info)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_crypto():
    """Ajouter une nouvelle cryptomonnaie"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            symbol = request.form['symbol'].upper()
            quantity = float(request.form['quantity'])
            purchase_price = float(request.form['purchase_price'])
            
            # Vérifier si la crypto existe déjà pour cet utilisateur
            existing_crypto = Crypto.query.filter_by(
                user_id=current_user.id,
                symbol=symbol
            ).first()
            
            if existing_crypto:
                # Mettre à jour la quantité existante
                existing_crypto.quantity += quantity
                existing_crypto.purchase_price = (existing_crypto.purchase_price + purchase_price) / 2
                existing_crypto.last_updated = datetime.now()
                flash(f'{name} mise à jour avec succès! Quantité totale: {existing_crypto.quantity}', 'success')
            else:
                # Récupère le prix actuel automatiquement
                price_info = get_crypto_price_simple(symbol)
                current_price = price_info['price']
                
                # Créer la nouvelle cryptomonnaie
                new_crypto = Crypto(
                    name=name,
                    symbol=symbol,
                    quantity=quantity,
                    purchase_price=purchase_price,
                    current_price=current_price,
                    price_change_24h=price_info['change_24h'],
                    last_updated=datetime.now(),
                    user_id=current_user.id
                )
                
                db.session.add(new_crypto)
                flash(f'{name} ajoutée avec succès! Prix actuel: ${current_price:.2f}', 'success')
            
            db.session.commit()
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Erreur lors de l\'ajout: {str(e)}', 'error')
            return redirect(url_for('add_crypto'))
    
    return render_template('add_crypto.html')

@app.route('/edit/<int:crypto_id>', methods=['GET', 'POST'])
def edit_crypto(crypto_id):
    """Éditer une cryptomonnaie - FONCTIONNALITÉ DÉSACTIVÉE"""
    # Redirige vers l'accueil avec un message
    flash('La modification des cryptomonnaies est désactivée. Vous pouvez uniquement ajouter et supprimer des cryptos.', 'info')
    return redirect(url_for('index'))

@app.route('/delete/<int:crypto_id>', methods=['POST'])
@login_required
def delete_crypto(crypto_id):
    """Supprimer une cryptomonnaie"""
    crypto = Crypto.query.filter_by(id=crypto_id, user_id=current_user.id).first_or_404()
    crypto_name = crypto.name
    
    try:
        db.session.delete(crypto)
        db.session.commit()
        flash(f'{crypto_name} supprimée avec succès!', 'success')
    except Exception as e:
        flash(f'Erreur lors de la suppression: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/refresh_prices', methods=['POST'])
@login_required
def refresh_prices():
    """Rafraîchir tous les prix"""
    try:
        cryptos = Crypto.query.filter_by(user_id=current_user.id).all()
        updated_count = 0
        
        for crypto in cryptos:
            price_info = get_crypto_price_simple(crypto.symbol)
            crypto.current_price = price_info['price']
            crypto.price_change_24h = price_info['change_24h']
            crypto.last_updated = datetime.now()
            updated_count += 1
        
        db.session.commit()
        flash(f'{updated_count} prix mis à jour avec succès!', 'success')
        
    except Exception as e:
        flash(f'Erreur lors de la mise à jour: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/portfolio_stats')
@login_required
def api_portfolio_stats():
    """API pour les statistiques du portefeuille"""
    try:
        cryptos = Crypto.query.filter_by(user_id=current_user.id).all()
        
        if not cryptos:
            return jsonify({
                'total_value': 0,
                'total_profit_loss': 0,
                'total_invested': 0,
                'best_performer': None,
                'worst_performer': None
            })
        
        total_value = sum(c.current_value for c in cryptos)
        total_invested = sum(c.quantity * c.purchase_price for c in cryptos)
        total_profit_loss = total_value - total_invested
        
        # Trouve les meilleures et pires performances
        performers = []
        for crypto in cryptos:
            if crypto.purchase_price > 0:
                performance = crypto.profit_loss_percentage
                performers.append((crypto, performance))
        
        if performers:
            best_performer = max(performers, key=lambda x: x[1])
            worst_performer = min(performers, key=lambda x: x[1])
        else:
            best_performer = worst_performer = None
        
        return jsonify({
            'total_value': round(total_value, 2),
            'total_profit_loss': round(total_profit_loss, 2),
            'total_invested': round(total_invested, 2),
            'profit_loss_percentage': round((total_profit_loss/total_invested*100) if total_invested > 0 else 0, 2),
            'best_performer': {
                'name': best_performer[0].name,
                'symbol': best_performer[0].symbol,
                'performance': round(best_performer[1], 2)
            } if best_performer else None,
            'worst_performer': {
                'name': worst_performer[0].name,
                'symbol': worst_performer[0].symbol,
                'performance': round(worst_performer[1], 2)
            } if worst_performer else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market_data')
def api_market_data():
    """API pour les données du marché (top cryptos) avec rate limiting"""
    try:
        rate_limit()  # Rate limiting
        
        # Top cryptos populaires
        popular_ids = ['bitcoin', 'ethereum', 'cardano', 'polkadot', 'chainlink', 
                      'litecoin', 'ripple', 'binancecoin', 'dogecoin', 'solana']
        
        url = f"{COINGECKO_API}/simple/price"
        params = {
            'ids': ','.join(popular_ids),
            'vs_currencies': 'usd',
            'include_24hr_change': 'true'
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 429:
            app.logger.warning("Rate limit hit for market data")
            return jsonify({
                'market_data': [
                    {'name': 'Bitcoin', 'symbol': 'BTC', 'current_price': 45000, 'price_change_24h': 2.5},
                    {'name': 'Ethereum', 'symbol': 'ETH', 'current_price': 2800, 'price_change_24h': 1.8}
                ]
            })
            
        response.raise_for_status()
        data = response.json()
        
        market_data = []
        for coin_id, info in data.items():
            # Mapping inverse pour obtenir le nom
            coin_name = coin_id.replace('-', ' ').title()
            market_data.append({
                'name': coin_name,
                'symbol': coin_id.upper(),
                'current_price': info['usd'],
                'price_change_24h': info.get('usd_24h_change', 0),
                'image': f"https://assets.coingecko.com/coins/images/1/large/{coin_id}.png"
            })
        
        return jsonify({'market_data': market_data})
        
    except Exception as e:
        app.logger.error(f"Erreur market_data: {e}")
        # Retourne des données par défaut en cas d'erreur
        return jsonify({
            'market_data': [
                {'name': 'Bitcoin', 'symbol': 'BTC', 'current_price': 45000, 'price_change_24h': 2.5},
                {'name': 'Ethereum', 'symbol': 'ETH', 'current_price': 2800, 'price_change_24h': 1.8}
            ]
        })

@app.route('/settings')
@login_required
def settings():
    """Page des paramètres"""
    return render_template('settings.html')

@app.route('/analytics')
@login_required
def portfolio_analytics():
    """Page d'analytics du portefeuille"""
    cryptos = Crypto.query.filter_by(user_id=current_user.id).all()
    
    if not cryptos:
        return render_template('analytics.html',
                             has_data=False,
                             total_portfolio_value=0,
                             total_profit_loss=0,
                             best_performer=None,
                             worst_performer=None)
    
    total_portfolio_value = sum(c.current_value for c in cryptos)
    total_invested = sum(c.quantity * c.purchase_price for c in cryptos)
    total_profit_loss = total_portfolio_value - total_invested
    
    # Trouve les meilleures et pires performances
    performers = []
    for crypto in cryptos:
        if crypto.purchase_price > 0:
            performance = crypto.profit_loss_percentage
            performers.append((crypto, performance))
    
    best_performer = max(performers, key=lambda x: x[1]) if performers else None
    worst_performer = min(performers, key=lambda x: x[1]) if performers else None
    
    return render_template('analytics.html',
                         has_data=True,
                         cryptos=cryptos,
                         total_portfolio_value=total_portfolio_value,
                         total_profit_loss=total_profit_loss,
                         total_invested=total_invested,
                         best_performer=best_performer[0] if best_performer else None,
                         worst_performer=worst_performer[0] if worst_performer else None,
                         best_performance=best_performer[1] if best_performer else 0,
                         worst_performance=worst_performer[1] if worst_performer else 0)

@app.route('/market')
@login_required
def market_overview():
    """Page de vue d'ensemble du marché"""
    return render_template('market.html')

@app.route('/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw_crypto():
    """Page de retrait/vente de cryptomonnaies"""
    cryptos = Crypto.query.filter_by(user_id=current_user.id).all()
    
    # Calculer les statistiques du portefeuille
    total_portfolio_value = sum(c.current_value for c in cryptos) if cryptos else 0
    total_invested = sum(c.quantity * c.purchase_price for c in cryptos) if cryptos else 0
    total_profit_loss = total_portfolio_value - total_invested if cryptos else 0
    total_profit_loss_percentage = (total_profit_loss/total_invested*100) if total_invested > 0 else 0
    
    if request.method == 'POST':
        try:
            crypto_id = request.form['crypto_id']
            quantity_to_withdraw = float(request.form['quantity'])
            current_price = float(request.form['current_price'])
            
            crypto = Crypto.query.filter_by(id=crypto_id, user_id=current_user.id).first_or_404()
            
            if quantity_to_withdraw > crypto.quantity:
                flash('Quantité insuffisante dans le portefeuille', 'error')
                return redirect(url_for('withdraw_crypto'))
            
            # Calculer la valeur du retrait
            withdraw_value = quantity_to_withdraw * current_price
            
            # Mettre à jour la quantité
            crypto.quantity -= quantity_to_withdraw
            crypto.last_updated = datetime.now()
            
            # Si quantité devient 0, supprimer la crypto
            if crypto.quantity <= 0.001:
                db.session.delete(crypto)
                flash(f'{crypto.name} retirée complètement du portefeuille', 'success')
            else:
                flash(f'Retrait de {quantity_to_withdraw} {crypto.symbol} effectué. Valeur: ${withdraw_value:.2f}', 'success')
            
            db.session.commit()
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Erreur lors du retrait: {str(e)}', 'error')
            return redirect(url_for('withdraw_crypto'))
    
    return render_template('withdraw.html',
                         cryptos=cryptos,
                         total_value=total_portfolio_value,
                         total_profit_loss=total_profit_loss,
                         total_profit_loss_percentage=total_profit_loss_percentage)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)