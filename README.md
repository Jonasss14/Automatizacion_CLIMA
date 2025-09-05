# Sistema de Monitoreo Climático para Ciudades Argentinas 🌤️

## Descripción
Este proyecto implementa un sistema automatizado de monitoreo climático que recolecta, procesa y analiza datos meteorológicos en tiempo real de las principales ciudades de Argentina. Utilizando la API de OpenWeather, el sistema genera informes detallados y almacena datos históricos para su posterior análisis.

## Características principales 🌟
- Monitoreo en tiempo real de 11 ciudades argentinas
- Traducción automática de condiciones climáticas (inglés a español)
- Análisis estadístico de datos climáticos
- Almacenamiento en base de datos SQLite
- Sistema de flujo de trabajo automatizado con Prefect
- Manejo de errores y reintentos automáticos
- Generación de reportes CSV

## Ciudades monitoreadas 🏙️
- Buenos Aires
- Córdoba
- Santa Fe
- Mendoza
- Salta
- Entre Ríos
- San Luis
- San Juan
- Neuquén
- La Rioja
- Misiones

## Tecnologías utilizadas 🛠️
- Python 3.12
- Pandas para análisis de datos
- NumPy para cálculos estadísticos
- SQLite para almacenamiento persistente
- Prefect para orquestación de flujos de trabajo
- Requests para consumo de API
- JSON para configuración

## Requisitos previos 📋
```bash
pip install -r requirements.txt
```

## Estructura del proyecto 📁
```
CLIMA/
├── Clima.py              # Script principal
├── requirements.txt      # Dependencias del proyecto
├── Traducc_Desc.json    # Configuración y traducciones
└── datos/
    ├── analisis.db      # Base de datos SQLite
    └── raw/             # Archivos CSV con datos crudos
```

## Funcionalidades principales 🔍

### 1. Extracción de datos
- Conexión con la API de OpenWeather
- Recopilación de datos meteorológicos en tiempo real
- Sistema de reintentos en caso de fallos

### 2. Procesamiento de datos
- Traducción automática de condiciones climáticas
- Transformación y limpieza de datos
- Cálculo de métricas derivadas

### 3. Análisis estadístico
- Temperatura promedio por ciudad
- Sensación térmica promedio
- Humedad promedio
- Diferencia térmica promedio
- Detección de valores fuera de rango
- Cálculo de desviación estándar

### 4. Almacenamiento
- Generación de archivos CSV con timestamp
- Base de datos SQLite con resúmenes
- Histórico de datos para análisis temporal

## Métricas calculadas 📊
- Temperatura promedio (°C)
- Sensación térmica promedio (°C)
- Humedad promedio (%)
- Diferencia térmica promedio (°C)
- Registros fuera de rango estadístico
- Porcentaje de datos atípicos

## Configuración ⚙️
El archivo `Traducc_Desc.json` contiene:
- API KEY de OpenWeather
- Diccionario de traducciones de condiciones climáticas
- Descripciones detalladas del clima

## Automatización 🤖
El proyecto utiliza Prefect para:
- Programación de tareas periódicas
- Manejo de errores y reintentos
- Monitoreo de ejecución
- Orquestación de flujos de datos

## Autor ✒️
- **Jonas Luna**
- GitHub: [@Jonasss14](https://github.com/Jonasss14)

## Notas 📝
- El sistema está configurado para analizar los datos cuando se acumulan 15 archivos CSV
- Los datos se recopilan en intervalos regulares
- Todos los timestamps están en hora local
- Los datos se almacenan en formato UTF-8

---
Desarrollado con ❤️ para monitoreo climático en Argentina
