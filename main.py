import streamlit as st
import yt_dlp
from faster_whisper import WhisperModel
import os

st.title("🎙️ Transcritor Online Grátis")

url = st.text_input("Cole o link do YouTube:")

if st.button("Transcrever"):
    if url:
        try:
            with st.spinner("Processando... aguarde."):
                # Download
                ydl_opts = {'format': 'm4a/bestaudio', 'outtmpl': 'audio.m4a', 'overwrites': True}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # Na nuvem tem que ser CPU e INT8 (Regra do servidor gratis)
                model = WhisperModel("tiny", device="cpu", compute_type="int8")
                segments, _ = model.transcribe("audio.m4a")

                texto = " ".join([s.text.strip() for s in segments])

            st.success("Pronto!")
            st.text_area("Resultado:", texto, height=300)
        except Exception as e:
            st.error(f"Erro: {e}")
