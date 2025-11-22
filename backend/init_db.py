#!/usr/bin/env python3
"""
Script d'initialisation de la base de donnees pour l'application Portefeuille Crypto
"""

import sys
import os

# Ajouter le repertoire courant au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db
    from models import User, Crypto
    
    def init_database():
        """Initialise la base de donnees et cree toutes les tables"""
        print("Initialisation de la base de donnees...")
        
        with app.app_context():
            try:
                # Creer toutes les tables
                db.create_all()
                print("Tables creees avec succes!")
                
                # Verifier si des utilisateurs existent deja
                user_count = User.query.count()
                print(f"Nombre d'utilisateurs existants: {user_count}")
                
                print("Base de donnees initialisee avec succes!")
                
            except Exception as e:
                print(f"Erreur lors de l'initialisation: {e}")
    
    def show_database_info():
        """Affiche les informations de la base de donnees"""
        with app.app_context():
            try:
                user_count = User.query.count()
                crypto_count = Crypto.query.count()
                
                print("Informations de la base de donnees:")
                print(f"   - Utilisateurs: {user_count}")
                print(f"   - Cryptomonnaies: {crypto_count}")
                
                if user_count > 0:
                    print("\nUtilisateurs existants:")
                    for user in User.query.all():
                        crypto_count_for_user = Crypto.query.filter_by(user_id=user.id).count()
                        print(f"   - {user.username} ({user.email}) - {crypto_count_for_user} cryptos")
                        
            except Exception as e:
                print(f"Erreur lors de l'acces aux donnees: {e}")

    if __name__ == '__main__':
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == 'init':
                init_database()
            elif command == 'info':
                show_database_info()
            else:
                print("Commande inconnue. Utilisez: init, ou info")
        else:
            print("Usage:")
            print("  python init_db.py init    - Initialiser la base de donnees")
            print("  python init_db.py info    - Afficher les informations de la base")
    
except ImportError as e:
    print(f"Erreur d'importation: {e}")
    print("Assurez-vous d'etre dans le bon repertoire et que les dependances sont installees.")