# =============================================================================
# prompt.py — Plantilla de prompt del asistente académico
# Responsabilidad única: construir el prompt final que se envía al modelo
# =============================================================================

# Rol e instrucciones base del asistente
# Se define aquí para poder cambiarlo sin tocar la lógica de conexión
SYSTEM_ROLE: str = """Eres un asistente académico de cátedra especializado en 
tecnología e inteligencia artificial. Tu función es apoyar a estudiantes y 
docentes con explicaciones claras, precisas y en español. 

Pautas de comportamiento:
- Responde siempre en español, con tono formal pero accesible.
- Cuando expliques conceptos técnicos, usa ejemplos concretos.
- Si no conoces la respuesta con certeza, indícalo claramente.
- Mantén las respuestas enfocadas y estructuradas.
- Evita respuestas excesivamente largas; sé conciso pero completo."""


def build_prompt(user_input: str) -> str:
    """
    Construye el prompt completo combinando el rol del sistema
    con la pregunta del usuario.

    Args:
        user_input (str): Texto ingresado por el usuario desde consola.

    Returns:
        str: Prompt formateado listo para enviar al modelo.
    """
    if not user_input or not user_input.strip():
        raise ValueError("El input del usuario no puede estar vacío.")

    prompt = f"""[INST] {SYSTEM_ROLE}

Pregunta del estudiante:
{user_input.strip()}
[/INST]"""

    return prompt