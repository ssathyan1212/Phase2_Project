# carla_simulator/carla_client.py
import carla
import time
def connect_to_carla(host='localhost', port=2000, timeout=10.0):
    client = carla.Client(host, port)
    client.set_timeout(timeout)
    world = client.get_world()
    print("[INFO] Connected to CARLA")
    return client, world
