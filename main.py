import streamlit as st
import yt_dlp
from faster_whisper import WhisperModel

st.set_page_config(page_title="Transcritor Online", page_icon="🎙️")
st.title("🎙️ Transcritor Online Grátis")

url = st.text_input("Cole o link do YouTube:")

if st.button("Transcrever"):
    if not url:
        st.warning("Por favor, cole um link válido.")
    else:
        try:
            with st.spinner("Baixando áudio e processando... Isso pode levar alguns minutos."):
                # Configuração para tentar burlar o bloqueio 403 do YouTube
                ydl_opts = {
                    'format': 'm4a/bestaudio',
                    'outtmpl': 'audio.m4a',
                    'overwrites': True,
                    'nocheckcertificate': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # Modelo Tiny para ser rápido na CPU do servidor
                model = WhisperModel("tiny", device="cpu", compute_type="int8")
                segments, _ = model.transcribe("audio.m4a")
                
                texto_final = ""
                for segment in segments:
                    texto_final += segment.text + " "
                
                st.success("Transcrição concluída!")
                st.text_area("Resultado:", texto_final, height=300)
                st.download_button("Baixar Texto", texto_final, file_name="transcricao.txt")
        except Exception as e:
            st.error(f"Erro ao processar: {str(e)}")
            st.info("Dica: Se o erro for '403 Forbidden', o YouTube bloqueou o servidor. Tente novamente em alguns minutos ou com outro link.")
