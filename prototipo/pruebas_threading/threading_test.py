import threading
import numpy as np
import time
import keyboard

sync_event = threading.Event()
stop_event = threading.Event()

def poses_robotat():
    while not stop_event.is_set():
        sync_event.wait()
        print("hilo")
        sync_event.clear()
    print("Hilo terminado...")
    
t1 = threading.Thread(target = poses_robotat) # asignar hilp
t1.start() # iniciar hilo

time.sleep(2)
while True:
    print("ciclo principal")
    sync_event.set()
    time.sleep(0.5)
    
    if keyboard.is_pressed('a'):
        print("finalizado")
        # detener el hilo
        stop_event.set()
        sync_event.set()
        t1.join()   # esperar a que termine el hilo
        break
    
    