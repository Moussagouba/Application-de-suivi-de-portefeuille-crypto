#!/usr/bin/env python3
# Script pour initialiser la base de données avec toutes les colonnes nécessaires

from app import app, db
from models import Crypto

def init_database():
    """Initialise la base de données avec toutes les colonnes"""
    with app.app_context():
        try:
            # Supprime toutes les tables existantes
            db.drop_all()
            print("Anciennes tables supprimées")
            
            # Crée toutes les nouvelles tables
            db.create_all()
            print("Nouvelles tables créées avec succès")
            
            # Vérifie la structure de la table
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = inspector.get_columns('crypto')
            print("\nColonnes dans la table crypto:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
            
            print("\nBase de données initialisée avec succès!")
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'initialisation: {e}")
            return False

if __name__ == '__main__':
    init_database()