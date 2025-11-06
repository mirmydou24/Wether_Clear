#!/bin/bash

echo "=================================================="
echo "🌤️  INSTALLATION DE WEATHER ASSISTANT"
echo "=================================================="

#  Mise à jour des paquets et installation des dépendances
echo " Mise à jour et installation des paquets système requis..."
sudo apt update
sudo apt install -y python3-venv python3-pip ffmpeg alsa-utils portaudio19-dev espeak flac libasound2-dev

#  Vérification et création de l'environnement virtuel
if [ ! -d "venv" ]; then
    echo " Création de l'environnement virtuel..."
    python3 -m venv venv
fi

#  Activation de l'environnement virtuel
echo " Activation de l'environnement virtuel..."
source venv/bin/activate

#  Installation des bibliothèques Python
echo " Installation des bibliothèques Python..."
pip install --upgrade pip
pip install --no-cache-dir requests flask speechrecognition pyttsx3 pynput keyboard pyaudio

#  Configuration audio
echo " Configuration audio (sortie sur Jack)..."
if ! amixer > /dev/null 2>&1; then
    echo " Erreur : ALSA ne trouve pas de périphérique audio."
else
    echo " Audio configuré avec succès !"
fi

# ✅ Installation terminée !
echo " Installation terminée !"
echo " Exécution de weather_clear.py..."
sudo bash -c "source venv/bin/activate && python3 weather_clear.py"
