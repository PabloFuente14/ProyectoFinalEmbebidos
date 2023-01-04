import Adafruit_DHT
import time
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import signal
import MySQLdb


db = MySQLdb.connect(host='localhost',user='pi',passwd='pi',db='DatosFabrica')
cur = db.cursor()

reader = SimpleMFRC522()
GPIO.cleanup()


contador = 0

def rfid():
    #CODIGO de la tarjeta rfid
    while True:
        id , text = reader.read()
        
        if id == 1002848969990:
            contado += 1
            print('Accediendo con la tarjeta') 
            print('contador: ',contador) 
            time.sleep(1)  
    
        if id == 649130914353:
            contador += 1
            print('Accediendo con el llavero')
            print('Contador: ',contador)
            time.sleep(1)

        
        
    cur.execute('''INSERT INTO Contador(contador) VALUES(%s,%s);''',(contador))
    db.commit()
    
    
def temp_hum():
    #CODIGO de la temperatura y la huedad
    while True:
        print('Leyedo temperatura y humedad')
        humidity, temperature = Adafruit_DHT.read_retry(11,18)
        
        print('Temp = {0:0.1f}* Humidity = {1:0.1f}%'.format(temperature, humidity))
        time.sleep(1)
        
        
    cur.execute('''INSERT INTO Temp_Hum(humidity, temperature) VALUES(%s,%s);''',(humidity,temperature))
    db.commit()
    
if __name__ == '__main__':
    #Creamos los hilos
    t1 = threading.Thread(target=rfid)
    t2 = threading.Thread(target=temp_hum)
    
    #iniciamos los hilos:
    t1.start()
    t2.start()
    
    
    #Esperamos a que los hilos terminen
    t1.join()
    t2.join()
    
    