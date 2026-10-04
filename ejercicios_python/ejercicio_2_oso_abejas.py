"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

# Mecanismos de sincronización
mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        sem_tarro_disponible.acquire()
        if not simulacion_activa:
            sem_tarro_disponible.release()
            break
            
        with mutex:
            tarro_miel += 1
            lleno = (tarro_miel == M)
            
        if lleno:
            print(f"🐝 Abeja {id_abeja}: ¡Tarro lleno! Despertando al oso 🐻")
            sem_oso.release()
        else:
            sem_tarro_disponible.release()

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        sem_oso.acquire()
        print("🐻 El oso se despierta y se come toda la miel!")
        with mutex:
            tarro_miel = 0
        tarros_comidos += 1
        sem_tarro_disponible.release()
        print("🐻 El oso vuelve a dormir.")
        time.sleep(0.05)
        
    simulacion_activa = False

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
    
    # Crear e iniciar el hilo del oso
    hilo_oso = threading.Thread(target=oso, args=(2,))
    hilo_oso.start()
    
    # Crear e iniciar los hilos de las abejas
    hilos_abejas = []
    for i in range(NUM_ABEJAS):
        h = threading.Thread(target=abeja, args=(i+1,))
        hilos_abejas.append(h)
        h.start()
        
    # Esperar a que terminen los hilos
    hilo_oso.join()
    for h in hilos_abejas:
        h.join()
        
    print("🏁 Simulación finalizada.")