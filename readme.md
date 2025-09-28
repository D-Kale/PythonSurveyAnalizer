# 📊 Analizador y Generador de Gráficos de Encuestas Docentes

## 👤 Autoría
Este script de análisis fue diseñado y desarrollado íntegramente por Andrés Sanchez, Nicaragua como parte de su proceso de analisis de informacion para la realizacion de una investigacion documental con el tema general *Innovación Pedagógica y Práctica Docente en la Era Digital*.

Creador del Código: Andrés Francisco Sanchez Santana

Contacto: [Github](https://github.com/D-Kale)

## Finalidad del proyecto
Este proyecto contiene un script en Python (analizador_con_graficos.py) diseñado para automatizar el análisis cuantitativo de una encuesta de investigación documental. El script lee datos de respuesta en formato JSON, calcula las frecuencias y porcentajes, e inmediatamente genera gráficos de barras PNG para las preguntas clave, facilitando la interpretación y presentación de resultados.

## 🚀 Requisitos del Sistema
Para ejecutar este script, necesitas tener instalado Python y la librería de visualización matplotlib.

- Python: Versión 3.x.

- Librería Matplotlib: Instálala usando pip:

## Bash
```
pip install matplotlib
```
## 📁 Estructura del Proyecto
Asegúrate de que los dos archivos principales se encuentren en el mismo directorio:

```
/tu_proyecto_investigacion
├── encuesta.py  <-- El script de Python.
└── Encuesta.json              <-- Archivo con los datos de las respuestas.
```

Al ejecutar el script, se creará una carpeta de salida:

```
/tu_proyecto_investigacion
├── ...
└── /graficos                  <-- Carpeta generada automáticamente con los PNG.
```

## 💾 Estructura del Archivo de Entrada (Encuesta.json)
El script requiere que el archivo Encuesta.json siga una estructura estricta, dividida en la definición de preguntas (questions) y las respuestas de los encuestados (Encuestados).

1. Clave questions (Definición de Preguntas)
Aquí se definen las preguntas y sus opciones de respuesta, lo que permite al script mapear los índices numéricos a texto.

    | **Campo** | **Tipo** | **Descripción** |
    |-----------|----------|-----------------|
    | `question` | `string` | El texto completo de la pregunta |
    | `choices` | `array` | Una lista de strings con todas las opciones de respuesta |

2. Clave Encuestados (Respuestas)
Aquí se ingresan las respuestas transcritas de cada cuestionario en papel. Las respuestas se registran usando el índice de la opción (base 1).

    | **Campo** | **Tipo** | **Descripción** |
    |-----------|----------|-----------------|
    | `id` | `integer` | Identificador único del encuestado (ej: 1, 2, 3...). |
    | `Respuestas` | `array` | Lista de objetos, donde cada objeto contiene la respuesta a una pregunta. |
    | `Clave` | `string` | El número de pregunta (ej: "1", "2", "3"). |
    | `Valor` | `string` o `array` | El índice de la opción seleccionada. Debe ser un string para respuestas únicas (ej: "4") o un array de string para respuestas múltiples (ej: ["1", "4", "6"]). |

## Ejemplo de Estructura JSON

```
{
    "questions": [
        {
            "question": "¿Que nivel educativo imparte?",
            "choises": ["Preescolar", "Primaria", "Secundaria", "Educacion Tecnica", "Universidad", "Otro"]
        },
        // ... (Preguntas 2 a 13)
    ],
    "Encuestados": [
        {
            "id": 1,
            "Respuestas": [
                {"1": ["4", "5"]},      
                // Pregunta 1: Opción 4 ("Educacion Tecnica") y Opción 5 ("Universidad")
                {"2": "4"},             
                // Pregunta 2: Opción 4 ("Mas de 10 años")
                {"3": "1"},             
                // Pregunta 3: Opción 1 ("Si, frecuentemente")
                // ... (Otras preguntas)
            ]
        }
        // ... (Otros encuestados)
    ]
}

```
## ⚙️ Instrucciones de Uso
- Preparar el JSON: Asegúrate de que tu archivo Encuesta.json contenga la estructura correcta con todas las respuestas transcritas.

- Abrir la Terminal: Navega hasta el directorio donde guardaste ambos archivos (analizador_con_graficos.py y Encuesta.json).

- Ejecutar el Script:

### Bash
```
python encuesta.py
```

## Personalización de Gráficos
El script incluye una lista llamada preguntas_a_graficar que define qué preguntas se visualizan. Por defecto, solo se grafican las preguntas de uso, beneficios y desafíos.

Para graficar todas las preguntas (1 a n), puedes modificar esta lista en el script de la siguiente manera:

### Python
```
preguntas_a_graficar = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'
]
```

## 📦 Salida del Script
- Consola: El script imprime en la terminal un resumen del análisis con el conteo y el porcentaje de cada respuesta.

- Archivos PNG: Se crea la carpeta /graficos, donde se guardan los gráficos de barras horizontales (en formato PNG) para las preguntas seleccionadas. Cada gráfico está nombrado con el número de pregunta y una parte de su título (ej: P4_Herramientas_tecnologicas.png).