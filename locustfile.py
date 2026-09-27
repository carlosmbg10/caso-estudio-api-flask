import random
from datetime import date, timedelta

from locust import HttpUser, task, between

NOMBRES = ["Carlos", "Ana", "Luis", "Maria", "Jorge", "Laura", "Andres", "Camila"]
APELLIDOS = ["Bañol", "Gomez", "Ramirez", "Torres", "Vargas", "Ortiz", "Castro"]


class ApiUser(HttpUser):
    """
    Usuario simulado que ejercita los 3 endpoints del microservicio de
    utilidades: /api/persona, /api/salario y /api/edad, cubriendo casos
    válidos e inválidos.
    """
    wait_time = between(1, 3)

    @task(2)
    def persona_valido(self):
        payload = {
            "nombre": random.choice(NOMBRES),
            "apellido": random.choice(APELLIDOS),
        }
        with self.client.post("/api/persona", json=payload, catch_response=True) as resp:
            if resp.status_code == 200 and "nombre_completo" in resp.json():
                resp.success()
            else:
                resp.failure(f"Respuesta inesperada: {resp.status_code} - {resp.text}")

    @task(1)
    def persona_invalido(self):
        payload = {"nombre": "", "apellido": ""}
        with self.client.post("/api/persona", json=payload, catch_response=True) as resp:
            if resp.status_code == 400:
                resp.success()
            else:
                resp.failure(f"Se esperaba 400 y llegó {resp.status_code}")

    @task(2)
    def salario_valido(self):
        salario = round(random.uniform(800_000, 8_000_000), 2)
        with self.client.post("/api/salario", json={"salario": salario}, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Se esperaba 200 y llegó {resp.status_code}")
                return
            data = resp.json()
            neto_esperado = round(salario * 0.8, 2)
            if abs(data.get("salario_neto", 0) - neto_esperado) < 0.5:
                resp.success()
            else:
                resp.failure(f"Neto incorrecto: esperado {neto_esperado}, recibido {data.get('salario_neto')}")

    @task(2)
    def edad_valida(self):
        dias_atras = random.randint(365 * 5, 365 * 70)
        fecha_nacimiento = (date.today() - timedelta(days=dias_atras)).isoformat()
        with self.client.get(
            f"/api/edad?fecha_nacimiento={fecha_nacimiento}",
            name="/api/edad?fecha_nacimiento=[valida]",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200 and "edad" in resp.json():
                resp.success()
            else:
                resp.failure(f"Respuesta inesperada: {resp.status_code} - {resp.text}")

    @task(1)
    def edad_futura(self):
        fecha_futura = (date.today() + timedelta(days=365)).isoformat()
        with self.client.get(
            f"/api/edad?fecha_nacimiento={fecha_futura}",
            name="/api/edad?fecha_nacimiento=[futura]",
            catch_response=True,
        ) as resp:
            if resp.status_code == 400:
                resp.success()
            else:
                resp.failure(f"Se esperaba 400 y llegó {resp.status_code}")
