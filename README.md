# Asistente de Cátedra Inteligente

Proyecto de Inteligencia Artificial local basado en procesamiento de lenguaje natural.

## Tecnologías usadas

- Python
- Ollama (Mistral)
- Whisper (Speech-to-Text)
- SoundDevice
- NumPy

## Arquitectura

Pipeline basado en:
Audio → STT → NLP → LLM → Respuesta

## Estado del proyecto

- [x] Conexión con LLM local (Mistral)
- [x] Captura de audio
- [x] Guardado de audio
- [ ] Transcripción (requiere ffmpeg)
- [ ] Limpieza NLP
- [ ] TTS
- [ ] Frontend

## Notas

El proyecto está diseñado para funcionar completamente offline sin uso de APIs externas, cumpliendo con los requisitos del taller.

Para ejecutar correctamente la transcripción, es necesario instalar ffmpeg.