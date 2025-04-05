import requests
import json

# URL del endpoint
url = "https://www.iberdrola.es/o/webclipb/iberdrola/puntosrecargacontroller/getListarPuntosRecarga"

# Payload con coordenadas (ajústalas según la zona que quieras consultar)
payload = {
    "dto": {
        "chargePointTypesCodes": ["P", "R", "I", "N"],
        "socketStatus": [],
        "advantageous": False,
        "connectorsType": [],
        "loadSpeed": [],
      #    "latitudeMax": 38.4716227,
      #   "latitudeMin": 38.4703627,
      #   "longitudeMax": -0.7982563,
      #   "longitudeMin": -0.7996698
     # "latitudeMax":38.47186625660738,
     # "latitudeMin":38.47018628641727,
     # "longitudeMax":-0.799357454367684,
     # "longitudeMin":-0.8010847969732748
        "latitudeMax":38.47580637031306,"latitudeMin":38.47454646519379,"longitudeMax":-0.7700730395413236,"longitudeMin":-0.7723180484867886

    },
    "language": "es"
}

# Encabezados requeridos por Iberdrola
headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": "https://www.iberdrola.es",
    "Referer": "https://www.iberdrola.es/movilidad-electrica/puntos-de-recarga",
    "X-Requested-With": "XMLHttpRequest"
}

print("Enviando petición a Iberdrola...")

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
    response.raise_for_status()
    data = response.json()

    puntos_disponibles = []

    for punto in data.get("entidad", []):
        status = punto.get("cpStatus", {}).get("statusCode")
        if status == "AVAILABLE":
            direccion = punto["locationData"]["supplyPointData"]["cpAddress"]
            puntos_disponibles.append(f"{direccion.get('streetName')} {direccion.get('streetNum')}, {direccion.get('townName')}")

    if puntos_disponibles:
        print("⚡ Puntos de carga disponibles:")
        for d in puntos_disponibles:
            print(f" - {d}")
    else:
        print("❌ No hay puntos disponibles por ahora.")

except Exception as e:
    print("Error al consultar el punto de carga:", e)

