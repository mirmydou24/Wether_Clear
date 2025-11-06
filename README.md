# 🌤️ Weather Clear

**Weather Clear** est un assistant vocal météo intelligent conçu pour **Raspberry Pi**.  
Il combine une **interface web intuitive** avec un **assistant vocal** capable d’écouter et de répondre à des questions sur la météo en temps réel.

---

## 🧠 Présentation du projet

Ce projet a été réalisé dans le cadre d’un **cours d’anglais**, avec pour objectif de créer une application pratique et interactive, fonctionnant **en local sur Raspberry Pi**.

Weather Clear récupère les données météo via une API en ligne, les affiche sur une interface web moderne et permet à l’utilisateur d’interagir par **commande vocale** pour poser des questions comme :

- “What’s the temperature today?”  
- “Is it going to rain?”  
- “What should I wear today?”  
- “How strong is the wind?”

---

## ⚙️ Fonctionnalités principales

- 🌍 **Affichage en temps réel** des données météo (température, humidité, vent, pression, précipitations)  
- 🎤 **Reconnaissance vocale** avec retour audio grâce à `speech_recognition` et `pyttsx3`  
- 💬 **Assistant vocal intelligent** capable de comprendre et formuler des réponses naturelles  
- 💻 **Interface web interactive** via **Flask**, accessible depuis n’importe quel appareil du réseau local  
- 🔁 **Mise à jour automatique** des données météo toutes les 10 minutes  
- 🧠 **Analyse sémantique basique** pour adapter les réponses aux questions posées  

---

## 🧩 Technologies utilisées

| Catégorie | Outils / Librairies |
|------------|--------------------|
| **Langage principal** | Python 3 |
| **Framework web** | Flask |
| **Reconnaissance vocale** | SpeechRecognition |
| **Synthèse vocale** | Pyttsx3 |
| **Audio / Microphone** | PyAudio, ALSA |
| **Appels API** | Requests |
| **Interface** | HTML + CSS (intégré dans Flask) |
| **Matériel cible** | Raspberry Pi (3 B ou supérieur) |

---

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/<ton-utilisateur>/WeatherClear.git
cd WeatherClear
```

### 2. Lancer le script d’installation automatique
```bash
bash Setup_WeatherClear.sh
```

Ce script :
- Met à jour le système  
- Installe toutes les dépendances nécessaires  
- Configure l’environnement virtuel Python  
- Lance automatiquement le serveur Flask  

---

## 🖥️ Utilisation

Une fois l’installation terminée, le script démarre automatiquement le serveur.  
L’application sera accessible à l’adresse suivante :

👉 **http://localhost:5000**  
(ou depuis un autre appareil du réseau via l’IP du Raspberry Pi)

Sur la page web :
- Consulte la météo en temps réel  
- Clique sur **🎤 Ask about weather** pour poser ta question vocalement  
- L’assistant répondra directement à voix haute et affichera sa réponse sur la page

---

## 🧠 Exemple de dialogue

**Utilisateur :** “What should I wear today?”  
**Assistant :** “It’s cool. I recommend wearing a light jacket and a sweater.”  

**Utilisateur :** “Is it going to rain?”  
**Assistant :** “There is no precipitation at the moment.”

---

## ⚠️ Configuration

Dans le fichier `weather_clear.py`, veille à remplacer la clé API :

```python
API_KEY = "ea492956c0a146f9991165325250902"  # Remplace par ta clé personnelle
```

Obtiens une clé gratuite sur :  
🔗 [https://www.weatherapi.com](https://www.weatherapi.com)

---

## 🧰 Structure du projet

```
WeatherClear/
├── weather_clear.py         # Application principale (Flask + Voice Assistant)
├── Setup_WeatherClear.sh    # Script d’installation et de lancement
├── venv/                    # Environnement virtuel (créé automatiquement)
└── README.md                # Documentation
```

---

## 👨‍💻 Auteur

Projet réalisé par **Maxime** dans le cadre d’un **cours d’anglais**.  
Étudiant en **BUT Informatique**, passionné par les solutions innovantes et le développement sur Raspberry Pi.  

---

## 📄 Licence

Ce projet est distribué sous licence **MIT** — vous êtes libre de l’utiliser, le modifier et le partager à des fins éducatives ou personnelles.
