# Predictor Mundial FIFA 2026

Aplicación web desarrollada con Flask para visualizar información del Mundial FIFA 2026, incluyendo grupos, equipos clasificados, fixture, predicciones y un chatbot de apoyo.

## Características

- Visualización de grupos del Mundial 2026.
- Listado de equipos clasificados.
- Visualización del fixture de partidos.
- Predicciones de resultados.
- Interfaz web responsiva.
- Integración de banderas de las selecciones.
- Chatbot de asistencia para consultas del torneo.

## Tecnologías utilizadas

- Python
- Flask
- HTML5
- CSS3
- Git
- GitHub

## Estructura del proyecto

```text
mundial_app/
│
├── app.py
├── download_flags.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── flags/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── grupos.html
│   ├── equipos.html
│   ├── fixture.html
│   ├── predicciones.html
│   └── chatbot.html
│
└── README.md
```

## Instalación

1. Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

2. Entrar al proyecto:

```bash
cd mundial_app
```

3. Crear y activar entorno virtual:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

4. Instalar dependencias:

```bash
pip install flask requests
```

5. Ejecutar la aplicación:

```bash
python app.py
```

6. Abrir en el navegador:

```text
http://127.0.0.1:5000
```

## Integrantes

- Jaquelin Natalia Lorenzana León
- Salvador André Martínez Juárez

## Universidad

Universidad Mariano Gálvez de Guatemala

Proyecto académico desarrollado para el curso de Inteligencia Artificial.

## Estado del proyecto

En desarrollo.
Actualmente incluye grupos, equipos clasificados, sistema de banderas e interfaces principales.
