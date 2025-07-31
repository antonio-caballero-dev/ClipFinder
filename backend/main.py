

# FastAPI application 
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
import shutil
import os
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from src.video_utils import *
from src.video_utils import extract_thumbnail
from src.whisper_utils import *
from src.embeddings_utils import *
from src.search_utils import *
import torch
import glob
import json
import numpy as np

app = FastAPI()


# Servir archivos estáticos de video_data

# Servir archivos estáticos de video_data y clips
app.mount("/video_data", StaticFiles(directory="video_data"), name="video_data")
app.mount("/clips", StaticFiles(directory="clips"), name="clips")
app.mount("/thumbnails", StaticFiles(directory="thumbnails"), name="thumbnails")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la FastAPI de ClipFinder!"}

# Variable global para almacenar el modelo Whisper cargado
whisper_model_instance = "small"
device = "cuda" if torch.cuda.is_available() else "cpu"

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    try:
        os.makedirs("video_data", exist_ok=True)
        os.makedirs("thumbnails", exist_ok=True)
        
        # Guardar el archivo original con un nombre temporal único
        temp_file_location = f"video_data/temp_{file.filename}"
        with open(temp_file_location, "wb") as buffer:
            buffer.write(await file.read())

        # Nombre final del archivo mp4 convertido
        mp4_filename = os.path.splitext(file.filename)[0] + ".mp4"
        mp4_file_location = f"video_data/{mp4_filename}"

        ext = os.path.splitext(file.filename)[1].lower()
        if ext == ".mp4":
            # Si ya es mp4, solo renombrar/mover el archivo
            os.rename(temp_file_location, mp4_file_location)
        else:
            # Convertir a mp4 (H.264)
            convert_to_h264(temp_file_location, mp4_file_location)
            os.remove(temp_file_location)

   

        # Crear directorios necesarios si no existen
        os.makedirs("audio", exist_ok=True)
        os.makedirs("transcripts", exist_ok=True)
        os.makedirs("embeddings", exist_ok=True)

        # Extraer audio
        audio_file_location = f"audio/{os.path.splitext(mp4_filename)[0]}.wav"
        extract_audio(mp4_file_location, audio_file_location)
        print(f"Audio guardado en: {audio_file_location}")

        # Transcribir el audio usando Whisper
        trabscription_file_location = f"transcripts/{os.path.splitext(mp4_filename)[0]}_transcript.json"
        whisper_model = load_whisper_model(whisper_model_instance, device)
        segments = transcribe_audio(whisper_model, audio_file_location)
        save_transcript(segments, trabscription_file_location)
        print(f"Transcripción guardada en: {trabscription_file_location}")
        del whisper_model  # Liberar memoria del modelo

        # Generar embeddings del audio
        embeddings_file_location = f"embeddings/{os.path.splitext(mp4_filename)[0]}_embeddings"
        embeddings_model = load_embedding_model()
        audio_embeddings = embed_texts(embeddings_model, [segment['text'] for segment in segments])
        save_embeddings(audio_embeddings, embeddings_file_location)
        print(f"Embeddings guardados en: {embeddings_file_location}")
        del embeddings_model  # Liberar memoria del modelo

        torch.cuda.empty_cache()  # Limpiar caché de CUDA




        return JSONResponse(
            content={
                "filename": mp4_filename,
                "video_url": f"/video_data/{mp4_filename}",
                "audio_file": os.path.basename(audio_file_location),
                "audio_url": f"/audio/{os.path.basename(audio_file_location)}",
                "transcript_file": os.path.basename(trabscription_file_location),
                "transcript_url": f"/transcripts/{os.path.basename(trabscription_file_location)}",
                "embeddings_file": os.path.basename(embeddings_file_location),
                "embeddings_url": f"/embeddings/{os.path.basename(embeddings_file_location)}",
                "message": "Video subido y procesado exitosamente!"
            },
            status_code=200
        )
    except Exception as e:
        import traceback
        print('ERROR EN /upload-video/')
        traceback.print_exc()
        return JSONResponse(content={"error": str(e), "trace": traceback.format_exc()}, status_code=500)
    
@app.get("/videos_disponibles/")
async def get_videos_disponibles():
    try:
        video_files = [f for f in os.listdir("video_data") if f.endswith(('.mp4', '.avi', '.mov'))]
        return JSONResponse(content={"videos": video_files}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



# Endpoint para consultar el estado de procesamiento de un video
@app.get("/video_status/{nombre}")
async def video_status(nombre: str):
    audio_path = os.path.join("audio", f"{nombre}.wav")
    transcript_path = os.path.join("transcripts", f"{nombre}_transcript.json")
    # Puede ser .pt o sin extensión, revisamos ambos
    embeddings_path_pt = os.path.join("embeddings", f"{nombre}_embeddings.npy")
    embeddings_path = os.path.join("embeddings", f"{nombre}_embeddings")
    return JSONResponse(content={
        "audio": os.path.exists(audio_path),
        "transcript": os.path.exists(transcript_path),
        "embeddings": os.path.exists(embeddings_path_pt) or os.path.exists(embeddings_path)
    })




# Variable global para el embeddings cargado y el nombre del video
current_embeddings = None
current_embeddings_video = None

@app.get("/video/{video_name}")
async def get_video(video_name: str):
    file_path = os.path.join("video_data", video_name)
    ext = os.path.splitext(video_name)[1].lower()
    if ext != ".mp4":
        return JSONResponse(content={"error": "Formato de video inadecuado. Solo se aceptan archivos .mp4"}, status_code=400)
    if not os.path.exists(file_path):
        return JSONResponse(content={"error": "Video no encontrado"}, status_code=404)


    # Cargar solo el embeddings .npy del video actual en memoria
    global current_embeddings, current_embeddings_video
    nombre_sin_ext = os.path.splitext(video_name)[0]
    embeddings_path_npy = os.path.join("embeddings", f"{nombre_sin_ext}_embeddings.npy")
    if os.path.exists(embeddings_path_npy):
        import numpy as np
        current_embeddings = np.load(embeddings_path_npy, allow_pickle=True)
        current_embeddings_video = video_name
        print(f"Embeddings cargados en memoria para {video_name}")
    else:
        current_embeddings = None
        current_embeddings_video = None
        print(f"No se encontraron embeddings para {video_name}")

    return FileResponse(file_path, media_type="video/mp4")

@app.post("/preprocess-video/{video_name}")
async def preprocess_video(video_name: str):
    try:
        video_path = os.path.join("video_data", video_name)
        if not os.path.exists(video_path):
            return JSONResponse(content={"error": "Video no encontrado"}, status_code=404)
            # Extraer audio solo si no existe
        audio_file_location = f"audio/{os.path.splitext(video_name)[0]}.wav"
        if not os.path.exists(audio_file_location):
            extract_audio(video_path, audio_file_location)

        # Transcribir el audio usando Whisper solo si no existe
        trabscription_file_location = f"transcripts/{os.path.splitext(video_name)[0]}_transcript.json"
        if not os.path.exists(trabscription_file_location):
            whisper_model = load_whisper_model(whisper_model_instance, device)
            segments = transcribe_audio(whisper_model, audio_file_location)
            save_transcript(segments, trabscription_file_location)
            del whisper_model  # Liberar memoria del modelo
        else:
            segments = load_transcript(trabscription_file_location)
            print(f"Transcripción cargada desde: {trabscription_file_location}")
  
        # Generar embeddings del audio solo si no existe
        embeddings_file_location = f"embeddings/{os.path.splitext(video_name)[0]}_embeddings.npy"
        if not os.path.exists(embeddings_file_location):
            embeddings_model = load_embedding_model()
            audio_embeddings = embed_texts(embeddings_model, [segment['text'] for segment in segments])
            save_embeddings(audio_embeddings, embeddings_file_location)
            del embeddings_model  # Liberar memoria del modelo  

        torch.cuda.empty_cache()  # Limpiar caché de CUDA 

        # Cargar en memoria el embeddings generado
        global current_embeddings, current_embeddings_video
        if os.path.exists(embeddings_file_location):
            import numpy as np
            current_embeddings = np.load(embeddings_file_location, allow_pickle=True)
            current_embeddings_video = video_name
            print(f"Embeddings cargados en memoria para {video_name} tras preprocesado")
        else:
            current_embeddings = None
            current_embeddings_video = None
            print(f"No se encontraron embeddings para {video_name} tras preprocesado")

        return JSONResponse(
            content={
                "message": "Video preprocesado exitosamente!",
                "audio_file": os.path.basename(audio_file_location),
                "transcript_file": os.path.basename(trabscription_file_location),
                "embeddings_file": os.path.basename(embeddings_file_location)
            },
            status_code=200
        )
    except Exception as e:
        import traceback
        print('ERROR EN /preprocess_video/')
        traceback.print_exc()
        return JSONResponse(content={"error": str(e), "trace": traceback.format_exc()}, status_code=500)




 # Endpoint POST para búsqueda y generación de clips y metadatos
@app.post("/video_search/{video_name}")
async def video_search(video_name: str, request: Request):
    try:
        data = await request.json()
        query = data.get("query", "")
        top_k = int(data.get("top_k", 5))
        clip_length = float(data.get("clip_length", 30.0))

        global current_embeddings, current_embeddings_video
        # Cargar embeddings si no están en memoria
        if current_embeddings is None or current_embeddings_video != video_name:
            nombre_sin_ext = os.path.splitext(video_name)[0]
            embeddings_path = os.path.join("embeddings", f"{nombre_sin_ext}_embeddings.npy")
            if not (os.path.exists(os.path.join("video_data", video_name)) and os.path.exists(embeddings_path)):
                return JSONResponse(content={"error": "Video o embeddings no encontrados"}, status_code=404)
            current_embeddings = np.load(embeddings_path, allow_pickle=True)
            current_embeddings_video = video_name

        # Limpiar clips y thumbnails previos
        clip_base = os.path.splitext(video_name)[0]
        for f in glob.glob(os.path.join("clips", f"{clip_base}_clip_*.mp4")):
            os.remove(f)
        for f in glob.glob(os.path.join("thumbnails", f"{clip_base}_clip_*.jpg")):
            os.remove(f)

        # Cargar modelos y segmentos
        embeddings_model = load_embedding_model()
        transcript_path = os.path.join("transcripts", f"{clip_base}_transcript.json")
        segments = load_transcript(transcript_path)

        # Buscar clips relevantes
        results = search_clips(
            query=query,
            model=embeddings_model,
            embeddings=current_embeddings,
            segments=segments,
            top_k=top_k,
            clip_length=clip_length
        )

        metadatos = []
        os.makedirs("thumbnails", exist_ok=True)
        for idx, result in enumerate(results):
            start, end = float(result['start']), float(result['end'])
            clip_filename = f"clip_{idx}.mp4"
            clip_path = os.path.join("clips", clip_filename)
            thumbnail_filename = f"clip_{idx}.jpg"
            thumbnail_path = os.path.join("thumbnails", thumbnail_filename)

            extract_clip(
                video_path=os.path.join("video_data", video_name),
                start_time=start,
                end_time=end,
                output_clip_dir_path="clips",
                clip_id=idx,
                query_id=0
            )

            # Generar thumbnail
            try:
                extract_thumbnail(clip_path, thumbnail_path)
                thumbnail_url = f"/thumbnails/{thumbnail_filename}"
            except Exception as thumb_exc:
                print(f"No se pudo generar thumbnail para {clip_path}: {thumb_exc}")
                thumbnail_url = None

            meta = {k: str(v) for k, v in result.items()}
            meta.update({
                "clip_url": f"/clips/{clip_filename}",
                "clip_id": str(idx),
                "thumbnail_url": thumbnail_url
            })
            metadatos.append(meta)

        # Guardar metadatos
        metadatos_path = os.path.join("clips", f"{clip_base}_clips_metadata.json")
        with open(metadatos_path, "w", encoding="utf-8") as f:
            json.dump(metadatos, f, ensure_ascii=False, indent=2)

        return JSONResponse(content={"results": metadatos}, status_code=200)

    except Exception as e:
        import traceback
        print('ERROR EN /video_search/')
        traceback.print_exc()
        return JSONResponse(content={"error": str(e), "trace": traceback.format_exc()}, status_code=500)
    


 # Endpoint GET para obtener los metadatos de los clips generados (estructura plana)
@app.get("/clips_metadata/{video_base}")
async def get_clips_metadata(video_base: str):
    metadatos_path = os.path.join("clips", f"{video_base}_clips_metadata.json")
    if not os.path.exists(metadatos_path):
        return JSONResponse(content={"error": "No existen metadatos para este video."}, status_code=404)
    import json
    with open(metadatos_path, "r", encoding="utf-8") as f:
        metadatos = json.load(f)
    return JSONResponse(content={"results": metadatos}, status_code=200)
    
@app.get("/clips/{video_base}_clip_{clip_id}.mp4")
async def get_clip(video_base: str, clip_id: int):
    clip_path = os.path.join("clips", f"{video_base}_clip_{clip_id}.mp4")
    if not os.path.exists(clip_path):
        return JSONResponse(content={"error": "Clip no encontrado"}, status_code=404)
    return FileResponse(clip_path, media_type="video/mp4")


## No es necesario un endpoint para thumbnails individuales, se sirven como archivos estáticos en /thumbnails/{video_base}_clip_{clip_id}.jpg

