# Semana 1 - Del firmware al software: reencuadra lo que ya sabes

### Prompts dados: 23

### Chats creados: 1

---

## Prompt (Lunes)

> Mapea una lectura de sensor de C a Python moderno usando dataclasses inmutables, enums, tipado estructural (`Protocol`) y 5 funciones puras de procesamiento.

### Respuesta

> ¡Excelente trabajo completando el Checkpoint de la Semana 0!
>
> Establecemos el **Pacto de Trabajo**: la IA propone estructuras y código limpio, pero tú debes auditar y entender cada línea. Si algo no lo puedes defender, lo borramos y lo reescribimos.
>
> Para hoy, Lunes (Python Idiomático para ingenieros de C), abordaremos:
>
> 1. **Modelado de Dominio (De `struct` y `#define` a Enum y Dataclass):** En Python moderno, representamos una lectura (`Reading`) usando `@dataclass(frozen=True)`. Al hacerla inmutable, evitamos efectos secundarios de punteros de C en memoria.
> 2. **Abstracción con Protocol (Tipado Estructural):** Definiremos un contrato de interfaz `Sensor` usando `typing.Protocol`.
> 3. **5 Funciones Puras:** Funciones deterministas en `sensor_utils.py` que procesen datos generando copias (`replace`) sin modificar la entrada.

### Resultado / Aprendizaje

* **Acepté el modelado de datos inmutable:** Adopté **`@dataclass(frozen=True)`** para definir la estructura **`Reading`** y asegurar que los datos no puedan ser mutados accidentalmente, mitigando efectos colaterales de punteros.
* **Rechacé y corregí la ruta de ejecución de Mypy:** La IA sugirió correr Mypy posicionada dentro de la subcarpeta **`semana1/`**, lo cual rompía la resolución de imports de módulos absolutos. Corregí la metodología de calidad, obligándome a ejecutar todos los linters siempre desde el directorio raíz del proyecto.

---

## Prompt (Martes)

> Reimplementa una máquina de estados finita (FSM) orientada a objetos para experimentar el estilo OO frente al C procedural, con 4 tests unitarios.

### Respuesta

> El corazón del firmware robusto embebido es la **Máquina de Estados Finitos (FSM)**. En C, típicamente se implementa con variables globales y un `switch-case` gigante en el superloop, lo cual genera alto acoplamiento y transiciones ilegales invisibles.
>
> En Python y Orientación a Objetos, encapsulamos el estado y sus transiciones válidas dentro de una clase, controlando los errores mediante excepciones personalizadas.
>
> Crearemos una FSM para un **Semáforo de la Bodega (`TrafficLightFSM`)** usando un mapeo **O(1)** de transiciones válidas en un diccionario.

### Resultado / Aprendizaje

* **Rechacé el primer diseño genérico de FSM:** La IA propuso un diseño de FSM para un nodo IoT complejo con múltiples excepciones personalizadas, el cual se desviaba de la especificación técnica estricta de la guía.
* **Acepté la refactorización a semáforo (`TrafficLightFSM`):** Implementé la máquina de estados basándome en un mapeo limpio **`O(1)`** usando **`TrafficLightState`** (`Enum`), encapsulando de forma segura el contador de ciclos sin variables globales.
* **Acepté los 4 tests unitarios de pytest:** Validé de forma estricta los escenarios del ciclo de vida del semáforo: estado inicial, transición `RED -> GREEN`, ciclo completo de retorno a `RED`, y conteo exacto de ciclos acumulados.

---

## Prompt (Miércoles)

> Implementa los tres primeros principios SOLID (S, O y L) con el código base y las firmas exactas indicadas en la guía para `SensorReader`, `AlertStrategy`, `AnomalyDetector` y `process_sensor`.

### Respuesta

> Excelente. Enfrentamos los tres primeros principios de **SOLID** aplicados al dominio de IoT industrial:
>
> * **SRP:** Desacoplamos la lectura física del sensor (`SensorReader`) de la persistencia en disco (`DataLogger`).
> * **OCP:** Diseñamos clases de alertas que hereden de una clase abstracta `AlertStrategy` (`ABC`). Añadir `EmailAlert` no modificará las clases de negocio existentes.
> * **LSP:** Las subclases de sensores deben ser completamente intercambiables sin alterar la lógica de procesamiento en la función `process_sensor()`.

### Resultado / Aprendizaje

* **Rechacé la alteración de firmas y renombramiento de clases:** La primera propuesta de la IA sobre-diseñaba la solución y renombraba la función **`process_sensor`** a **`process_sensor_data`**, rompiendo los contratos del evaluador. Exigí respetar al 100% las firmas del documento base.
* **Acepté el desacoplamiento SRP, OCP y LSP corregido:** Implementé el desacoplamiento de lectura física respecto a persistencia (S), el diseño polimórfico de alertas ampliando el sistema sin modificar el detector de anomalías (O), y la compatibilidad nominal de sensores (L), validándolo con una suite de **6 pruebas unitarias**.

---

## Prompt (Jueves)

> Completa la biblioteca en `semana1/solid_isp_dip.py` dividiendo una interfaz gorda en `Readable`, `Writable` y `Calibratable` (ISP), y usando `Protocol` para inyectar un `DataRepository` en un `DataProcessor` (DIP), junto con una implementación `InMemoryRepository` para pruebas.

### Respuesta

> Para prepararte de cara a la defensa con el coordinador, estructuramos `semana1/solid_isp_dip.py` con interfaces pequeñas (`Readable`, `Writable`, `Calibratable`) para no obligar a sensores analógicos simples a implementar métodos fantasma de calibración (ISP).
>
> En DIP, hacemos que `DataProcessor` dependa del protocolo `DataRepository` en su constructor. En producción le inyectas Postgres; en los tests le inyectamos `InMemoryRepository` en RAM. El procesador jamás se entera.

### Resultado / Aprendizaje

* **Acepté la segregación de interfaces con Protocol (ISP):** Evité acoplar dispositivos simples a clases monolíticas que los obliguen a heredar métodos vacíos o inoperantes de calibración y escritura.
* **Acepté el desacoplamiento de persistencia (DIP):** Implementé el protocolo **`DataRepository`** inyectando opcionalmente el repositorio simulado en memoria **`InMemoryRepository`** en el constructor de **`DataProcessor`**. Esto permitió probar la lógica en milisegundos en la RAM de forma aislada.

---

## Prompt (Viernes)

> Genera el código y los tests para el driver UART modular (`config`, `parsers`, `device`, `recorder`) aplicando principios SOLID según las firmas especificadas en la guía del curso.

### Respuesta

> ¡Freno de mano puesto, vaquero! Reestructuramos el plan para usar exactamente la arquitectura estipulada de **4 clases principales**:
>
> 1. `config.py` (`UartConfig`, dataclass inmutable con validaciones de hardware).
> 2. `parsers.py` (Contrato abstracto `MessageParser`, `ModbusParser` y `NMEAParser`).
> 3. `device.py` (`UartDevice` con inyección de dependencias para aislar la UART).
> 4. `recorder.py` (`DataRecorder` dedicado a persistir en formato `.jsonl`).

### Resultado / Aprendizaje

* **Rechacé el sobre-diseño de la IA con concurrencia compleja:** Descarté el buffer circular por exclusión mutua de hilos y *lockings* complejos sugerido por el asistente, simplificando el alcance para cumplir estrictamente con los 4 archivos dictados por la especificación.
* **Rechacé y corregí el comportamiento de `can_parse()` en `ModbusParser`:** La IA proponía arrojar un error de valor (`raise ValueError`) si la trama de entrada era corta. Identifiqué que esto rompía LSP y OCP al interrumpir toda la tubería de análisis polimórfica en cascada. Lo corregí para retornar limpiamente **`False`**.
* **Corregí la inyección de tipos nulos con Mypy:** Identifiqué que inyectar **`config=None`** en el test violaba la aserción nominal tipada **`config: UartConfig`**. Modifiqué el test para instanciar un objeto de configuración real, logrando el verde de tipos.
