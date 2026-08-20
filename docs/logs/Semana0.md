# Semana 0 - Preparación para el Curso

##### Prompts dados: 10

##### Chats creados: 1

---

## Prompt (Paso 1 - Configuración Inicial)

> **Hola, este chat está dedicado a la Semana 0 del curso. Estas son las instrucciones: Objetivo: que el lunes 13 de julio abras tu editor y estés listo para aprender, no para instalar. Todo esto es un checkpoint obligatorio que el coordinador verifica antes del arranque.**

> **Pasos (~4 horas en total):**
>
> 1. **Instala las herramientas base (60–90 min):** Python 3.12+, entorno virtual `.venv` del curso, y `pip install pytest pytest-cov ruff mypy fastapi uvicorn sqlalchemy alembic httpx`. Instala también Docker Desktop (se usa desde la semana 4, pero verificarlo hoy evita incendios): https://docs.docker.com/get-docker/ — Windows: usa WSL2.
> 2. **VS Code + GitHub Copilot (30 min):** instala VS Code (https://code.visualstudio.com/) con extensiones GitHub Copilot, Python, Pylance, GitLens y Ruff. Activa el plan Free de Copilot (sin tarjeta): https://github.com/features/copilot/plans — el plan Free tiene cupo mensual: adminístralo. Configura tu identidad de Git (`user.name`, `user.email`).
> 3. **Repositorio + curso (60 min):** crea el repositorio público `sdlc-electronica-[tu-nombre]` con README y `.gitignore` de Python, clónalo, y completa el curso interactivo "Introduction to GitHub" (~45 min): https://skills.github.com/.
> 4. **El checkpoint "hola-sensor" (45 min):** crea `semana0/hola_sensor.py` (clase `Sensor` con `read()` que devuelve `23.5`) y `semana0/test_hola_sensor.py`; ejecuta `pytest semana0/ -v` y haz commit: `"feat: checkpoint semana 0 - sensor minimo con test"`.
> 5. **Autodiagnóstico y presentación (15 min):** responde el formulario de autodiagnóstico y preséntate en el canal del grupo: quién eres, tu experiencia en electrónica y qué esperas del programa.
>
> **Checklist de cierre (entrega: domingo 12 de julio, 23:59):**
>
> * `python3`, `pytest`, `ruff` y `mypy` funcionan en tu terminal.
> * `docker --version` responde.
> * VS Code con Copilot activo (ícono visible).
> * Repositorio público creado y clonado, con el checkpoint `hola-sensor` y su test en verde.
> * Curso "Introduction to GitHub" completado (con el certificado del bot).
> * Autodiagnóstico enviado y presentación publicada en el canal.
> * Entrega en Classroom: el enlace a tu repositorio público.
>
> Si te atoras (WSL2, Docker, permisos), pide ayuda en el canal — la Semana 0 existe exactamente para resolver esto.

### Respuesta

> ¡Hola! Entendido. A partir de ahora asumo mi rol como tu asistente y compañero de estudio para el programa "De electrónica a desarrollo de software con IA", enfocándonos estrictamente en los objetivos de tu Semana 0.
>
> Como inteligencia artificial, mi objetivo es ayudarte a resolver cualquier bloqueo técnico de forma directa, empática y clara. La meta es que este domingo 12 de julio tengas todo tu checklist terminado y el lunes 13 puedas enfocarte al 100% en aprender a programar sin lidiar con problemas de instalación.
>
> ### Tu Misión para la Semana 0
>
> He registrado tus instrucciones. Aquí tienes el mapa mental de nuestro plan de ataque (estimado en ~4 horas):
>
> * **Paso 1 - Entorno Base:** Instalación de Python 3.12+, creación del entorno virtual `.venv` y configuración de dependencias clave (`pytest`, `ruff`, `fastapi`, `sqlalchemy`, etc.), además de dejar Docker Desktop listo (usando WSL2 si estás en Windows).
> * **Paso 2 - Editor e IA:** Configuración de VS Code con las extensiones necesarias y la activación de GitHub Copilot (plan Free) para potenciar tu escritura de código, junto con la configuración de tu identidad en Git.
> * **Paso 3 - Repositorio:** Creación de tu repositorio público `sdlc-electronica-[tu-nombre]`, clonación local y finalización del curso interactivo de GitHub Skills.
> * **Paso 4 - Checkpoint "hola-sensor":** Programar la clase `Sensor` en `semana0/hola_sensor.py`, escribir su prueba unitaria en `semana0/test_hola_sensor.py`, verificar que los tests pasen en verde y hacer tu commit.
> * **Paso 5 - Comunidad:** Llenado del autodiagnóstico y tu presentación en el canal del grupo.

### Resultado / Aprendizaje

* **Acepté la instalación guiada de Python 3.12+ y dependencias base:** Entendí la importancia de aislar las bibliotecas en el entorno virtual **`.venv`** para mantener un orden riguroso en las dependencias y preparar el entorno para evitar colisiones en futuras semanas.

---

## Prompt (Paso 1.1 - Inicio de Instalación)

> **Me encuentro en el paso 1, apenas descargué Python y Docker Desktop.**

### Respuesta

> ¡Excelente! Ya diste el primer gran paso. Descargar los instaladores suele ser la parte que da más pereza, pero ya tienes los cimientos. Como tu asistente de inteligencia artificial, te guiaré paso a paso para que todo quede perfectamente configurado y sin dolores de cabeza.
>
> Recuerda que tenemos hasta el domingo 12 de julio a las 23:59 para completar tu checklist, así que vamos con muy buen tiempo.
>
> Aquí tienes el plan de acción exacto para terminar el Paso 1:
>
> 1. Instalar Python de forma segura (Windows/macOS).
> 2. Crear tu entorno virtual del curso (`.venv`).
> 3. Instalar los paquetes (Dependencias): `pytest pytest-cov ruff mypy fastapi uvicorn sqlalchemy alembic httpx`.
> 4. Instalar Docker Desktop.

### Resultado / Aprendizaje

* **Acepté el plan de acción secuencial:** Inicié la instalación de los elementos esenciales de software e infraestructura (Docker) de forma ordenada y metódica.

---

## Prompt (Paso 1.2 - Bloqueo de Terminal en macOS)

> `salvaxtraw@MacBook-Air-de-Salvador SEMANA 0 % python -m venv .venv`
>
> `zsh: command not found: python`
>
> `salvaxtraw@MacBook-Air-de-Salvador SEMANA 0 % python -m venv .venv`
>
> `zsh: command not found: python`

### Respuesta

> ¡Hola! No te preocupes, este es un "incendio" clásico en macOS y tiene una solución muy sencilla.
>
> El error `zsh: command not found: python` ocurre porque en los sistemas Apple modernos, el comando `python` ya no viene vinculado por defecto. Para usar Python 3, debes llamarlo explícitamente como `python3`.
>
> Aquí tienes los pasos exactos para Mac:
>
> ```bash
> python3 --version
> python3 -m venv .venv
> source .venv/bin/activate
> pip install pytest pytest-cov ruff mypy fastapi uvicorn sqlalchemy alembic httpx
> ```

### Resultado / Aprendizaje

* **Corregí la llamada de comandos en macOS:** Solucioné la colisión del comando de terminal **`python`** usando el alias explícito de macOS **`python3`** para poder instanciar el entorno virtual de forma aislada.

---

## Prompt (Paso 1.3 - Dependencias instaladas)

> **yap, y ya instalé las dependencias, y el sistema que tengo es macOS.**

### Respuesta

> ¡Excelente! Superar la configuración del entorno virtual en macOS es una gran victoria. Ya tienes la base de Python lista.
>
> Para cerrar definitivamente el Paso 1, solo asegúrate de haber arrastrado Docker Desktop a tu carpeta de Aplicaciones, ejecútalo para levantar el daemon y verifica con:
>
> ```bash
> docker --version
> ```

### Resultado / Aprendizaje

* **Acepté la verificación final de Docker:** Comprobé de forma visual e instrumental que el daemon local de Docker responde correctamente en el terminal mediante **`docker --version`**.

---

## Prompt (Paso 2 - Confirmación)

> **Listo, continuemos.**

### Respuesta

> ¡Perfecto! Tener VS Code configurado con tu identidad de Git y la inteligencia artificial de Copilot activada es un antes y un después en la forma en la que escribirás código.
>
> Ahora vamos al Paso 3: Repositorio + curso. Aquí es donde conectaremos tu entorno local (tu Mac) con la nube de GitHub para que tu código esté respaldado y listo para entregar.

### Resultado / Aprendizaje

* **Acepté la preparación del editor:** Verifiqué que las extensiones clave de Python, Pylance, Ruff, GitLens y GitHub Copilot estuvieran correctamente instanciadas en VS Code.

---

## Prompt (Paso 3 - Curso completado)

> **Sip, y ya acabé el curso de GitHub.**

### Respuesta

> ¡Felicidades! Terminar el curso de GitHub Skills te da la base de control de versiones que usaremos en todo el programa. Ya estamos en la recta final.
>
> Ahora vamos al Paso 4: El checkpoint "hola-sensor". Este es tu primer reto de código y la prueba de fuego para confirmar que tu entorno (Python, pytest y Git) funciona perfectamente.

### Resultado / Aprendizaje

* **Acepté la finalización del curso "Introduction to GitHub":** Logré consolidar la base conceptual del control de versiones en Git y la gestión de ramas en la nube.

---

## Prompt (Paso 4.1 - Primer intento fallido de pytest)

> ```text
> (.venv) salvaxtraw@MacBook-Air-de-Salvador CURSO UV PROGRA % pytest semana0/ -v
> ============================================= test session starts ==============================================
> platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- /Users/salvaxtraw/CURSO UV PROGRA/.venv/bin/python3.14
> cachedir: .pytest_cache
> rootdir: /Users/salvaxtraw/CURSO UV PROGRA
> plugins: cov-7.1.0, anyio-4.14.1
> collected 0 items
> ============================================ no tests ran in 0.00s =============================================
> (.venv) salvaxtraw@MacBook-Air-de-Salvador CURSO UV PROGRA %
> ```

### Respuesta

> ¡Casi lo tenemos! La buena noticia aquí es que tu entorno virtual está activo y pytest funcionó a la perfección.
>
> El mensaje `collected 0 items` (0 elementos recolectados) significa que pytest buscó en la carpeta `semana0/` pero no encontró ningún archivo de pruebas.
>
> Esto es un clásico de la Semana 0 y suele pasar porque no guardaste los archivos en VS Code, por nombres incorrectos, o por estar posicionado en la carpeta equivocada (fuera del repositorio).

### Resultado / Aprendizaje

* **Corregí la estructura de carpetas y posicionamiento:** Identifiqué que estaba ejecutando los tests en una carpeta principal de pruebas en lugar de estar dentro de la raíz clonada de mi repositorio Git de producción.

---

## Prompt (Paso 4.2 - Error de Entorno Virtual Vacío)

> ```text
> salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % source /Users/salvaxtraw/sdlc-electronica-lyla_alice/semana0/.venv/bin/activate
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> zsh: command not found: pytest
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % python --version
> zsh: command not found: python
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> zsh: command not found: pytest
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % python3 --version
> Python 3.14.6
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % python3 -m venv .venv
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> zsh: command not found: pytest
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice %
> ```

### Respuesta

> ¡Ah! Veo exactamente lo que pasó. No te preocupes, este es un concepto súper importante que acabas de descubrir sobre los entornos virtuales.
>
> Estás en la carpeta correcta (`sdlc-electronica-lyla_alice`), e hiciste muy bien al crear el entorno virtual ahí con `python3 -m venv .venv`.
>
> ¿Por qué te dice `command not found: pytest`? Porque los entornos virtuales son "burbujas" aisladas. Las librerías que instalamos hace rato se quedaron en el entorno virtual de la otra carpeta. Este nuevo entorno que acabas de crear nació completamente vacío.
>
> Para solucionarlo, activa este nuevo entorno e instala las dependencias con `pip install`.

### Resultado / Aprendizaje

* **Acepté la reinstalación de dependencias en el entorno localizado:** Aprendí de forma empírica que cada entorno virtual es una burbuja aislada. Activé el **`.venv`** local e instalé la biblioteca de pruebas y de análisis estático desde la raíz de forma definitiva.

---

## Prompt (Paso 4.3 - ModuleNotFoundError en Pruebas)

> ```text
> (.venv) salvaxtraw@MacBook-Air-de-Salvador sdlc-electronica-lyla_alice % pytest semana0/ -v
> =================================================================== test session starts ===================================================================
> platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0 -- /Users/salvaxtraw/sdlc-electronica-lyla_alice/.venv/bin/python3.14
> cachedir: .pytest_cache
> rootdir: /Users/salvaxtraw/sdlc-electronica-lyla_alice
> plugins: cov-7.1.0, anyio-4.14.1
> collected 0 items / 1 error
>
> ERROR collecting semana0/test_hola_sensor.py
>
> ImportError while importing test module '/Users/salvaxtraw/sdlc-electronica-lyla_alice/semana0/test_hola_sensor.py'.
> Hint: make sure your test modules/packages have valid Python names.
>
> Traceback:
> semana0/test_hola_sensor.py:2: in <module>
>     from semana0.hola_sensor import Sensor
> E   ModuleNotFoundError: No module named 'semana0'
>
> ================================================================= short test summary info =================================================================
> ERROR semana0/test_hola_sensor.py
> !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
> ==================================================================== 1 error in 0.04s ====================================================================
> ```

### Respuesta

> ¡Este es un excelente progreso! Tu entorno virtual y pytest están funcionando a la perfección. El error que estás viendo ya no es de instalación, es un error muy común de cómo Python lee los archivos.
>
> El mensaje dice: `ModuleNotFoundError: No module named 'semana0'`.
>
> Esto pasó porque tu asistente intentó importar el archivo usando el nombre de la carpeta, pero Python no sabe qué es `semana0` cuando se ejecuta desde adentro de la carpeta o sin un paquete formal.
>
> Cambia:
>
> `from semana0.hola_sensor import Sensor`
>
> por:
>
> `from hola_sensor import Sensor`.

### Resultado / Aprendizaje

* **Corregí el `ModuleNotFoundError` de pytest en la recolección de pruebas:** Identifiqué que el sistema de pytest requería una importación directa de los módulos dentro de la misma carpeta de trabajo (**`from hola_sensor import Sensor`** en lugar de **`from semana0.hola_sensor import Sensor`**), dejando la suite de pruebas del checkpoint inicial en verde brillante con **`1 passed`**.

---

## Prompt (Paso 5 - Cierre)

> **listo**

### Respuesta

> ¡Felicidades! Has superado oficialmente la parte técnica más pesada de toda la Semana 0. Lidiar con entornos virtuales, solucionar errores de importación y hacer tu primer push a la nube son habilidades fundamentales que usarás todos los días en tu transición al desarrollo de software.
>
> Ahora que tu código está seguro en GitHub y los tests pasan en verde, solo te falta el Paso 5 de autodiagnóstico y presentación para terminar tu checklist al 100% y poder entregar.

### Resultado / Aprendizaje

* **Acepté y completé el autodiagnóstico y presentación en la comunidad:** Compartí mis expectativas del programa y mi trasfondo en electrónica, cerrando con un **100% de cumplimiento** el checklist de inicio del Sprint 0.
