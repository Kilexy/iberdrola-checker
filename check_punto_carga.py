import requests

PUNTO_ID = 97896
URL = "https://www.iberdrola.es/o/webclipb/iberdrola/puntosrecargacontroller/getDatosPuntoRecarga"
HEADERS = {
    "Content-Type": "application/json"
}
PAYLOAD = {
    "dto": {"cuprId": [PUNTO_ID]},
    "language": "es"
}

def check_port():
    try:
        response = requests.post(URL, json=PAYLOAD, headers=HEADERS, timeout=10)
        data = response.json()
        conectores = data["listaConectores"]

        for conector in conectores:
            estado = conector.get("estadoConector", "").lower()
            if "libre" in estado:
                print("¡Hay un conector LIBRE!")
                return True

        print("No hay conectores libres. Seguimos comprobando...")
        return False

    except Exception as e:
        print(f"Error al consultar el punto de carga: {e}")
        return False

if __name__ == "__main__":
    check_port()
