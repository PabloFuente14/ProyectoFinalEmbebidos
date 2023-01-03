#Libreria Adafruit_DHT
import Adafruit_DHT


while True:
    #primer número es el tipo de sensor, y el segundo el pin de la Rpi dónde tenemos puesto nuestro sensor
    humidity,temperature = Adafruit_DHT.read_retry(11,4)
    
    #Mostramos nuestro resultado formateándolo de la siguiente manera.
    print('Temp = {0:0.1f}* Humidity = {1:0.1f}%'.format(temperature, humidity))
    
    
    ##Hola Pablo