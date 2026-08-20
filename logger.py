import os
import re


def procesar_chat(ruta_archivo: str, titulo_semana: str) -> str:
    """
    Lee el archivo de bitácora. Si ya está formateado en Markdown,
    lo concatena directamente. Si es un chat crudo, extrae e interactúa.
    """
    with open(ruta_archivo, encoding='utf-8') as file:
        contenido = file.read()

    # NUEVA LÓGICA BLINDADA:
    # Verificamos si el archivo ya tiene la estructura de una bitácora procesada.
    es_formateado = (
        "**Prompt:**" in contenido or 
        "### Prompts dados:" in contenido or 
        "## Prompt" in contenido or
        "### Resultado / Aprendizaje" in contenido
    )

    if es_formateado:
        resultado = ""
        # Agrega encabezado si el archivo no lo tiene ya
        if not contenido.strip().startswith("#"):
            resultado += f"# {titulo_semana}\n\n"
        resultado += contenido.strip() + "\n\n---\n\n"
        return resultado

    # Si es un chat crudo, aplicamos la expresión regular original
    patron = r"User\s*:\s*(.*?)\s*Gemini\s*:\s*(.*?)(?=User\s*:|$)"
    interacciones = re.findall(patron, contenido, re.DOTALL)
    cantidad_prompts = len(interacciones)

    if cantidad_prompts == 0:
        if contenido.strip():
            return contenido.strip() + "\n\n---\n\n"
        return ""

    md = f"# {titulo_semana}\n\n"
    md += f"### Prompts dados: {cantidad_prompts}\n"
    md += "### Chats creados: 1\n\n"

    for usuario, gemini in interacciones:
        prompt_limpio = usuario.strip()
        respuesta_limpia = gemini.strip()
        prompt_formateado = "\n".join([f"> **{linea}**" for linea in prompt_limpio.split('\n')])
        md += f"**Prompt:**\n{prompt_formateado}\n\n"
        md += f"**Respuesta:**\n{respuesta_limpia}\n\n---\n\n"

    return md


def main() -> None:
    # ORDENADO: De la más reciente (Semana 6) a la más antigua (Semana 0)
    archivos_a_procesar = {
        "docs/logs/Semana6.md": "Semana 6 - Proyecto Final: SensorHub & Estabilización de API",
        "docs/logs/Semana5.md": "Semana 5 - Arquitectura, IA y Calidad Avanzada",
        "docs/logs/Semana4.md": "Semana 4 - Docker, CI/CD y Despliegue",
        "docs/logs/Semana3.md": "Semana 3 - API, Persistencia y Capas",
        "docs/logs/Semana2.md": "Semana 2 - Scrum, TDD y User Stories",
        "docs/logs/Semana1.md": "Semana 1 - Del firmware al software: reencuadra lo que ya sabes",
        "docs/logs/Semana0.md": "Semana 0 — Diagnóstico y puesta a punto"
    }
    archivo_salida = "AI_LOG.md"
    contenido_total_md = ""

    print("Iniciando procesamiento de bitácoras...")
    for archivo, titulo in archivos_a_procesar.items():
        if os.path.exists(archivo):
            print(f"Procesando: {archivo}...")
            extraido = procesar_chat(archivo, titulo)
            print(f" -> Caracteres extraídos de {titulo}: {len(extraido)}")
            contenido_total_md += extraido
        else:
            print(f"⚠️ Archivo no encontrado: {archivo}")

    # VALIDACIÓN DE SEGURIDAD: Evitar generar un AI_LOG vacío
    if not contenido_total_md.strip():
        print("❌ Error crítico: El contenido extraído está vacío. Revisa el contenido de tus archivos.")
        return

    # Escribimos el resultado en el archivo final
    with open(archivo_salida, 'w', encoding='utf-8') as file:
        file.write(contenido_total_md)

    print(f"\n✅ ¡Éxito! Tu bitácora unificada ha sido generada en: {archivo_salida}")


if __name__ == "__main__":
    main()