import whisper
from src.config import WHISPER_MODELS_DIR, TRANSCRIPTS_DIR

import json

def load_whisper_model(model_size: str = "small", device: str = "cpu"):
    """
    Carga el modelo Whisper especificado, usando el directorio local para modelos.
    """
    print(f"Cargando modelo Whisper '{model_size}' en dispositivo '{device}'...")
    return whisper.load_model(model_size, device=device, download_root=WHISPER_MODELS_DIR)

def transcribe_audio(model, audio_path: str, language: str = "es"):
    """
    Transcribe el audio con Whisper, devolviendo los segmentos con timestamps en segundos.
    """
    print(f"Transcribiendo audio: {audio_path}...")
    result = model.transcribe(audio_path, language=language)
    print(f"Transcripción completada.\n")
    return result.get('segments', [])

def save_transcript(segments, output_path: str):
    """
    Guarda la transcripción segmentada en un archivo JSON.
    """
    print(f"Guardando transcripción en: {output_path}...\n")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"Transcripción guardada correctamente.\n")

def load_transcript(input_path: str):
    """
    Carga la transcripción desde un archivo JSON.
    """
    print(f"Cargando transcripción desde: {input_path}...\n")
    with open(input_path, 'r', encoding='utf-8') as f:
        segments = json.load(f)
    print(f"Transcripción cargada correctamente.\n")
    return segments