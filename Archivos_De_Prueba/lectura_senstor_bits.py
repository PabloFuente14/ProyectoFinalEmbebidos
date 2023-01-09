#Leeremos los valores del sensor mediante la lectura de los bits.
import time
import RPi
import RPi.GPIO as GPIO
import datetime
import _thread

class DHT11:
    pin = 17

    def __init__(self, pin):
        self.pin = pin
        
    def read(self):

        #LEEMOS EL PULSO DE ESTART
        RPi.GPIO.setup(self.pin, RPi.GPIO.OUT)

        # Enviar HIGH inicial para avisar de que queremos establecer conexión
        RPi.GPIO.output(self.pin, RPi.GPIO.HIGH)
        time.sleep(0.05)

        # ENVIAR LOW (debes ser >18ms) para que no la confunda con un 0
        RPi.GPIO.output(self.pin, RPi.GPIO.LOW)
        time.sleep(0.02)
  
        # #GPIO OUTPUT - PULLUP RESISTOR
        RPi.GPIO.setup(self.pin, RPi.GPIO.IN, RPi.GPIO.PUD_UP)
        
       
        data = self.get_data()


        # Calcular el numero de 0s y 1s de cada pulso (tamanos de los pulsos alto y bajo)
        data_lengths = self.parse_data(data)

        # Error: numero de bits recibidos erroneos (segun datasheet 40 bits totaltes)
        if len(data_lengths) != 40:
            print("ERROR: numero de bits recibidos: "+str(data_lengths))
            return -1,-1

        #Calcular bits a partir del tamano de los pulsos alto y bajo
        
        bits = self.calculate_bits(data_lengths)
        print("Formato de bits: "+str(bits))


        #Extraemos los bytes y los almacenamos
        bytes = []
        size=8
        for i in range(0, len(bits), size):
            byte = bits[i:i + size]
            bytes.append(byte)
        
        
        #para cada bite del byte comprovamos su valor decimal y lo almacenamos
        num = []
        
        for b in bytes:
            index = 7
            n=0
            for bit in b:
                n=n + (bit*(2**(index)))
                index= index-1
            num.append(n)   
        
        #Comprobamos que el checksum es correcto
        
        checksum= num[0]+ num[1]+num[2]+num[3]
        if checksum == num[4]:
            print("Lectura buena")
            temperature = num[0] + (num[1]/10)
            humidity = num[2]+ (num[3]/10)
        else:
            print("Lectura mala")
            temperature = 0
            humidity = 0

        return temperature, humidity



    # Vamos a comprobar que la lectura se hace bien y no hay transiciones entre 0s y 1s en 100 mediciones
    def get_data(self):
        unchanged_count = 0
        max_unchanged_count = 100

        last = -1
        data = []
        while True:
            current = RPi.GPIO.input(self.pin)
            data.append(current)
            if last != current:
                unchanged_count = 0
                last = current
            else:
                unchanged_count += 1
                if unchanged_count > max_unchanged_count:
                    break

        return data

    #Maquina de estados
    def parse_data(self, data):
        STATE_INIT = 1
        STATE_INIT_PULL_UP = 2
        STATE_DATA_FIRST_LOW = 3
        STATE_DATA_HIGH = 4
        STATE_DATA_LOW = 5

        state = STATE_INIT

        lengths = [] #
        current_length = 0

        for i in range(len(data)):
            current = data[i]
            current_length += 1

            if state == STATE_INIT:
                if current == 0:
                    state = STATE_INIT_PULL_UP
                    continue
                else:
                    continue
            if state == STATE_INIT_PULL_UP:
                if current == 1:
                    state = STATE_DATA_FIRST_LOW
                    continue
                else:
                    continue
            if state == STATE_DATA_FIRST_LOW:
                if current == 0:
                    state = STATE_DATA_HIGH
                    continue
                else:
                    continue
            if state == STATE_DATA_HIGH:
                if current == 1:
                    current_length = 0
                    state = STATE_DATA_LOW
                    continue
                else:
                    continue
            if state == STATE_DATA_LOW:
                if current == 0:
                    lengths.append(current_length)
                    state = STATE_DATA_HIGH
                    continue
                else:
                    continue

        return lengths

    def calculate_bits(self, data_lengths):
        # encontrar periodo mas largo y mas corto para establecer umbral entre 0 y 1
        shortest_pull_up = 1000
        longest_pull_up = 0

        for i in range(0, len(data_lengths)):
            length = data_lengths[i]
            if length < shortest_pull_up:
                shortest_pull_up = length
            if length > longest_pull_up:
                longest_pull_up = length
        
        # la mitad del valor lo usamos para distinguir entre 0 y 1
        halfway = shortest_pull_up + (longest_pull_up - shortest_pull_up) / 2
        bits = []

        for i in range(0, len(data_lengths)):
            bit = 0
            if data_lengths[i] > halfway:
                bit = 1
            bits.append(bit)

        return bits



   
#---------------------------------
#PROGRAMA DE PRUEBA DEL SENSOR
#---------------------------------
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Ejemplo usando del GPIO 5
instance = DHT11(pin=17)

#Creo un hilo que llame a envio
_thread.start_new_thread(envio,())

while True:
    result_temperature,result_humidity = instance.read()
    current_time = datetime.datetime.now()
    print("Temperatura LCD: "+str(result_temperature))
    print("Humedad LCD: "+str(result_humidity))
    #solo mostrar valores si no hay error en el checksum
   


