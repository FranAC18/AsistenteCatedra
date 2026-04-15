"""
speech_to_text.py
Transcribe audio (.wav) a texto usando Whisper local.
Módulo independiente — listo para integrarse al pipeline.
"""

import sys
import shutil
from pathlib import Path

# ──────────────────────────────────────────────
# Verificación de dependencias
# ──────────────────────────────────────────────
try:
    import whisper
except ImportError:
    print("[ERROR] Instala Whisper: pip install openai-whisper")
    sys.exit(1)

if not shutil.which("ffmpeg"):
    print("[ERROR] ffmpeg no está instalado o no está en el PATH.")
    print("Instálalo con: winget install Gyan.FFmpeg")
    print("Luego reinicia la terminal.")
    sys.exit(1)

# ──────────────────────────────────────────────
# Configuración del modelo
# ──────────────────────────────────────────────
MODEL_NAME = "tiny"

print(f"[WHISPER] Cargando modelo '{MODEL_NAME}' en memoria...")

try:
    modelo = whisper.load_model(MODEL_NAME, device="cpu")
    print(f"[OK] Modelo '{MODEL_NAME}' listo para inferencia.")
except Exception as e:
    print(f"[FALLO CRÍTICO] No se pudo cargar Whisper: {e}")
    sys.exit(1)


# ──────────────────────────────────────────────
# Función principal
# ──────────────────────────────────────────────
def transcribir(ruta_audio: str) -> str:
    """
    Transcribe un archivo .wav a texto.

    Args:
        ruta_audio: Ruta al archivo .wav

    Returns:
        Texto transcrito limpio
    """
    ruta = Path(ruta_audio).resolve()

    if not ruta.exists():
        raise FileNotFoundError(f"[ERROR] Archivo no encontrado: {ruta}")

    print(f"[STT] Transcribiendo: {ruta.name}")

    try:
        resultado = modelo.transcribe(
            str(ruta),
            language="es",     # fuerza español (más rápido y preciso)
            task="transcribe", # evita traducción automática
            fp16=False,
            verbose=False
        )

        texto = resultado["text"].strip()

        if not texto:
            print("[WARN] No se detectó voz clara en el audio.")

        return texto

    except Exception as e:
        raise RuntimeError(f"[ERROR] Fallo en transcripción: {e}") from e


# ──────────────────────────────────────────────
# Prueba integrada (audio → texto)
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("\n[TEST] Grabación → Transcripción\n")

    try:
        # Import correcto desde el paquete backend
        from backend.audio_input import capturar

        ruta_wav = capturar(duracion_segundos=5)
        texto = transcribir(ruta_wav)

        print("\n" + "=" * 50)
        print("[TEXTO TRANSCRITO]")
        print(texto)
        print("=" * 50 + "\n")

    except ImportError:
        print("[ERROR] No se pudo importar audio_input.")
        print("Ejecuta desde la raíz del proyecto:")
        print("python -m backend.speech_to_text")

    except Exception as e:
        print(f"[FALLO] {e}")
        sys.exit(1)