# 📱 Guide de création d'APK pour votre Portefeuille Crypto

## 🎯 Option 1 : Capacitor (Recommandé - Le plus simple)

### Prérequis
1. **Node.js** installé (version 16+)
2. **Android Studio** installé
3. **Java Development Kit (JDK)** 11+

### Étapes :

#### 1. Installation de Capacitor
```bash
# Dans le dossier de votre projet
npm install -g @capacitor/core @capacitor/cli @capacitor/android
npm install @capacitor/app @capacitor/haptics @capacitor/keyboard @capacitor/status-bar
```

#### 2. Initialisation du projet
```bash
npx cap init "Portefeuille Crypto" "com.cryptoportfolio.app"
```

#### 3. Configuration de la production
```bash
# Modifier main.py pour la production
python main.py --production
```

#### 4. Ajout de la plateforme Android
```bash
npx cap add android
npx cap copy
npx cap sync
```

#### 5. Génération de l'APK
```bash
# Développement (APK direct)
npx cap run android

# Production (via Android Studio)
npx cap open android
# Dans Android Studio : Build > Generate Signed Bundle/APK
```

## 🛠 Option 2 : Android Studio (Conversion native)

### Étapes manuelles :
1. Créer un nouveau projet Android vide
2. Configurer un WebView
3. Pointer vers votre serveur Flask local
4. Compiler l'APK

## 📦 Fichiers de configuration fournis

Les fichiers suivants ont été créés pour vous :
- `build_apk.sh` : Script automatisé
- `capacitor.config.ts` : Configuration Capacitor
- `package.json` : Dépendances npm

## 🚀 Démarrage rapide

Exécutez le script :
```bash
chmod +x build_apk.sh
./build_apk.sh
```

Puis suivez les étapes de génération d'APK.

## 💡 Avantages de Capacitor

- ✅ **Multi-plateforme** : Android + iOS
- ✅ **APIs natives** : Caméra, notifications, etc.
- ✅ **Performance** : Optimisé pour mobile
- ✅ **Facilité** : Pas de code Java natif requis
- ✅ ** Communauté** : Maintenu par Ionic

## 🔧 Configuration supplémentaire pour la production

1. **Optimiser le serveur Flask** pour la production
2. **Activer HTTPS** pour les fonctionnalités natives
3. **Signer l'APK** pour la distribution
4. **Tester** sur différents appareils Android

## 📱 Fonctionnalités natives disponibles

Avec Capacitor, votre APK aura accès à :
- Notifications push
- Haptic feedback (vibrations)
- Status bar native
- Fullscreen mode
- Orientation locked
- Biometric authentication

## 🎨 Personnalisation de l'apparence

Le fichier `capacitor.config.ts` contient :
- Nom de l'app
- Bundle ID
- Version
- Configuration web
- Mode de développement/production

## 📋 Checklist pour la distribution

- [ ] Tester l'APK sur plusieurs appareils
- [ ] Vérifier les permissions
- [ ] Signer l'APK avec votre clé
- [ ] Tester les fonctionnalités natives
- [ ] Optimiser la taille de l'APK
- [ ] Ajouter les icônes et splash screens

## 🌐 Alternative : Application Web Progressive (PWA)

Si vous préférez une solution plus simple :
1. Ajouter un manifest.json
2. Activer le service worker
3. Publier sur un serveur HTTPS
4. Les utilisateurs peuvent "installer" l'app depuis leur navigateur

Votre application Flask est déjà prête avec son design responsive !