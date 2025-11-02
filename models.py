from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=True, default=0)
    price_change_24h = db.Column(db.Float, nullable=True, default=0)
    last_updated = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    
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

    def __repr__(self):
        return f'<Crypto {self.name}>'