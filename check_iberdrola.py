import json
import requests
import os
import time

# === Configuración Telegram ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Parámetros ===
ESTADO_PATH = ".notificado"
tiempo_espera = 5   # segundos entre ciclos
ciclos = 60         # total = 5 minutos

# === Funciones ===

def notificar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            print("✅ Notificado por Telegram", flush=True)
        else:
            print("❌ Error en notificación:", response.text, flush=True)
    except Exception as e:
        print("❌ Excepción en Telegram:", e, flush=True)

def leer_estado():
    if not os.path.exists(ESTADO_PATH):
        return False
    with open(ESTADO_PATH, "r") as f:
        return f.read().strip() == "1"

def guardar_estado(valor):
    with open(ESTADO_PATH, "w") as f:
        f.write("1" if valor else "0")

def consultar_punto():
    url = "https://www.iberdrola.es/o/webclipb/iberdrola/puntosrecargacontroller/getListarPuntosRecarga"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Origin": "https://www.iberdrola.es",
        "Referer": "https://www.iberdrola.es/movilidad-electrica",
        "X-Requested-With": "XMLHttpRequest"
    }
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
        },
        "language": "es"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            disponibles = [
                punto for punto in data.get("entidad", [])
                if punto.get("cpStatus", {}).get("statusCode") == "AVAILABLE"
            ]
            return disponibles
        else:
            print("❌ Error HTTP:", response.status_code, flush=True)
            return []
    except Exception as e:
        print("❌ Excepción al consultar:", e, flush=True)
        return []

# === MAIN LOOP ===

print("🚀 Iniciando verificación de disponibilidad...", flush=True)
estado_notificado = leer_estado()

for i in range(ciclos):
    print(f"🔄 Ciclo {i+1}/{ciclos}", flush=True)
    puntos = consultar_punto()
    print(f"📊 Puntos disponibles: {len(puntos)}", flush=True)

    if puntos and not estado_notificado:
        mensaje = f"⚡ Punto disponible: {puntos[0]['locationData']['cuprName']}"
        notificar_telegram(mensaje)
        guardar_estado(True)
        estado_notificado = True

    elif not puntos and estado_notificado:
        print("🔁 Punto ya no está disponible. Reiniciando notificación...", flush=True)
        guardar_estado(False)
        estado_notificado = False

    time.sleep(tiempo_espera)

print("⏹️ Finalizado", flush=True)
