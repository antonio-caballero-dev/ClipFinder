from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()

AUDIO_DIR = PROJECT_ROOT / "audio"
EMBEDDINGS_DIR = PROJECT_ROOT / "embeddings"
LOGS_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = PROJECT_ROOT / "models"
WHISPER_MODELS_DIR = MODELS_DIR / "whisper_models"
SENTENCE_TRANSFORMERS_DIR = MODELS_DIR / "sentence_transformers"

VIDEO_DATA_DIR = PROJECT_ROOT / "video_data"
TRANSCRIPTS_DIR = PROJECT_ROOT / "transcripts"

CLIP_DATA_DIR = PROJECT_ROOT / "clips"