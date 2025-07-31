

import subprocess
import os

from src.config import AUDIO_DIR, CLIP_DATA_DIR
import cv2

def convert_to_h264(input_path: str, output_path: str) -> None:
    """
    Convierte un video a formato MP4 con códec H.264 (libx264) y audio AAC.
    """
    print(f"Convirtiendo {input_path} a H.264 MP4...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        str(output_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Video convertido y guardado en {output_path}\n")


def extract_audio(video_path: str, output_audio_path: str = None) -> None:


    if output_audio_path is None:
        _baseName = os.path.basename(video_path)
        output_audio_path = os.path.join(AUDIO_DIR, f"{os.path.splitext(_baseName)[0]}.wav")
    print(f"Extrayendo audio de {video_path}...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le",
        "-ar", "16000", "-ac", "1",
        str(output_audio_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Audio extraído y guardado en {output_audio_path}\n")

def extract_clip(video_path: str,
                 start_time: float,
                 end_time: float,
                 output_clip_dir_path: str,
                 clip_id: int = 0,
                 query_id: int = 0) -> None:
    """
        Extrae un clip de video entre start_time y end_time usando códec H.264 (libx264).
        """
    print(f"Extrayendo clip de {start_time} a {end_time} segundos...")

    # Guardar el clip exactamente en clips/{video_name}/clip_{clip_id}.mp4
    os.makedirs(output_clip_dir_path, exist_ok=True)
    output_clip_path = os.path.join(output_clip_dir_path, f"clip_{clip_id}.mp4")
    subprocess.run([
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-to", str(end_time),
        "-i", str(video_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-avoid_negative_ts", "make_zero",
        str(output_clip_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Clip guardado en {output_clip_path}\n")


def extract_thumbnail(video_path: str, thumbnail_path: str) -> None:
    """
    Extrae el primer fotograma de un video y lo guarda como imagen.
    """
    import cv2
    print(f"Extrayendo miniatura de {video_path}...")
    try:
        vidcap = cv2.VideoCapture(video_path)
        success, image = vidcap.read()
        if success:
            cv2.imwrite(thumbnail_path, image)
            print(f"Miniatura guardada en {thumbnail_path}\n")
        else:
            print(f"No se pudo extraer el fotograma de {video_path}")
    except Exception as e:
        print(f"Error extrayendo miniatura: {e}")