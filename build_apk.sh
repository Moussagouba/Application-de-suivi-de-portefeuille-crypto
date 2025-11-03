#!/bin/bash

echo "🚀 Configuration de Capacitor pour convertir l'app web en APK"

# 1. Installation de Capacitor
npm install -g @capacitor/core @capacitor/cli @capacitor/android
npm install -g @capacitor/app @capacitor/haptics @capacitor/keyboard @capacitor/status-bar

# 2. Initialisation du projet
npx cap init "Portefeuille Crypto" "com.cryptoportfolio.app"

# 3. Ajout de la plateforme Android
npx cap add android

# 4. Copie des fichiers web
npx cap copy

# 5. Configuration Android
# Pour déployer sur APK de développement :
npx cap run android

# Pour ouvrir Android Studio (production) :
# npx cap open android

echo "✅ Configuration terminée!"
echo "Pour créer l'APK :"
echo "1. npx cap open android"
echo "2. Dans Android Studio : Build > Generate Signed Bundle/APK"
echo "3. Suivez les étapes pour signer votre APK"