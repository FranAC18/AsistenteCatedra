# =============================================================================
# llm_client.py — Cliente de conexión con Ollama
# Responsabilidad única: enviar prompts al modelo local y devolver respuestas
# No conoce nada del prompt ni de la interfaz; solo habla con la API de Ollama
# =============================================================================

import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

from config import (
    OLLAMA_API_ENDPOINT,
    MODEL_NAME,
    TEMPERATURE,
    TOP_P,
    MAX_TOKENS,
    STREAM,
    REQUEST_TIMEOUT,
)


class OllamaConnectionError(Exception):
    """Se lanza cuando Ollama no está disponible o no responde."""
    pass


class OllamaResponseError(Exception):
    """Se lanza cuando Ollama responde pero con un error en el contenido."""
    pass


def query_model(prompt: str) -> str:
    """
    Envía un prompt al modelo Ollama configurado y retorna la respuesta
    como texto plano.

    Args:
        prompt (str): Prompt completo ya construido para el modelo.

    Returns:
        str: Texto de respuesta generado por el modelo.

    Raises:
        OllamaConnectionError: Si Ollama no está corriendo o no responde.
        OllamaResponseError: Si la respuesta tiene un formato inesperado.
    """
    payload = {
        "model":   MODEL_NAME,
        "prompt":  prompt,
        "stream":  STREAM,
        "options": {
            "temperature": TEMPERATURE,
            "top_p":       TOP_P,
            "num_predict": MAX_TOKENS,
        },
    }

    try:
        response = requests.post(
            url=OLLAMA_API_ENDPOINT,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

    except ConnectionError:
        raise OllamaConnectionError(
            "No se pudo conectar con Ollama. "
            "Asegúrate de que el servicio esté corriendo en "
            f"{OLLAMA_API_ENDPOINT.split('/api')[0]}"
        )
    except Timeout:
        raise OllamaConnectionError(
            f"Ollama no respondió dentro del límite de {REQUEST_TIMEOUT}s. "
            "El modelo puede estar cargándose; intenta de nuevo."
        )
    except RequestException as e:
        raise OllamaConnectionError(f"Error de red inesperado: {e}")

    # --- Parsear respuesta JSON ---
    try:
        data = response.json()
        text = data.get("response", "").strip()
    except ValueError:
        raise OllamaResponseError(
            "La respuesta de Ollama no tiene formato JSON válido."
        )

    if not text:
        raise OllamaResponseError(
            "Ollama devolvió una respuesta vacía. "
            "Verifica que el modelo esté disponible con: ollama list"
        )

    return text


def check_ollama_availability() -> bool:
    """
    Verifica si el servicio Ollama está activo consultando su endpoint raíz.

    Returns:
        bool: True si Ollama responde, False si no está disponible.
    """
    from config import OLLAMA_BASE_URL
    try:
        r = requests.get(OLLAMA_BASE_URL, timeout=5)
        return r.status_code == 200
    except (ConnectionError, Timeout, RequestException):
        return False