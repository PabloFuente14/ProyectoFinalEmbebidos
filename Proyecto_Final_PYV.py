import Adafruit_DHT
import time
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import signal
import MySQLdb

#contador = 0

reader = SimpleMFRC522()
GPIO.setwarnings(False)
GPIO.cleanup()


db = MySQLdb.connect(host='localhost',user='PYV',passwd='PYV',db='DatosFabrica')
cur = db.cursor()

query = "TRUNCATE TABLE Contador"
cur.execute(query)
db.commit()

def buzz(duration):    
    GPIO.output(22, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(22, GPIO.LOW)

def rfid():    
    contador = 0
    #CODIGO de la tarjeta rfid
    while True:
        id , text = reader.read()
        if id == 1002848969990:
            contador += 1
            print('Accediendo con la tarjeta')
            
            print('contador: ',contador)
            print('------------------')
            time.sleep(1)  
    
        if id == 649130914353:
            contador += 1
            print('Accediendo con el llavero')
            #print('------------------')
            print('Contador: ',contador)
            print('------------------')
            time.sleep(1)

        
        
        query = "INSERT INTO Contador (contador) VALUES (%s)"
        cur.execute(query, (contador,))
        db.commit()
        
    
    
def temp_hum():
    #CODIGO de la temperatura y la huedad
    while True:
        print('------------------')
        print('Leyedo temperatura y humedad')
        humidity, temperature = Adafruit_DHT.read_retry(11,18)
        
        print('Temp = {0:0.1f}* Humidity = {1:0.1f}%'.format(temperature, humidity))
        print('------------------')
        time.sleep(5)
        
        
        cur.execute('''INSERT INTO Temp_Hum(humidity, temperature) VALUES(%s,%s);''',(humidity,temperature))
        db.commit()
        
        
        if humidity > 90:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(22, GPIO.OUT)
            pwm = GPIO.PWM(22, 500)
        # reproducir la melodía de alarma sencilla durante 10 segundos
            for note in notes:
                frequency, duration = note
                pwm.start(50)
                pwm.ChangeFrequency(frequency)
                buzz(duration / 1000.0)
                pwm.stop()
            time.sleep(1)
            
        if temperature > 30:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(22, GPIO.OUT)
            pwm = GPIO.PWM(22, 500)
        # reproducir la melodía de alarma sencilla durante 10 segundos
            for note in notes:
                frequency, duration = note
                pwm.start(50)
                pwm.ChangeFrequency(frequency)
                buzz(duration / 1000.0)
                pwm.stop()
            time.sleep(1)
    
notes = [
    (523, 500),
    (659, 500),
    (523, 500),
    (659, 500),
    (523, 500),
    (659, 500),
    (523, 500),
    (659, 500),
 
]


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
    
    