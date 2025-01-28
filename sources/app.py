import requests

# URL de la API
API_URL = "http://localhost:3000/api/simulaciones"

# Función para guardar una simulación
def guardar_simulacion(angulo1, angulo2, peso):
    datos = {
        "angulo1": angulo1,
        "angulo2": angulo2,
        "peso": peso
    }
    response = requests.post(f"{API_URL}", json=datos)
    if response.status_code == 201:
        print("Simulación guardada exitosamente.")
    else:
        print("Error al guardar la simulación:", response.json())

# Función para cargar una simulación
def cargar_simulacion(id_simulacion):
    response = requests.get(f"{API_URL}/{id_simulacion}")
    if response.status_code == 200:
        simulacion = response.json()
        return simulacion["angulo1"], simulacion["angulo2"], simulacion["peso"]
    else:
        print("Error al cargar la simulación:", response.json())
        return None, None, None

# Ejemplo de uso
angulo1 = 45
angulo2 = 56
peso = 890

# Guardar simulación
guardar_simulacion(angulo1, angulo2, peso)

# Cargar simulación (id = 1)
cargado_angulo1, cargado_angulo2, cargado_peso = cargar_simulacion(1)
if cargado_angulo1 is not None:
    print(f"Simulación cargada: Ángulo 1={cargado_angulo1}, Ángulo 2={cargado_angulo2}, Peso={cargado_peso}")
