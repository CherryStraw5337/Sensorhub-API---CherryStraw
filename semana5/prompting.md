# Bitácora de Prompting y Uso Crítico de IA - Semana 5

## 1. La Anatomía de un Prompt Efectivo en Ingeniería de Software
Un prompt profesional no es una simple pregunta, es una especificación de requerimientos. Se compone de: Contexto, Instrucción, Restricciones y Formato.

**Ejemplo de Prompt utilizado para TDD (Conversiones):**
> **Contexto:** Actúa como un Ingeniero de Software Senior especializado en Python.
> **Instrucción:** Escribe una función pura `celsius_to_fahrenheit` y sus pruebas unitarias en `pytest`.
> **Restricciones:** Usa tipado estricto (`float`). Añade una cláusula de guarda (guard clause) para lanzar un `ValueError` si la temperatura ingresada es inferior al cero absoluto (-273.15 °C).
> **Formato:** Devuelve el código estructurado y modularizado, listo para producción.

## 2. Detección de Riesgos en Código Generado (El Instrumento Descalibrado)
Un LLM predice el siguiente token buscando plausibilidad, no corrección matemática o lógica. Al usar IA en el código de este proyecto, he vigilado de cerca estos riesgos:
* **Alucinaciones:** La IA a menudo inventa métodos o asume librerías que no están en el `requirements.txt`. El código debe compilar y pasar `mypy` antes de darse por válido.
* **Seguridad:** Riesgo de sugerir código vulnerable (ej. concatenación de strings en queries SQL en lugar de usar inyección segura a través del ORM SQLAlchemy).
* **Licencias y Propiedad Intelectual:** Evitar que la IA pegue bloques monolíticos de código que podrían estar atados a licencias restrictivas (GPL) sin la debida atribución.

## 3. Fundamento Arquitectónico: ¿Cuándo NO usar Microservicios?
Guiado por el principio *Monolith First* de Martin Fowler, concluimos que NO se deben usar microservicios cuando:
1.  **El dominio es incierto:** Si no entendemos bien los "bounded contexts" (límites lógicos del negocio), crearemos microservicios acoplados que requerirán cambios simultáneos (el antipatrón "monolito distribuido").
2.  **Sobrecarga Operativa:** Un equipo pequeño no debe asumir el costo de mantener múltiples pipelines CI/CD, redes, seguridad entre contenedores y observabilidad distribuida si el sistema aún no tiene escala masiva.
3.  **Latencia Estricta:** Cuando la comunicación en milisegundos es vital. Una llamada a una función en memoria (monolito) siempre será órdenes de magnitud más rápida que una petición HTTP/gRPC entre servidores.