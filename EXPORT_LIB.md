# Exportation et Installation de Paquets Poetry en Mode Hors Ligne

Ce guide explique comment exporter les paquets Python gérés par Poetry dans un fichier ZIP, puis comment installer ces paquets sur une machine virtuelle (VM) sans accès Internet.

## Étape 1 : Exporter les Dépendances avec Poetry

Tout d'abord, assurez-vous d'avoir Poetry installé dans votre environnement de développement. Ensuite, exportez les dépendances de votre projet dans un fichier `requirements.txt` :

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

Cette commande génère un fichier `requirements.txt` contenant toutes les dépendances de votre projet.

## Étape 2 : Télécharger les Paquets

Créez un dossier pour stocker les fichiers de paquets téléchargés, puis utilisez pip pour télécharger les dépendances :

```bash
pip download -r requirements.txt -d ./dossier_paquets
```

Remplacez `./dossier_paquets` par le chemin du dossier de destination pour les fichiers téléchargés.

## Étape 3 : Compresser le Dossier des Paquets

Compressez le dossier contenant les paquets téléchargés en un fichier ZIP pour faciliter le transfert :

Sous Linux/macOS :

```bash
zip -r dossier_paquets.zip dossier_paquets/
```

## Étape 4 : Transférer le Fichier ZIP sur la VM

Transférez le fichier ZIP contenant les paquets sur votre machine virtuelle .

## Étape 5 : Activer l'Environnement Virtuel Python sur la VM

Avant d'installer les paquets, il est crucial d'activer l'environnement virtuel Python. Voici comment vous pouvez activer votre environnement virtuel selon votre système d'exploitation :


```bash
source nom_environnement/bin/activate
```


Remplacez `nom_environnement` par le nom de votre environnement virtuel. Ceci garantit que les paquets seront installés dans l'environnement virtuel plutôt que globalement.

Sur votre VM, décompressez le fichier ZIP pour extraire les paquets. Puis, installez les paquets en utilisant pip en mode hors ligne :

```bash
pip install --no-index --find-links=./dossier_paquets -r requirements.txt
```

Assurez-vous de remplacer `./dossier_paquets` par le chemin vers le dossier contenant les paquets sur votre VM.

En suivant ces instructions, vous pourrez installer vos dépendances Poetry sur une VM sans nécessiter une connexion Internet.
## Étape 7 : Activer l'Environnement Virtuel Python sur la VM


Remplacez `nom_environnement` par le nom de votre environnement virtuel. Une fois activé, vous pouvez commencer à utiliser les paquets installés dans votre projet.