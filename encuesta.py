"""
Script de Análisis y Graficación para Encuestas de Investigación.

Tema general: Innovación Pedagógica y Práctica Docente en la Era Digital
Tema específico: Nivel de Integración pedagógica en las herramientas tecnológicas enfocada a los docente de secundaria en el Colegio Santa Luisa de Marillac para los estudiantes de undécimo año a durante el año 2025

Autor: Andres Francisco Sanchez Santana
Institución: Colegio Santa Luisa de Marillac, Managua, Nicaragua

Fecha de Creación: Septiembre 2025
Propósito: Procesa datos JSON de encuestas (respuestas cerradas) para calcular 
           frecuencias y porcentajes, y genera visualizaciones PNG con Matplotlib.
"""
import json
from collections import defaultdict
import matplotlib.pyplot as plt # type: ignore
import os
import re # Necesario para limpiar nombres de archivo

def analizar_encuesta_json(nombre_archivo):
    """
    Procesa el archivo JSON de la encuesta para calcular frecuencias y porcentajes.
    (Función original, modificada solo para incluir el porcentaje_valor numérico en el retorno)
    """
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return None, 0
    except json.JSONDecodeError:
        print(f"Error: El archivo '{nombre_archivo}' no es un JSON válido.")
        return None, 0

    total_encuestados = len(datos.get("Encuestados", []))
    if total_encuestados == 0:
        print("Advertencia: No hay encuestados en el archivo.")
        return {}, 0

    mapa_preguntas = {
        str(i + 1): {
            "pregunta": datos["questions"][i]["question"],
            "opciones": datos["questions"][i]["choises"]
        } for i in range(len(datos["questions"]))
    }
    conteo_respuestas = defaultdict(lambda: defaultdict(int))

    # --- FASE DE PROCESAMIENTO ---
    for encuestado in datos["Encuestados"]:
        for respuesta_obj in encuestado["Respuestas"]:
            pregunta_num = list(respuesta_obj.keys())[0]
            respuestas = list(respuesta_obj.values())[0]

            if not isinstance(respuestas, list):
                respuestas = [respuestas]

            for opcion_indice in respuestas:
                conteo_respuestas[pregunta_num][opcion_indice] += 1

    # --- FASE DE RESULTADOS Y CÁLCULO DE PORCENTAJES ---
    resultados_finales = {}

    for q_num, conteos in conteo_respuestas.items():
        info_q = mapa_preguntas.get(q_num, {})
        resultados_q = {}
        
        for indice_opcion, conteo in conteos.items():
            indice_opcion_cero = int(indice_opcion) - 1
            
            try:
                texto_opcion = info_q["opciones"][indice_opcion_cero]
            except IndexError:
                texto_opcion = f"Opción {indice_opcion} (No definida)"

            porcentaje = (conteo / total_encuestados) * 100

            resultados_q[texto_opcion] = {
                "conteo": conteo,
                "porcentaje_valor": porcentaje, # AÑADIDO: Valor numérico para Matplotlib
                "porcentaje_formato": f"{porcentaje:.2f}%"
            }

        resultados_finales[q_num] = {
            "pregunta": info_q.get("pregunta", "Pregunta Desconocida"),
            "resultados": resultados_q
        }

    return resultados_finales, total_encuestados

# ----------------------------------------------------------------------
# --- FUNCIÓN PARA GENERAR GRÁFICOS ---
# ----------------------------------------------------------------------

def generar_grafico_barras(q_num, resultados_q, total_encuestados):
    """Crea y guarda un gráfico de barras horizontales para una pregunta específica."""
    
    pregunta = resultados_q["pregunta"]
    
    # Extraer etiquetas (opciones) y valores (porcentajes)
    etiquetas = list(resultados_q["resultados"].keys())
    valores_porcentuales = [data["porcentaje_valor"] for data in resultados_q["resultados"].values()]
    
    # 1. Limpiar la etiqueta para usarla en el nombre del archivo
    # Solo tomamos las primeras 5 palabras y removemos caracteres especiales.
    titulo_limpio = "_".join(pregunta.split(' ')[:5])
    nombre_archivo_base = f"P{q_num}_{re.sub(r'[^a-zA-Z0-9_]', '', titulo_limpio)}" 
    
    plt.figure(figsize=(10, 6)) # Define el tamaño del gráfico

    # Barras horizontales (plt.barh) para mejor lectura de etiquetas largas
    barras = plt.barh(etiquetas, valores_porcentuales, color='#0077b6') 
    
    # Añadir el valor porcentual sobre cada barra
    for barra in barras:
        ancho = barra.get_width()
        plt.text(ancho + 0.5, barra.get_y() + barra.get_height()/2, 
                 f'{ancho:.1f}%', va='center')

    plt.xlabel('Porcentaje de Docentes (%)')
    plt.title(f'P{q_num}: {pregunta}\n(N={total_encuestados})', fontsize=12)
    # El límite máximo es 100 o un poco más si es una pregunta de respuesta múltiple (aunque eso es poco probable con N=5)
    plt.xlim(0, max(100, max(valores_porcentuales) + 10)) 
    
    # Invertir el orden para que la primera opción esté arriba
    plt.gca().invert_yaxis()
    plt.tight_layout() # Ajusta el diseño para que las etiquetas no se corten
    
    # Crear la carpeta 'graficos' si no existe
    if not os.path.exists('graficos'):
        os.makedirs('graficos')
    
    ruta_guardado = os.path.join('graficos', f'{nombre_archivo_base}.png')
    plt.savefig(ruta_guardado)
    plt.close() # Cierra la figura para liberar memoria
    
    print(f"✅ Gráfico generado y guardado en: {ruta_guardado}")


# --- EJECUCIÓN DEL SCRIPT Y AGRUPACIÓN DE DATOS ---

nombre_archivo_encuesta = 'Encuesta.json' 
resultados, total = analizar_encuesta_json(nombre_archivo_encuesta)

if resultados:
    print(f"\n--- Análisis Cuantitativo de la Encuesta (N={total}) ---\n")

    # Definimos qué preguntas vamos a graficar (las más relevantes para el análisis)
    preguntas_a_graficar = [
        '3',
        '4',
        '7',
        '8',
        '10',
        '11',
        '12',
    ]

    # Recorremos los resultados para mostrarlos en consola y generar gráficos
    for k in resultados.keys():
        print(f"\n--- Pregunta {k}: {resultados[k]['pregunta']} ---")
        
        # Mostrar los resultados en consola
        for opcion, data in resultados[k]['resultados'].items():
            print(f"  - {opcion}: {data['conteo']} ({data['porcentaje_formato']})")
        
        # Generar gráfico si está en la lista de prioridades
        if k in preguntas_a_graficar:
            generar_grafico_barras(k, resultados[k], total)
            
    print("\nProceso de análisis completado. Los gráficos se encuentran en la carpeta 'graficos'.")