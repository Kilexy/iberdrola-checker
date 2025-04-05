import time
import requests
from bs4 import BeautifulSoup

# CONFIGURA AQUÍ:
URL = "https://www.iberdrola.es/o/webclipb/iberdrola/puntosrecargacontroller/getDatosPuntoRecarga"
BOT_TOKEN = "8102593995:AAExuxIBZmPtuIOjBZqjT10KitpSKh-7RI8"
CHAT_ID = "6275686013"

def obtener_estado_cargador():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        print("❌ Error al acceder a la página.")
        return False

    soup = BeautifulSoup(response.text, "html.parser")

    # Cambia esto según la web exacta del punto
    if "libre" in soup.text.lower():
        return True
    return False

def enviar_notificacion(mensaje):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": mensaje}
    )

print("🔍 Iniciando revisión de punto de carga...")

if obtener_estado_cargador():
    print("✅ ¡Cargador disponible! Enviando notificación.")
    enviar_notificacion("⚡ Punto de carga disponible en Iberdrola!")
else:
    print("⛔ Sin disponibilidad. Esperando siguiente intento.")
