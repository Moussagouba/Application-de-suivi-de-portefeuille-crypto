from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def create_models(db):
    """Fonction pour créer les modèles avec l'instance db fournie"""
    
    class User(UserMixin, db.Model):
        """Modèle utilisateur avec authentification"""
        __tablename__ = 'user'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(128), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        # Relations
        cryptos = db.relationship('Crypto', backref='owner', lazy=True, cascade='all, delete-orphan')
        
        def set_password(self, password):
            """Hachage du mot de passe"""
            self.password_hash = generate_password_hash(password)
        
        def check_password(self, password):
            """Vérification du mot de passe"""
            return check_password_hash(self.password_hash, password)
        
        def __repr__(self):
            return f'<User {self.username}>'

    class Crypto(db.Model):
        """Modèle de cryptomonnaie associé à un utilisateur"""
        __tablename__ = 'crypto'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        symbol = db.Column(db.String(10), nullable=False)
        quantity = db.Column(db.Float, nullable=False)
        purchase_price = db.Column(db.Float, nullable=False)
        current_price = db.Column(db.Float, nullable=True, default=0)
        price_change_24h = db.Column(db.Float, nullable=True, default=0)
        last_updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
        
        # Clé étrangère vers l'utilisateur
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        
        # Champs calculés (non stockés en base)
        @property
        def current_value(self):
            return (self.current_price or 0) * self.quantity
        
        @property
        def profit_loss(self):
            return ((self.current_price or 0) - self.purchase_price) * self.quantity
        
        @property
        def profit_loss_percentage(self):
            if self.purchase_price > 0:
                return ((self.current_price or 0) - self.purchase_price) / self.purchase_price * 100
            return 0
        
        @property
        def invested_amount(self):
            return self.quantity * self.purchase_price
        
        @property
        def current_value_rounded(self):
            return round(self.current_value, 2)
        
        @property
        def profit_loss_rounded(self):
            return round(self.profit_loss, 2)
        
        @property
        def profit_loss_percentage_rounded(self):
            return round(self.profit_loss_percentage, 2)

        def __repr__(self):
            return f'<Crypto {self.name}>'

    return User, Crypto