import sqlite3
import random
import time
from datetime import datetime

# 1. Configuración y conexión a la base de datos (Se creará solo aquí)
def inicializar_base_datos():
    conexion = sqlite3.connect("call_center.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS llamadas (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_hora TEXT,
            duracion_segundos INTEGER,
            estado TEXT
        )
   """)
    conexion.commit()
    conexion.close()

# 2. Función para registrar la llamada en la base de datos
def registrar_llamada(duracion):
    conexion = sqlite3.connect("call_center.db")
    cursor = conexion.cursor()
    
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO llamadas (fecha_hora, duracion_segundos, estado)
        VALUES (?, ?, ?)
    """, (fecha_actual, duracion, "Atendida"))
    
    conexion.commit()
    
    cursor.execute("SELECT COUNT(*) FROM llamadas")
    total_clientes = cursor.fetchone()[0]
    
    conexion.close()
    return total_clientes

# 3. Simulador del flujo del Call Center
def simular_call_center():
    inicializar_base_datos()
    print("--- Sistema de Monitoreo de Call Center Iniciado ---\n")
    
    try:
        while True:
            print("Esperando una llamada entrante...")
            time.sleep(random.randint(1, 4)) 
            
            print("¡Llamada entrante recibida! Atendiendo...")
            duracion_llamada = random.randint(3, 10)
            
            time.sleep(2) # Pausa para simular la llamada en progreso
            
            total_atendidos = registrar_llamada(duracion_llamada)
            
            print("\n=========================================")
            print("✔ LLAMADA FINALIZADA Y REGISTRADA")
            print(f"⏱ Duración de la llamada: {duracion_llamada} segundos")
            print(f"👥 Total de clientes atendidos: {total_atendidos}")
            print("=========================================\n")
            
            opcion = input("Presiona Enter para esperar otra llamada o 'q' para salir: ")
            if opcion.lower() == 'q':
                print("\nCerrando el sistema. ¡Buen trabajo hoy!")
                break
                
    except KeyboardInterrupt:
        print("\nSistema interrumpido. Saliendo...")

if __name__ == "__main__":
    simular_call_center()