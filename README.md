# ClipFinder

## Descripción (Español)
ClipFinder es una aplicación web que permite buscar y extraer clips relevantes de videos largos a partir de consultas en lenguaje natural. Utiliza modelos de transcripción automática (Whisper) y embeddings semánticos para localizar los fragmentos más relevantes según la consulta del usuario.

## Description (English)
ClipFinder is a web application that allows you to search and extract relevant clips from long videos using natural language queries. It leverages automatic transcription (Whisper) and semantic embeddings to find the most relevant segments according to the user's query.

---

## Características principales / Main Features
- Subida y procesamiento automático de videos (audio, transcripción, embeddings)
- Búsqueda semántica de fragmentos mediante texto libre
- Generación automática de clips de video y miniaturas
- Interfaz web interactiva (React + Vite)
- Backend API con FastAPI

---

## Instalación / Installation

### Requisitos / Requirements
- Python 3.10 (recomendado usar conda)
- Node.js >= 18
- ffmpeg

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
1. Sube un video desde la interfaz web.
2. Espera a que se procese (transcripción y embeddings).
3. Realiza una consulta en lenguaje natural para buscar fragmentos relevantes.
4. Visualiza y descarga los clips generados.

---

## Estructura del proyecto / Project Structure
```
ClipFinder/
├── backend/         # Backend FastAPI, procesamiento de video/audio
├── frontend/        # Frontend React + Vite
├── src/             # Utilidades de procesamiento (usadas por backend)
├── video_data/      # Videos originales
├── audio/           # Audios extraídos
├── transcripts/     # Transcripciones generadas
├── embeddings/      # Embeddings generados
├── clips/           # Clips de video generados
├── thumbnails/      # Miniaturas de clips
```

---

## Dependencias principales / Main Dependencies
- [FastAPI](https://fastapi.tiangolo.com/)
- [moviepy](https://zulko.github.io/moviepy/)
- [openai-whisper](https://github.com/openai/whisper)
- [sentence-transformers](https://www.sbert.net/)
- [React](https://react.dev/)
- [Vite](https://vitejs.dev/)

---

## Atribuciones / Attributions
- Escuela de Ingeniería y Arquitectura (EINA) de la Universidad de Zaragoza, CC BY 3.0, vía Wikimedia Commons. Video: Atenea_EINA_267

---

## Licencia / License
Este proyecto se distribuye sin licencia explícita. Consulta con el autor para usos comerciales o de investigación.

---

## Autor / Author
Antonio Caballero
- [LinkedIn](www.linkedin.com/in/antonio-caballero-carrasco)
