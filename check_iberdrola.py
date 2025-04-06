import requests
import os
import time
import json
import sys

# Mostrar print en tiempo real
sys.stdout.reconfigure(line_buffering=True)

# Configuración Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def esta_activo():
    try:
        with open("estado.txt", "r") as f:
            estado = f.read().strip().lower()
            return estado == "activo"
    except FileNotFoundError:
        return False

def notificar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Notificado por Telegram")
        else:
            print("❌ Error en notificación:", response.text)
    except Exception as e:
        print("❌ Excepción en Telegram:", e)

if not esta_activo():
    print("🛑 Monitorización desactivada. No se realiza búsqueda.")
    exit()
print("✅ Monitorización activada. Realizando búsqueda...")

def consultar_punto():
    url = "https://www.iberdrola.es/o/webclipb/iberdrola/puntosrecargacontroller/getListarPuntosRecarga"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://www.iberdrola.es",
        "Referer": "https://www.iberdrola.es/movilidad-electrica",
        "X-Requested-With": "XMLHttpRequest"
    }

    # Coordenadas del punto de carga
    payload = {
        "dto": {
            "chargePointTypesCodes": ["P", "R", "I", "N"],
            "socketStatus": [],
            "advantageous": False,
            "connectorsType": [],
            "loadSpeed": [],
            "latitudeMax": 38.47133335593224,
            "latitudeMin": 38.47070336704179,
            "longitudeMax": -0.7981991849749259,
            "longitudeMin": -0.7993216894476585
           # "latitudeMax":38.493634489628164,"latitudeMin":38.4533165765376,"longitudeMax":-0.7698327166954999,"longitudeMin":-0.8416730029503827
        },
        "language": "es"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
        if response.status_code == 200:
            data = response.json()
            disponibles = [
                punto for punto in data.get("entidad", [])
                if punto.get("cpStatus", {}).get("statusCode") == "AVAILABLE"
            ]
            return disponibles
        else:
            print("❌ Error HTTP:", response.status_code)
            return []
    except Exception as e:
        print("❌ Excepción al consultar:", e)
        return []

# 🔁 MAIN LOOP
notificado = False
tiempo_espera = 5  # segundos
ciclos = 720        # total 10 minutos

print("🚀 Iniciando verificación de disponibilidad...")
for i in range(ciclos):
    print(f"🔄 Ciclo {i + 1}/{ciclos}")
    puntos = consultar_punto()
    print(f"📊 Puntos disponibles: {len(puntos)}")
    if puntos and not notificado:
        mensaje = f"⚡ Punto disponible: {puntos[0]['locationData']['cuprName']}"
        notificar_telegram(mensaje)
        notificado = True
    elif not puntos:
        notificado = False  # Reset si se ocupa
    time.sleep(tiempo_espera)

print("⏹️ Finalizado")
