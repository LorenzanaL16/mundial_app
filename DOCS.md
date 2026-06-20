# Documentación Técnica - Predictor Mundial FIFA 2026

## 1. Arquitectura del Sistema

El sistema está compuesto por cuatro módulos principales:

### Frontend

Desarrollado con HTML5, CSS3 y JavaScript.

Permite al usuario:

* Consultar grupos del Mundial 2026.
* Visualizar equipos participantes.
* Revisar el fixture.
* Obtener predicciones.
* Consultar estadísticas.
* Interactuar con el chatbot.

### Backend

Implementado con Flask.

Funciones principales:

* Gestionar rutas web.
* Procesar solicitudes del usuario.
* Consultar información almacenada.
* Integrar el modelo de Machine Learning.
* Generar respuestas para el chatbot.

### Base de Datos

Se utiliza SQLite mediante el archivo:

```text
mundial.db
```

La base de datos almacena información relacionada con equipos, partidos, estadísticas y predicciones.

### Modelo de Inteligencia Artificial

El sistema utiliza un modelo de clasificación entrenado con Scikit-Learn.

Archivo:

```text
model.pkl
```

El modelo es utilizado para generar predicciones automáticas de resultados de partidos.

### Chatbot

El chatbot funciona mediante reconocimiento de palabras clave y respuestas predefinidas.

Permite responder preguntas relacionadas con:

* Equipos participantes.
* Grupos.
* Fixture.
* Predicciones.
* Estadísticas.
* Información general del Mundial.

---

## 2. Dataset

### Fuente

International Football Results Dataset

https://kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017

### Descripción

El dataset contiene resultados históricos de partidos internacionales de selecciones nacionales desde 1872 a 2017.

**Número de registros:** 49,477 (49,433 después de eliminar nulos)

### Variables utilizadas

* home_score
* away_score
* goal_diff

### Ingeniería de características

Se creó una nueva variable denominada:

```python
goal_diff = home_score - away_score
```

que representa la diferencia de goles entre ambos equipos.

### Variable objetivo

```text
result
```

Donde:

* 1 = Victoria local
* 0 = Empate
* 2 = Victoria visitante

### Limpieza de datos

Se realizaron las siguientes tareas:

* Eliminación de registros nulos mediante `dropna()`.
* Creación de variables derivadas.
* Preparación de datos para entrenamiento.

---

## 3. Modelo y Métricas

### Algoritmo seleccionado

Random Forest Classifier.

### Justificación

Se eligió este algoritmo debido a:

* Buen desempeño en problemas de clasificación.
* Capacidad para manejar grandes cantidades de datos.
* Robustez frente al ruido.
* Facilidad de implementación.

### División de datos

El conjunto de datos fue dividido en:

* 80% entrenamiento.
* 20% prueba.

Utilizando:

```python
train_test_split(test_size=0.2, random_state=42)
```

### Configuración del modelo

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
```

### Métricas utilizadas

Para evaluar el desempeño del modelo se utilizaron:

* Accuracy
* F1-Score (macro)

### Resultados

Accuracy: 1.0

F1-Score: 1.0

*(Resultados obtenidos al ejecutar model.py con el dataset actual)*

---

## 4. Chatbot

### Funcionamiento

El chatbot utiliza una lógica basada en reconocimiento de palabras clave y patrones específicos dentro de las preguntas del usuario. Cuando identifica una consulta válida, genera una respuesta utilizando la información almacenada en la aplicación.

### Preguntas reconocidas

| No. | Pregunta reconocida                     |
| --- | --------------------------------------- |
| 1   | ¿Cuándo juega México?                   |
| 2   | ¿Cuántos equipos participan?            |
| 3   | ¿Quiénes son los favoritos del Mundial? |
| 4   | ¿Cuál es el ranking de México?          |
| 5   | ¿En qué grupo está España?              |
| 6   | ¿En qué grupo está Brasil?              |
| 7   | ¿A qué grupo pertenece Alemania?        |
| 8   | ¿Quién ganará el Grupo A?               |
| 9   | ¿Cuántos mundiales ha ganado Brasil?    |
| 10  | ¿Quién será el campeón del Grupo C?     |
| 11  | ¿En qué puesto está Argentina en FIFA?  |
| 12  | ¿Cuál es la precisión del modelo?       |

### Proceso de respuesta

1. El usuario escribe una pregunta.
2. El chatbot normaliza el texto recibido.
3. Se buscan palabras clave relacionadas con las preguntas reconocidas.
4. Si existe coincidencia, se genera una respuesta correspondiente.
5. Si no existe coincidencia, el chatbot muestra un mensaje indicando que no comprende la consulta.

### Objetivo

El chatbot fue diseñado para complementar la experiencia del usuario dentro del sistema, proporcionando información rápida sobre el Mundial FIFA 2026, equipos participantes, grupos, estadísticas y resultados generados por el modelo de Inteligencia Artificial.

---

## 5. Guía de Uso

### Inicio

1. Acceder a `http://localhost:5000` o la URL del servidor.
2. La página principal muestra un menú de navegación con opciones principales.

### Grupos

1. Hacer clic en "Grupos" en el menú superior.
2. Se visualizan los 12 grupos (A-L) con los 4 equipos de cada grupo.

### Equipos

1. Hacer clic en "Equipos" en el menú superior.
2. Se muestran los 48 equipos participantes con ranking FIFA.

### Fixture

1. Hacer clic en "Fixture" en el menú superior.
2. Se lista el calendario de todos los partidos de grupo.

### Predicciones

1. Hacer clic en "Predicciones" en el menú superior.
2. Se muestran todas las predicciones de partidos con probabilidades.
3. **Filtrar resultados:**
   - Seleccionar "Grupo" (A-L) o dejar vacío para todos.
   - Ingresar nombre del equipo en el campo "Equipo" (ej: Argentina, México).
   - Establecer probabilidad mínima en "Min Prob (%)".
   - Hacer clic en "Filtrar".
4. Cada tarjeta muestra:
   - Enfrentamiento entre equipos.
   - Probabilidad de victoria local (%).
   - Probabilidad de empate (%).
   - Probabilidad de victoria visitante (%).

### Tabla de Posiciones

1. Hacer clic en "Tabla" en el menú superior.
2. Visualizar clasificación simulada por grupo.

### Estadísticas

1. Hacer clic en "Estadísticas" en el menú superior.
2. Información histórica de selecciones y datos relevantes.

### Chatbot

1. Hacer clic en "Chatbot" en el menú superior.
2. Escribir una pregunta en el campo de entrada.
3. El chatbot reconoce palabras clave y devuelve respuestas inmediatas.
4. **Ejemplos de preguntas:**
   - "¿Qué probabilidad tiene Argentina de ganar?"
   - "¿Cuándo juega México?"
   - "¿Quién ganará el Grupo A?"
   - "¿Cuántos mundiales ha ganado Brasil?"
5. Hacer clic en "Nuevo chat" para borrar el historial (se guarda en localStorage).

---

## 6. Conclusiones

El proyecto integra desarrollo web, bases de datos e Inteligencia Artificial para proporcionar una plataforma interactiva de análisis y simulación del Mundial FIFA 2026.

La aplicación demuestra la integración de Machine Learning dentro de un entorno web desarrollado con Flask, permitiendo generar predicciones y mejorar la experiencia del usuario mediante un chatbot interactivo.
