import threading
import random
import time
import keyboard

def gen_rand(a,b):
    print(random.randint(a,b))
    
t1 = threading.Thread(target=gen_rand, args=(1,10))
t1.start()
while True:
    time.sleep(0.5)
    if t1.is_alive():
        print("t1 alive")
    else:
        print("t1 dead")
        t1.start()
    if keyboard.is_pressed('a'):
        break
    
