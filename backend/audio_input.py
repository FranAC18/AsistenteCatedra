"""
audio_input.py
Captura audio desde el micrófono y lo guarda como archivo .wav.
Módulo independiente — no habla con LLM todavía.
"""

import sys
import wave
from datetime import datetime
from pathlib import Path

try:
    import sounddevice as sd
    import numpy as np
except ImportError:
    print("[ERROR] Instala dependencias: pip install sounddevice numpy")
    sys.exit(1)


# ──────────────────────────────────────────────
# Constantes de grabación
# ──────────────────────────────────────────────
SAMPLE_RATE = 16000   # Whisper prefiere 16kHz
CHANNELS    = 1       # Mono — menos ruido, más compatibilidad
DTYPE       = "int16" # PCM 16-bit


def esperar_enter(mensaje: str = "Presiona Enter para grabar...") -> None:
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input(mensaje)


def grabar_audio(duracion_segundos: int = 7) -> np.ndarray:
    """
    Graba audio desde el micrófono por N segundos.

    Args:
        duracion_segundos: Duración de la grabación.

    Returns:
        Array numpy con las muestras de audio.

    Raises:
        RuntimeError: Si no se detecta micrófono disponible.
    """
    dispositivos = sd.query_devices()
    entrada_disponible = any(
        d["max_input_channels"] > 0 for d in dispositivos
    )
    if not entrada_disponible:
        raise RuntimeError(
            "No se encontró micrófono. "
            "Conecta uno y vuelve a intentarlo."
        )

    print(f"[REC] Grabando {duracion_segundos}s... habla ahora.")

    try:
        audio = sd.rec(
            frames=int(duracion_segundos * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
        )
        sd.wait()
    except sd.PortAudioError as e:
        raise RuntimeError(f"Error de PortAudio al grabar: {e}") from e

    print("[OK] Grabación finalizada.")
    return audio


def guardar_wav(audio: np.ndarray, ruta: str | None = None) -> str:
    """
    Guarda el array de audio como archivo .wav en data/audio/ o en ruta personalizada.

    Args:
        audio:  Array numpy con muestras int16.
        ruta:   Ruta destino. Si es None, genera automáticamente en data/audio/.

    Returns:
        Ruta absoluta del archivo guardado.
    """
    if ruta is None:
        # Directorio relativo a la ubicación física de este script
        audio_dir = Path(__file__).resolve().parent / "data" / "audio"
        audio_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = str(audio_dir / f"audio_{timestamp}.wav")

    try:
        with wave.open(ruta, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)          # int16 → 2 bytes por muestra
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio.tobytes())
    except Exception as e:
        raise IOError(f"No se pudo guardar el archivo WAV en '{ruta}': {e}") from e

    print(f"[WAV] Guardado en: {ruta}")
    return ruta


def capturar(duracion_segundos: int = 7, ruta_salida: str | None = None) -> str:
    """
    Flujo completo: esperar Enter → grabar → guardar WAV.

    Args:
        duracion_segundos: Duración de la grabación.
        ruta_salida:       Ruta del WAV de salida (opcional).

    Returns:
        Ruta al archivo .wav listo para transcribir.
    """
    esperar_enter()
    audio = grabar_audio(duracion_segundos)
    ruta  = guardar_wav(audio, ruta_salida)
    return ruta


# ──────────────────────────────────────────────
# Prueba rápida del módulo solo
# ──────────────────────────────────────────────
if __name__ == "__main__":
    try:
        ruta_wav = capturar(duracion_segundos=7)
        print(f"[LISTO] WAV disponible en: {ruta_wav}")
    except (RuntimeError, IOError) as e:
        print(f"[FALLO] {e}")
        sys.exit(1)