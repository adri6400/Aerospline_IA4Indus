import streamlit as st
import os
from pathlib import Path
import json
from PIL import Image


# Titre de l'application
col1, col2 = st.columns(2)
with col1:
    st.image("aerospline.png", width=200)  # Remplacez "logo1.png" par le chemin de votre premier logo
with col2:
    st.image("ai4industry.png", width=200)  # Remplacez "logo2.png" par le chemin de votre second logo

st.title("Résumé de réunion avec reconnaissance vocale")

# Section 1 : Sélection de l'audio principal
st.header("Fichier audio principal")
default_audio = "echantillon.wav"

# Vérifier si le fichier par défaut existe
if os.path.exists(default_audio):
    st.success(f"Fichier audio par défaut trouvé : `{default_audio}`")
else:
    st.warning(f"Le fichier audio par défaut `{default_audio}` est introuvable.")

# Permettre à l'utilisateur de changer l'audio principal
uploaded_main_audio = st.file_uploader(
    "Téléchargez un fichier audio principal (WAV format préféré)", 
    type=["wav", "mp3"], 
    key="main_audio"
)

if uploaded_main_audio:
    # Sauvegarder le nouveau fichier principal
    with open(uploaded_main_audio.name, "wb") as f:
        f.write(uploaded_main_audio.getbuffer())
    st.success(f"Fichier audio principal mis à jour : `{uploaded_main_audio.name}`")
    main_audio_path = uploaded_main_audio.name
else:
    main_audio_path = default_audio

# Lecture de l'audio principal
if os.path.exists(main_audio_path):
    st.audio(main_audio_path, format="audio/wav")

# Section 2 : Gestion des fichiers d'entraînement pour les participants
st.header("Voix des participants")
participants_dir = Path("res_format")
participants_dir.mkdir(exist_ok=True)  # Crée le dossier s'il n'existe pas

# Ajouter des fichiers audio pour les participants
st.subheader("Ajouter une voix")
uploaded_participant_audio = st.file_uploader(
    "Téléchargez un fichier audio pour un participant (WAV format préféré)", 
    type=["wav", "mp3"], 
    key="participant_audio"
)

if uploaded_participant_audio:
    # Sauvegarder le fichier audio dans le dossier des participants
    file_path = participants_dir / uploaded_participant_audio.name
    with open(file_path, "wb") as f:
        f.write(uploaded_participant_audio.getbuffer())
    st.success(f"Fichier audio ajouté pour le participant : `{uploaded_participant_audio.name}`")

# Toggle button to show/hide participants
if "show_participants" not in st.session_state:
    st.session_state.show_participants = False

if st.button("Afficher/Cacher les voix des participants"):
    st.session_state.show_participants = not st.session_state.show_participants

if st.session_state.show_participants:
    # Afficher et gérer les fichiers des participants
    st.subheader("Gérer les voix des participants")
    participant_files = list(participants_dir.glob("*.wav"))

    if participant_files:
        for file in participant_files:
            with st.expander(f"Participant : {file.stem}"):
                st.audio(str(file), format="audio/wav")
                
                # Option pour supprimer le fichier
                if st.button(f"Supprimer {file.stem}", key=f"delete_{file.stem}"):
                    file.unlink()  # Supprimer le fichier
                    st.warning(f"Fichier supprimé : {file.stem}")
                    st.experimental_rerun()  # Recharger l'application pour refléter le changement
    else:
        st.info("Aucun fichier audio de participant n'est présent. Ajoutez-en ci-dessus.")

# Section 4 : Diarization/Transcription
st.header("Diarization/Transcription")
if "show_transcription" not in st.session_state:
    st.session_state.show_transcription = False

if st.button("Afficher/Cacher la transcription"):
    st.session_state.show_transcription = not st.session_state.show_transcription

if st.session_state.show_transcription:
    transcription_file = "resultat/aerospline_transcription.json"
    if os.path.exists(transcription_file):
        with open(transcription_file, "r") as f:
            transcription_data = json.load(f)
        st.json(transcription_data)
        st.download_button(
            label="Télécharger la transcription au format json",
            data=json.dumps(transcription_data),
            file_name="transcription.json",
            mime="application/json"
        )
    else:
        st.error(f"Le fichier `{transcription_file}` est introuvable.")

# Section 3 : Bouton pour générer le résumé
st.header("Générer un résumé de la réunion")
if st.button("Générer le résumé"):
    if not os.path.exists(main_audio_path):
        st.error("Aucun fichier audio principal n'a été trouvé ! Veuillez en téléverser un.")
    else:
        # Exemple : Exécuter un script de traitement (remplacez cette section par votre code réel)

        # Simuler l'analyse et le résumé
        st.success("Résumé généré avec succès !")

        # Afficher le résumé (vous pouvez remplacer par vos propres données)
        

        # Lire et afficher le contenu de resume.md
        resume_file = "resultat/resume.md"
        if os.path.exists(resume_file):
            with open(resume_file, "r") as f:
                resume_content = f.read()
            st.markdown(resume_content)
        else:
            st.error(f"Le fichier `{resume_file}` est introuvable.")

        # Option pour télécharger le fichier résumé
        st.download_button(
            label="Télécharger le résumé au format texte",
            data=resume_content,
            file_name="resumé.txt",
            mime="text/plain"
        )
def resize_image(image_path, size=(200, 135)):
    img = Image.open(image_path)
    img = img.resize(size)
    return img


st.sidebar.markdown("<h1 style='font-size: 50px;'>Formations</h1>", unsafe_allow_html=True)

st.sidebar.image(resize_image("cytech.png"), width=200)
st.sidebar.image(resize_image("cesi.png"), width=200)
st.sidebar.image(resize_image("univrochelle.png", (200,200)), width=200)


