import requests
import pymysql
import json

# Configuración
API_KEY = "3c0c907dce1fe67efdaa8f93895"  # Tu clave API-Football
BASE_URL = "https://v3.football.api-sports.io/fixtures"
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io"}
START_DATE = "2022-09-01"
END_DATE = "2025-01-14"  # Cambia si quieres ajustar la fecha
OUTPUT_SQL = "datos_historicos.sql"

# Función para obtener datos
def obtener_partidos(fecha_inicio, fecha_fin):
    url = f"{BASE_URL}?date_from={fecha_inicio}&date_to={fecha_fin}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        return data.get("response", [])
    else:
        print(f"Error al conectar a la API: {response.status_code}")
        return []

# Función para crear el archivo SQL
def generar_sql(datos):
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS partidos_historicos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            equipo_local VARCHAR(255),
            equipo_visitante VARCHAR(255),
            estadio VARCHAR(255),
            ciudad VARCHAR(255),
            fecha DATE,
            goles_local INT,
            goles_visitante INT
        );"""
    ]

    for partido in datos:
        fixture = partido["fixture"]
        teams = partido["teams"]
        goals = partido["goals"]

        equipo_local = teams["home"]["name"]
        equipo_visitante = teams["away"]["name"]
        estadio = fixture["venue"]["name"] or "Desconocido"
        ciudad = fixture["venue"]["city"] or "Desconocida"
        fecha = fixture["date"][:10]
        goles_local = goals["home"] if goals["home"] is not None else "NULL"
        goles_visitante = goals["away"] if goals["away"] is not None else "NULL"

        sql_statements.append(
            f"""INSERT INTO partidos_historicos (equipo_local, equipo_visitante, estadio, ciudad, fecha, goles_local, goles_visitante)
            VALUES ("{equipo_local}", "{equipo_visitante}", "{estadio}", "{ciudad}", "{fecha}", {goles_local}, {goles_visitante});"""
        )

    with open(OUTPUT_SQL, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_statements))

    print(f"Archivo SQL generado: {OUTPUT_SQL}")

# Ejecutar
if __name__ == "__main__":
    print("Obteniendo datos históricos...")
    partidos = obtener_partidos(START_DATE, END_DATE)
    if partidos:
        print(f"Datos obtenidos: {len(partidos)} partidos.")
        generar_sql(partidos)
    else:
        print("No se obtuvieron datos.")
