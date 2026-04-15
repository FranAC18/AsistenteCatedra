# =============================================================================
# main.py — Orquestador principal del asistente académico
# Responsabilidad: coordinar el flujo completo entrada → prompt → modelo → salida
# No contiene lógica de conexión ni de construcción de prompts; solo dirige
# =============================================================================

from config import CONSOLE_SEPARATOR, MODEL_NAME
from prompt import build_prompt
from llm_client import query_model, check_ollama_availability, OllamaConnectionError, OllamaResponseError


def print_banner() -> None:
    """Muestra el banner de bienvenida al iniciar el asistente."""
    print(CONSOLE_SEPARATOR)
    print("  Asistente de Cátedra — IA Local")
    print(f"  Modelo: {MODEL_NAME}  |  Motor: Ollama")
    print(CONSOLE_SEPARATOR)
    print("  Escribe tu pregunta y presiona Enter.")
    print("  Comandos: 'salir' o 'exit' para terminar.")
    print(CONSOLE_SEPARATOR)


def run_assistant() -> None:
    """
    Bucle principal de interacción con el usuario.
    Lee input desde consola, construye el prompt, consulta el modelo
    y muestra la respuesta formateada.
    """
    print_banner()

    # --- Verificar disponibilidad de Ollama antes de entrar al bucle ---
    print("\n  Verificando conexión con Ollama...", end=" ")
    if not check_ollama_availability():
        print("✗ FALLO")
        print("\n  [ERROR] Ollama no está disponible.")
        print("  Asegúrate de haber ejecutado:  ollama serve")
        print(f"  Y de tener el modelo descargado:  ollama pull {MODEL_NAME}\n")
        return
    print("✓ OK\n")

    # --- Bucle de conversación ---
    while True:
        try:
            user_input = input("  Tú › ").strip()
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C o Ctrl+D cierran limpiamente
            print("\n\n  Sesión finalizada. Hasta pronto.\n")
            break

        # Comandos de salida
        if user_input.lower() in ("salir", "exit", "quit"):
            print("\n  Sesión finalizada. Hasta pronto.\n")
            break

        # Ignorar input vacío
        if not user_input:
            print("  (Escribe algo para continuar)\n")
            continue

        # --- Pipeline: construir prompt → consultar modelo → mostrar respuesta ---
        print(f"\n{CONSOLE_SEPARATOR}")
        print("  Procesando...\n")

        try:
            prompt   = build_prompt(user_input)
            response = query_model(prompt)

            print(f"  Asistente › \n")
            # Indentamos cada línea de la respuesta para legibilidad
            for line in response.splitlines():
                print(f"  {line}")

        except OllamaConnectionError as e:
            print(f"  [ERROR DE CONEXIÓN] {e}")

        except OllamaResponseError as e:
            print(f"  [ERROR DE RESPUESTA] {e}")

        except ValueError as e:
            # Captura el ValueError de build_prompt (input vacío)
            print(f"  [ERROR DE INPUT] {e}")

        except Exception as e:
            print(f"  [ERROR INESPERADO] {e}")

        finally:
            print(f"\n{CONSOLE_SEPARATOR}\n")


# =============================================================================
# Punto de entrada
# =============================================================================
if __name__ == "__main__":
    run_assistant()