import os 
import json 
import sqlite3
import requests
import numpy as np
import pandas as pd

from datetime import datetime
from prefect import task, flow
 

def cargar_json():
    try:
        ruta_archivo = os.path.join(os.path.dirname(__file__), "Traducc_Desc.json")
        print(f"Ruta del archivo JSON: {ruta_archivo}")
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            clima_data = json.load(f)
        print("Contenido cargado :", clima_data.keys()) 
        API_KEY = clima_data["API_KEY"]
        Traducciones = clima_data["Traducciones"]
        Descripciones = clima_data["Descripciones"]
        return API_KEY, Traducciones, Descripciones
    except Exception as e:
        print(f"Error al cargar el archivo JSON: {e}")
        raise

def get_clima (Ciudad, API_KEY, units:str = 'metric' ):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={Ciudad}&appid={API_KEY}&units={units}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")
    
def transformar_datos(json_data, Traducciones, Descripciones):
    clima_en = json_data["weather"][0]["main"]
    descripcion_en = json_data["weather"][0]["description"]

    clima_es = Traducciones.get(clima_en, clima_en) 
    descripcion_es = Descripciones.get(descripcion_en.lower(), descripcion_en).capitalize()  

    datos = {
        "Ciudad": json_data.get("name"),
        "Fecha y Hora": datetime.fromtimestamp(json_data["dt"]),
        "Temperatura": json_data["main"]["temp"],
        "Sensación Térmica": json_data["main"]["feels_like"],
        "Humedad": json_data["main"]["humidity"],
        "Presión": json_data["main"]["pressure"],
        "Clima": clima_es,
        "Descripción": descripcion_es
    }

    df = pd.DataFrame([datos])
    return df

CIUDADES = ['Buenos Aires', 'Cordoba', 'Santa Fe', 'Mendoza', 'Salta', 'Entre Rios', 'San Luis', 'San Juan', 'Neuquen', 'La Rioja', 'Misiones']

def analizar_datos(directorio="datos/raw"):
    archivos = [f for f in os.listdir(directorio) if f.endswith(".csv")]
    if not archivos:
        print("No hay archivos CSV para analizar.")
        return None

    dfs = [pd.read_csv(os.path.join(directorio, f)) for f in archivos]
    df_total = pd.concat(dfs, ignore_index=True)
    df = df_total.copy()

    temp_prom = df.groupby('Ciudad')['Temperatura'].mean().round(2)
    sens_prom = df.groupby('Ciudad')['Sensación Térmica'].mean().round(2)
    humedad_prom = df.groupby('Ciudad')['Humedad'].mean().round(2)

    df['Diferencia termica'] = abs(df['Temperatura'] - df['Sensación Térmica'])
    df_ter_prom = df.groupby('Ciudad')['Diferencia termica'].mean().round(2)

    resumen_ciudades = pd.DataFrame({
        'Temperatura promedio (°C)': temp_prom,
        'Sensacion termica promedio (°C)': sens_prom,
        'Humedad promedio (%)': humedad_prom,
        'Diferencia termica promedio (°C)': df_ter_prom
    }).sort_index()

    temperaturas = df['Temperatura'].to_numpy()
    media = np.mean(temperaturas)
    std = np.std(temperaturas)
    max_temp = np.max(temperaturas)
    min_temp = np.min(temperaturas)

    fuera_de_rango = df[(df['Temperatura'] < media - std) | (df["Temperatura"] > media + std)]         
    cantidad_fuera = len(fuera_de_rango)
    porcentaje_fuera = round((cantidad_fuera / len(df)) * 100, 2 )
   
    resumen_global = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Temperatura media": round(media, 2),
        "Desvio estandar": round(std, 2),
        "Temp maxima": round(max_temp, 2),
        "Temp minima": round(min_temp, 2),
        "Registros fuera de rango": cantidad_fuera,
        "Porcentaje fuera de rango": porcentaje_fuera
    }])

    guardar_en_sqlite({
        "resumen_clima": resumen_ciudades,
        "resumen_global": resumen_global
    })

    return resumen_ciudades

def guardar_en_sqlite(dataframes:dict , db_path="datos/analisis.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)

    for tabla, df in dataframes.items():
        if df is not None and not df.empty:
            df.reset_index(drop=True, inplace=True)
            df.to_sql(tabla, conn, if_exists='append' if tabla== "resumen_global" else "replace", index=False)
            print (f"Datos guardados en la tabla {tabla}")
        else:
            print(f"No se guardaron datos en la tabla")
    conn.close()

@task(
        retries = 3,
        retry_delay_seconds = 60
)
def extraer_datos(API_KEY, Traducciones, Descripciones):
    datos = []
    for ciudad in CIUDADES:
        try:
            json_data = get_clima(ciudad, API_KEY)
            df = transformar_datos(json_data, Traducciones, Descripciones)
            datos.append(df)
        except Exception as e:
            print(f"Error con {ciudad}: {e}")
    return pd.concat(datos, ignore_index=True)

@task
def guardar_csv(df):
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    ruta_direc = "datos/raw"
    os.makedirs(ruta_direc, exist_ok=True)
    ruta = f"{ruta_direc}/clima_{fecha}.csv"
    df.to_csv(ruta, index=False, encoding='utf-8')
    print(f"Datos guardados en {ruta}")

@task
def verificacion(directorio="datos/raw", umbral=15):
    try:
        archivos = [f for f in os.listdir(directorio) if f.endswith(".csv")]
    except Exception as e:
        print(f"Error al listar archivos: {e}")
        return
    
    if len(archivos)>=umbral:
        print(f"Se encontraron {len(archivos)} archivos, Iniciando analisis.")
        analizar_datos(directorio)
    else:
        print(f"Solo hay {len(archivos)} archivos. Se esperan al menos {umbral}")

@flow
def flujo_clima_diario():
    API_KEY, Traducciones, Descripciones = cargar_json()
    df = extraer_datos(API_KEY, Traducciones, Descripciones)
    guardar_csv(df)
    verificacion()
