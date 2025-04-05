import requests
import json

# Coordenadas de tu zona (ajusta si hace falta)
payload = {
  "dto": {
    "chargePointTypesCodes": ["P", "R", "I", "N"],
    "socketStatus": [],
    "advantageous": False,
    "connectorsType": [],
    "loadSpeed": [],
    "latitudeMax": 38.4716227,
    "latitudeMin": 38.4703627,
    "longitudeMax": -0.7982563,
    "longitudeMin": -0.7996698
  },
  "language": "es"
}

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

url = "https://www.iberdrola.es/o/webclipb/iberdrola/puntosrecargacontroller/getListarPuntosRecarga"

try:
    print("Enviando petición a Iberdrola...")
    response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
    response.raise_for_status()
    data = response.json()

    disponibles = [p for p in data.get("lstPuntoRecarga", []) if p.get("statusCode") == "AVAILABLE"]

    if disponibles:
        print(f"¡Hay {len(disponibles)} puntos disponibles!")
        for p in disponibles:
            print(f"- {p['address']} ({p['name']})")
    else:
        print("No hay puntos disponibles por ahora.")

except Exception as e:
    print(f"Error al consultar el punto de carga: {e}")


