# =============================================================================
# config.py — Parámetros globales del sistema
# Centraliza toda la configuración para facilitar ajustes sin tocar otros módulos
# =============================================================================

# --- Conexión con Ollama ---
OLLAMA_BASE_URL: str = "http://localhost:11434"
OLLAMA_API_ENDPOINT: str = f"{OLLAMA_BASE_URL}/api/generate"

# --- Modelo LLM ---
MODEL_NAME: str = "mistral"

# --- Parámetros de generación ---
# temperature: 0.0 = determinista, 1.0 = más creativo
TEMPERATURE: float = 0.7

# top_p: probabilidad acumulada para nucleus sampling
TOP_P: float = 0.9

# max_tokens: límite de tokens en la respuesta (0 = sin límite explícito)
MAX_TOKENS: int = 1024

# stream: False para recibir la respuesta completa de una sola vez
STREAM: bool = False

# --- Timeouts (segundos) ---
REQUEST_TIMEOUT: int = 60   # espera máxima para respuesta del modelo

# --- Consola ---
# Separador visual para formatear la salida en terminal
CONSOLE_SEPARATOR: str = "─" * 60