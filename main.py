from backend.app import app

if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur: {e}")
        print("Essayez avec un port différent...")
        try:
            app.run(host='127.0.0.1', port=5001, debug=True, use_reloader=False)
        except Exception as e2:
            print(f"Erreur sur le port 5001: {e2}")
            print("Application terminée.")