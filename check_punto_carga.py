import requests
import time

PUNTO_ID = 97896  # ID del punto que quieres monitorear

def consultar_estado():
    url = "https://www.iberdrola.es/o/webclipb/iberdrola/puntosrecargacontroller/getDatosPuntoRecarga"
    payload = {
        "dto": {"cuprId": [PUNTO_ID]},
        "language": "es"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            punto = data["lstPuntos"][0]
            libres = punto.get("libres", 0)
            total = punto.get("total", 0)
            print(f"[{time.ctime()}] Dirección: {punto.get('direccion')} - Libres: {libres}/{total}")
            return libres > 0
        else:
            print(f"Error al obtener datos: {response.status_code}")
    except Exception as e:
        print(f"Excepción al hacer la solicitud: {e}")
    return False

# Para prueba simple
if _name_ == "_main_":
    disponible = consultar_estado()
    if disponible:
        print("¡Hay cargadores disponibles!")
    else:
        print("No hay disponibles por ahora.")
