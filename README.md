
# 🎬 ClipFinder

## Descripción (Español)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" />
  <img src="https://img.shields.io/badge/Node.js-18+-green?logo=node.js" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" />
</p>

ClipFinder es una aplicación web que permite buscar y extraer clips relevantes de videos largos a partir de consultas en lenguaje natural. Utiliza modelos de transcripción automática (Whisper) y embeddings semánticos para localizar los fragmentos más relevantes según la consulta del usuario. La idea está inspirada en el funcionamiento del juego [Her Story](https://www.herstorygame.com/).

> [!NOTE]
> Para generar transcripciones y embeddings de forma eficiente, se recomienda disponer de una GPU compatible con CUDA. El sistema está ajustado y probado principalmente para vídeos en español.

## Description (English)
ClipFinder is a web application that allows you to search and extract relevant clips from long videos using natural language queries. It leverages automatic transcription (Whisper) and semantic embeddings to find the most relevant segments according to the user's query. The idea is inspired by the mechanics of the game [Her Story](https://www.herstorygame.com/).

 > [!NOTE]
> For efficient transcription and embedding generation, a CUDA-compatible GPU is recommended. The system is tuned and tested mainly for Spanish-language videos.

---

## Características principales / Main Features
- 🚀 Subida y procesamiento automático de videos (audio, transcripción, embeddings)
- 🔎 Búsqueda semántica de fragmentos mediante texto libre
- ✂️ Generación automática de clips de video y miniaturas
- 🖥️ Interfaz web interactiva (React + Vite)
- ⚡ Backend API con FastAPI

---

## Instalación / Installation


### ⚙️ Requisitos / Requirements
- 🐍 Python 3.10 (recomendado usar conda)
- 🟩 Node.js >= 18
- 🎞️ ffmpeg

### Backend
```bash
# Crear entorno (opcional)
conda env create -f clipFinderEnv.yml
conda activate clipFinderEnv
# Instalar dependencias
pip install -r requirements.txt
# Ejecutar backend
cd backend
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

La aplicación web estará disponible en `http://localhost:5173` y el backend en `http://localhost:8000`.

---

## Uso / Usage
1. 📤 Sube un video desde la interfaz web.
2. ⏳ Espera a que se procese (transcripción y embeddings).
3. 💬 Realiza una consulta en lenguaje natural para buscar fragmentos relevantes.
4. 🎬 Visualiza y descarga los clips generados.

---



## Modelos / Models
- 📝 **Transcripción:** [Whisper Small](https://huggingface.co/openai/whisper-small)
- 🧠 **Embeddings:** [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)

---

## Dependencias principales / Main Dependencies
- ⚡ [FastAPI](https://fastapi.tiangolo.com/)
- 🎞️ [moviepy](https://zulko.github.io/moviepy/)
- 📝 [openai-whisper](https://github.com/openai/whisper)
- 🧠 [sentence-transformers](https://www.sbert.net/)
- ⚛️ [React](https://react.dev/)
- 🟣 [Vite](https://vitejs.dev/)

---

## Atribuciones / Attributions
- 🎥 El video "Atenea_EINA_267" de la Escuela de Ingeniería y Arquitectura (EINA) de la Universidad de Zaragoza, CC BY 3.0, vía Wikimedia Commons, se utiliza únicamente como ejemplo demostrativo en esta aplicación.


## Video demostrativo / Demo Video

<p align="center">
  <b>🎦 Aquí puedes ver un video demostrativo del funcionamiento de ClipFinder:</b><br><br>
  <a href="https://youtu.be/v4nJRlXDQG4" target="_blank">
    <img src="https://img.youtube.com/vi/v4nJRlXDQG4/0.jpg" alt="Demo de ClipFinder" width="480"/>
  </a>
</p>

---
## Licencia / License
Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

---

## Autor / Author
Antonio Caballero  
[<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="30" alt="LinkedIn"/>](https://www.linkedin.com/in/antoniocaballerocarrasco)
